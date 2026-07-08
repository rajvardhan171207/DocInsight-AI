import os
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def create_word_chart(text):

    if not text or not text.strip():
        return None

    words = text.lower().split()

    stop_words = {
        "the","a","an","is","are","of","to","and",
        "in","for","on","with","that","this","it",
        "as","at","by","be","or","from"
    }

    words = [
        word.strip(".,!?()[]{}:;\"'")
        for word in words
        if word not in stop_words and len(word) > 2
    ]

    common = Counter(words).most_common(10)

    labels = [x[0] for x in common]
    values = [x[1] for x in common]

    os.makedirs("static/charts", exist_ok=True)

    plt.style.use("ggplot")

    fig, ax = plt.subplots(figsize=(10,5))

    bars = ax.bar(
        labels,
        values,
        color="#3B82F6",
        edgecolor="#1E40AF",
        linewidth=1.5
    )

    ax.set_title(
        "Top 10 Most Frequent Words",
        fontsize=18,
        fontweight="bold"
    )

    ax.set_xlabel("Words", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)

    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.xticks(rotation=25)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x()+bar.get_width()/2,
            height+0.2,
            str(height),
            ha="center",
            fontsize=10,
            fontweight="bold"
        )

    plt.tight_layout()

    chart_path = "static/charts/word_chart.png"

    plt.savefig(chart_path, dpi=300)

    plt.close()

    return chart_path

def create_wordcloud(text):

    os.makedirs("static/charts", exist_ok=True)

    # Prevent error if text is empty
    if not text or not text.strip():
        return None

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="white",
        collocations=False
    ).generate(text)

    path = "static/charts/wordcloud.png"

    wc.to_file(path)

    return path
