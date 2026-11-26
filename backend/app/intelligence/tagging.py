import re
from collections import Counter

FRENCH_STOPWORDS = {
    "a", "au", "aux", "avec", "ce", "ces", "dans", "de", "des", "du", "elle", "en",
    "et", "eux", "il", "je", "la", "le", "les", "leur", "lui", "ma", "mais", "me",
    "meme", "mes", "moi", "mon", "ne", "nos", "notre", "nous", "on", "ou", "par",
    "pas", "pour", "qu", "que", "qui", "sa", "se", "ses", "son", "sur", "ta", "te",
    "tes", "toi", "ton", "tu", "un", "une", "vos", "votre", "vous", "the", "and",
    "est", "sont", "cette", "cet", "comme", "plus", "tout", "tous",
}

CATEGORY_RULES = {
    "rapport": {"rapport", "annuel", "analyse", "bilan", "synthese"},
    "contacts": {"contact", "nom", "ville", "email", "telephone"},
    "technique": {"projet", "systeme", "informatique", "indexation", "recherche"},
    "administratif": {"facture", "contrat", "budget", "administration"},
}


def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-ZÀ-ÿ0-9]{3,}", text.lower())
    return [word for word in words if word not in FRENCH_STOPWORDS]


def detect_category(tokens: list[str]) -> str | None:
    token_set = set(tokens)
    best_category = None
    best_score = 0

    for category, keywords in CATEGORY_RULES.items():
        score = len(token_set & keywords)
        if score > best_score:
            best_score = score
            best_category = category

    return best_category


def generate_tags(title: str, content: str, file_type: str) -> list[str]:
    tokens = _tokenize(f"{title} {content}")
    counts = Counter(tokens)
    top_keywords = [word for word, _ in counts.most_common(5)]

    tags = [file_type.lower()]
    category = detect_category(tokens)
    if category:
        tags.append(category)

    for keyword in top_keywords:
        if keyword not in tags:
            tags.append(keyword)

    return tags[:8]


def generate_summary(content: str, max_length: int = 220) -> str:
    """Résumé extractif léger : phrases scorées par densité de mots informatifs."""
    cleaned = " ".join(content.split())
    if not cleaned:
        return ""

    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[\.\!\?])\s+", cleaned)
        if sentence.strip()
    ]
    if not sentences:
        return cleaned[:max_length]

    if len(sentences) == 1 or len(cleaned) <= max_length:
        return cleaned if len(cleaned) <= max_length else cleaned[: max_length - 3].rstrip() + "..."

    global_tokens = _tokenize(cleaned)
    if not global_tokens:
        return cleaned[: max_length - 3].rstrip() + "..."

    frequencies = Counter(global_tokens)
    scored: list[tuple[float, int, str]] = []
    for index, sentence in enumerate(sentences):
        tokens = _tokenize(sentence)
        if not tokens:
            continue
        score = sum(frequencies[token] for token in tokens) / len(tokens)
        # Léger bonus aux premières phrases
        score += max(0, 0.35 - index * 0.05)
        scored.append((score, index, sentence))

    if not scored:
        return cleaned[: max_length - 3].rstrip() + "..."

    scored.sort(key=lambda item: item[0], reverse=True)
    selected = sorted(scored[:3], key=lambda item: item[1])
    summary = " ".join(sentence for _, _, sentence in selected)

    if len(summary) <= max_length:
        return summary
    return summary[: max_length - 3].rstrip() + "..."
