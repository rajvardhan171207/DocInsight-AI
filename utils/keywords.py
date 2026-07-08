import yake


def extract_keywords(text, num_keywords=10):
    kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=2,
        dedupLim=0.9,
        top=num_keywords
    )

    keywords = kw_extractor.extract_keywords(text)

    return [keyword for keyword, score in keywords]
