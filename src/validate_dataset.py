"""Validate token-level BIO tags in the NER JSONL dataset."""
from pathlib import Path
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "ner_dataset.jsonl"
VALID_TYPES = {"PERSON", "ORG", "LOC", "DATE", "MONEY"}
VALID_TAGS = {"O"} | {f"{p}-{t}" for p in ("B", "I") for t in VALID_TYPES}

def validate():
    seen_ids = set()
    tag_counts = Counter()
    entity_counts = Counter()
    errors = []
    sentence_count = token_count = 0

    with DATASET.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            sentence_count += 1
            row = json.loads(line)
            sid = row.get("sentence_id")
            if sid in seen_ids:
                errors.append(f"Line {line_no}: duplicate sentence_id {sid}")
            seen_ids.add(sid)

            tokens, tags = row.get("tokens", []), row.get("tags", [])
            if len(tokens) != len(tags):
                errors.append(f"Line {line_no} ({sid}): token/tag length mismatch")
                continue
            previous_type = None
            previous_prefix = "O"
            for index, (token, tag) in enumerate(zip(tokens, tags), start=1):
                token_count += 1
                tag_counts[tag] += 1
                if tag not in VALID_TAGS:
                    errors.append(f"Line {line_no} ({sid}), token {index}: invalid tag {tag}")
                    previous_type, previous_prefix = None, "O"
                    continue
                if tag == "O":
                    previous_type, previous_prefix = None, "O"
                    continue
                prefix, entity_type = tag.split("-", 1)
                entity_counts[entity_type] += 1 if prefix == "B" else 0
                if prefix == "I" and not (previous_prefix in {"B", "I"} and previous_type == entity_type):
                    errors.append(f"Line {line_no} ({sid}), token {index}: illegal BIO transition to {tag}")
                previous_type, previous_prefix = entity_type, prefix

    print(f"Sentences: {sentence_count}")
    print(f"Tokens: {token_count}")
    print("Entity starts:", dict(entity_counts))
    print("BIO tags:", dict(tag_counts))
    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for error in errors[:30]:
            print("-", error)
        return 1
    print("PASSED: no structural BIO errors found.")
    return 0

if __name__ == "__main__":
    raise SystemExit(validate())
