def classify_experience(text: str):
    text = text.lower()

    keywords = ["intern", "fresher", "student", "no experience"]
    for k in keywords:
        if k in text:
            return "entry"

    return "experienced"
