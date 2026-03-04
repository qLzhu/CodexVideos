from collections import Counter


def detect_summary_phrases(text: str, phrases: list[str]) -> list[str]:
    return [p for p in phrases if p in text]


def detect_repeated_lines(text: str, min_occurrence: int = 2) -> list[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    cnt = Counter(lines)
    return [line for line, c in cnt.items() if c >= min_occurrence]


def detect_long_paragraphs(text: str, max_chars: int) -> list[dict]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    result = []
    for idx, p in enumerate(paragraphs, start=1):
        if len(p) > max_chars:
            result.append({"paragraph_index": idx, "length": len(p), "max_chars": max_chars})
    return result


def run_rule_qc(text: str, rules: dict) -> dict:
    summary_phrases = rules.get("summary_phrases", [])
    repetition = rules.get("repetition", {"min_occurrence": 2})
    paragraph = rules.get("paragraph", {"max_chars": 300})

    hits = {
        "summary_phrase_hits": detect_summary_phrases(text, summary_phrases),
        "repeated_lines": detect_repeated_lines(text, repetition.get("min_occurrence", 2)),
        "long_paragraphs": detect_long_paragraphs(text, paragraph.get("max_chars", 300)),
    }

    score = 100
    score -= len(hits["summary_phrase_hits"]) * 10
    score -= len(hits["repeated_lines"]) * 5
    score -= len(hits["long_paragraphs"]) * 5
    score = max(0, score)

    return {
        "score": score,
        "passed": score >= rules.get("pass_score", 70),
        "hits": hits,
    }
