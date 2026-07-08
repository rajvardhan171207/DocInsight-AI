from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_pdf_report(filename, stats, summary, keywords):

    os.makedirs("reports", exist_ok=True)

    report_path = f"reports/{filename}_report.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(report_path)

    story = []

    story.append(Paragraph("<b>DocInsight AI Report</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Document:</b> {filename}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Words:</b> {stats['words']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Characters:</b> {stats['characters']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Sentences:</b> {stats['sentences']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Reading Time:</b> {stats['reading_time']} min", styles["BodyText"]))

    story.append(Paragraph("<br/><b>AI Summary</b>", styles["Heading2"]))
    story.append(Paragraph(summary, styles["BodyText"]))

    story.append(Paragraph("<br/><b>Keywords</b>", styles["Heading2"]))
    story.append(Paragraph(", ".join(keywords), styles["BodyText"]))

    doc.build(story)

    return report_path