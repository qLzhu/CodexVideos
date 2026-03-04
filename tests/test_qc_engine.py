from app.core.qc_engine import run_rule_qc


def test_qc_hits():
    text = "那一刻我终于明白\n\n重复句\n重复句\n\n" + ("长段" * 100)
    rules = {
        "pass_score": 99,
        "summary_phrases": ["那一刻我终于明白"],
        "repetition": {"min_occurrence": 2},
        "paragraph": {"max_chars": 50},
    }
    report = run_rule_qc(text, rules)
    assert report["hits"]["summary_phrase_hits"]
    assert report["hits"]["repeated_lines"]
    assert report["hits"]["long_paragraphs"]
    assert report["passed"] is False
