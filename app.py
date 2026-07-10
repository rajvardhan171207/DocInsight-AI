print("APP.PY IS RUNNING")
from flask import Flask, render_template, request, redirect, url_for, session
import os

from utils.pdf_reader import extract_pdf_text
from utils.docx_reader import extract_docx_text
from utils.statistics import document_statistics
from utils.gemini import(generate_summary, classify_document,
                         analyze_sentiment,
                        )
from db import get_connection
from utils.keywords import extract_keywords
from utils.chatbot import ask_document
from utils.pdf_report import create_pdf_report
from flask import send_from_directory
from datetime import datetime
from utils.ocr import extract_image_text

from utils.charts import create_word_chart, create_wordcloud
from history.history import save_history, load_history
from utils.recommendation import generate_recommendation
from history.database_history import save_history_db, load_history_db, get_dashboard_stats
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {  "pdf", "docx", "txt", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            session["role"] = user["role"]

            return redirect(url_for("dashboard"))

        else:
            return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )

            conn.commit()

        finally:
            conn.close()

        print("User Registered Successfully")

        return redirect(url_for("login"))

    return render_template("register.html")
       

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    dashboard = get_dashboard_stats(session["user_id"])

    return render_template(
        "index.html",
        dashboard=dashboard
    )

@app.route("/upload", methods=["POST"])
def upload():
    if "user_id" not in session:
     return redirect(url_for("login"))

    if "document" not in request.files:
        return "No file uploaded."

    file = request.files["document"]

    if file.filename == "":
        return "No file selected."

    if not allowed_file(file.filename):
        return "Unsupported file type."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    extension = file.filename.rsplit(".", 1)[1].lower()

    # Extract text
    if extension == "pdf":
       extracted_text, total_pages = extract_pdf_text(filepath)

       print("=" * 50)
       print(extracted_text[:500])
       print("=" * 50)
    elif extension == "docx":
        extracted_text = extract_docx_text(filepath)
        total_pages = "N/A"
    elif extension in ["png", "jpg", "jpeg"]:
        extracted_text = extract_image_text(filepath)
        total_pages = "Image"
    else:
        # txt and other text files
        with open(filepath, "r", encoding="utf-8") as f:
            extracted_text = f.read()
        total_pages = "N/A"
    
    print("=" * 50)
    print("Word Count:", len(extracted_text.split()))
    print("Character Count:", len(extracted_text))
    print("=" * 50)

    # Statistics
    stats = document_statistics(extracted_text)
    keywords = extract_keywords(extracted_text)
    chart = create_word_chart(extracted_text)
    wordcloud = create_wordcloud(extracted_text)
    print("Extracted Text:")
    print(extracted_text[:500])
    print("Length:", len(extracted_text))    

    

    # Gemini Summary
    try:
        # summary = generate_summary(extracted_text[:8000])
        # document_type = classify_document(extracted_text[:5000])
        # sentiment = analyze_sentiment(extracted_text[:5000])
        # recommendation= generate_recommendation(extracted_text[:5000])
        from utils.ai_analysis import analyze_document

        analysis = analyze_document(extracted_text[:10000])

        summary = analysis["summary"]
        document_type = analysis["document_type"]
        sentiment = analysis["sentiment"]
        recommendation = analysis["recommendations"]
        print("Before save_history_db")
        save_history_db(
    session["user_id"],
    file.filename,
    document_type,
    stats
)  
        print("After save_history_db")
        print("History saved successfully")
    except Exception as e:
        summary = f"Gemini Error: {str(e)}"
        document_type = "Unknown"
        sentiment = "Unknown"
        recommendation = "Recommendations unavailable."
 
    # Create PDF Report
    report = create_pdf_report(
        file.filename,
        stats,
        summary,
        keywords
    )
    analysis_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    return render_template(
        "result.html",
        filename=file.filename,
        extracted_text=extracted_text,
        summary=summary,
        stats=stats,
        keywords=keywords,
        report=report,
        analysis_time=analysis_time,
        total_pages=total_pages,
        sentiment=sentiment,
        chart=chart,
        wordcloud=wordcloud,
        recommendation=recommendation,
        document_type=document_type)


@app.route("/reports/<path:filename>")
def download_report(filename):
    return send_from_directory("reports", filename, as_attachment=True)

@app.route("/ask", methods=["POST"])
def ask():

    question = request.form["question"]
    document_text = request.form["document_text"]

    try:
        answer = ask_document(document_text[:7000], question)
    except Exception:
        answer = "⚠️ Unable to contact Gemini AI right now. Please try again later."

    return render_template(
        "chat_result.html",
        question=question,
        answer=answer
    )


@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    records = load_history_db(session["user_id"])
    print(records)

    return render_template(
        "history.html",
        records=records
    )

@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM history ORDER BY id DESC")
    history = cursor.fetchall()
    print("Total Users:", len(users))
    print("Total History:", len(history))
    conn.close()

    return render_template(
        "admin.html",
        users=users,
        history=history
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
print("\n===== REGISTERED ROUTES =====")
print(app.url_map)

if __name__ == "__main__":
      app.run(debug=True, use_reloader=False)