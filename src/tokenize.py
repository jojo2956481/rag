import re
import Stemmer


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    # stemmer = Stemmer.Stemmer("english")
    for word in re.findall(r"[A-Za-z0-9_]+", text):
        tokens.append(word.lower())
        parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", word)
        if len(parts) > 1:
            tokens.extend(p.lower() for p in parts)
        # return stemmer.stemWords(tokens)
    return tokens
