"""Generate the deterministic synthetic NER portfolio dataset (standard library only)."""
from pathlib import Path
import random, json, csv, re, collections

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SEED, COUNT = 20261121, 2500
VALUES = {
 "PERSON": ["Emily Carter","Aisha Khan","Daniel Brooks","Maria Garcia","Omar Farooq","Sophia Chen","James Wilson","Noah Ahmed","Olivia Martin","Liam Patel","Zara Hussain","Ethan Clark","Maya Johnson","Adam Rivera","Hana Ali","Lucas Moore","Sara Malik","David Kim","Amir Shah","Isabella Brown"],
 "ORG": ["Amazon","Microsoft","OpenAI","Google","World Health Organization","United Nations","Acme Technologies","Northstar Bank","Greenfield University","Global Relief Foundation","Pakistan State Oil","Bright Future Academy","Nova Robotics","Crescent Hospital","Atlas Logistics"],
 "LOC": ["Seattle","Karachi","Lahore","Islamabad","New York","London","Tokyo","Dubai","Pakistan","Canada","Sindh","California","Hyderabad","Berlin","Singapore","Thatta"],
 "DATE": ["January 12, 2025","March 2024","June 5, 2023","November 21, 2026","next Monday","yesterday","in 2022","December 31, 2025","April 18","last summer","February 2021","on Friday"],
 "MONEY": ["$2,500","$1.2 million","€750","£4,000","Rs. 50,000","PKR 125,000","$89.99","¥30,000","Rs. 2.5 million","$10 billion","€1,500","PKR 8,750"]
}
TEMPLATES = [
 ["",("PERSON","p")," joined ",("ORG","o")," in ",("LOC","l")," on ",("DATE","d"),"."],
 [("PERSON","p")," moved to ",("LOC","l")," after accepting a role at ",("ORG","o"),"."],
 [("ORG","o")," announced a new office in ",("LOC","l")," on ",("DATE","d"),"."],
 ["The contract was valued at ",("MONEY","m")," and signed by ",("PERSON","p"),"."],
 [("PERSON","p")," donated ",("MONEY","m")," to ",("ORG","o")," in ",("DATE","d"),"."],
 ["Representatives from ",("ORG","o")," met ",("PERSON","p")," in ",("LOC","l"),"."],
 ["The conference in ",("LOC","l")," will begin ",("DATE","d"),", according to ",("ORG","o"),"."],
 [("PERSON","p")," paid ",("MONEY","m")," for a service provided by ",("ORG","o"),"."],
 [("ORG","o")," hired ",("PERSON","p")," to lead its ",("LOC","l")," operations."],
 ["A report published ",("DATE","d")," identified new investment opportunities in ",("LOC","l"),"."],
 [("PERSON","p")," traveled from ",("LOC","l")," to meet officials at ",("ORG","o"),"."],
 ["The grant of ",("MONEY","m")," was approved on ",("DATE","d")," by ",("ORG","o"),"."],
 [("ORG","o")," plans to expand its services across ",("LOC","l")," next year."],
 [("PERSON","p")," will speak at ",("ORG","o"),"'s event in ",("LOC","l")," on ",("DATE","d"),"."],
 ["Investors committed ",("MONEY","m")," to ",("ORG","o")," during a meeting in ",("LOC","l"),"."],
 ["The shipment reached ",("LOC","l")," on ",("DATE","d")," and was received by ",("PERSON","p"),"."],
 [("ORG","o")," awarded ",("MONEY","m")," to ",("PERSON","p")," for research completed in ",("DATE","d"),"."],
 [("PERSON","p")," joined the board of ",("ORG","o")," while based in ",("LOC","l"),"."],
 ["Officials in ",("LOC","l")," confirmed the agreement with ",("ORG","o")," on ",("DATE","d"),"."],
 ["The project budget increased to ",("MONEY","m")," after ",("PERSON","p")," contacted ",("ORG","o"),"."],
 [("ORG","o")," opened a training center in ",("LOC","l")," during ",("DATE","d"),"."],
 [("PERSON","p")," said the equipment cost ",("MONEY","m")," at a press briefing in ",("LOC","l"),"."],
 ["A partnership between ",("ORG","o")," and ",("ORG","o")," was announced on ",("DATE","d"),"."],
 ["The delegation from ",("LOC","l")," was led by ",("PERSON","p")," and welcomed by ",("ORG","o"),"."],
 ["According to ",("ORG","o"),", ",("PERSON","p")," will receive ",("MONEY","m")," by ",("DATE","d"),"."]
]
TOKEN_RE = re.compile(r"\w+(?:[.,:/’'-]\w+)*|[$€£¥]+|[.,!?;:()'’]")

def main():
    DATA.mkdir(exist_ok=True)
    rng = random.Random(SEED)
    records = []
    for i in range(COUNT):
        sentence_parts, spans, offset = [], [], 0
        for part in rng.choice(TEMPLATES):
            if isinstance(part, tuple):
                label, _ = part
                value = rng.choice(VALUES[label])
                sentence_parts.append(value)
                spans.append((offset, offset + len(value), label))
                offset += len(value)
            else:
                sentence_parts.append(part)
                offset += len(part)
        sentence = "".join(sentence_parts)
        tokens, tags = [], []
        for match in TOKEN_RE.finditer(sentence):
            overlaps = [s for s in spans if match.start() < s[1] and match.end() > s[0]]
            if not overlaps:
                tag = "O"
            else:
                start, end, label = overlaps[0]
                first = not any(m.start() >= start and m.start() < match.start() for m in TOKEN_RE.finditer(sentence))
                tag = ("B-" if first else "I-") + label
            tokens.append(match.group())
            tags.append(tag)
        records.append({"sentence_id": f"NER-{i+1:05d}", "text": sentence, "tokens": tokens, "tags": tags,
                        "entities": [{"text": sentence[a:b], "label": t, "start": a, "end": b} for a,b,t in spans]})

    with (DATA / "ner_dataset.jsonl").open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    with (DATA / "ner_dataset.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sentence_id","text","tokens","tags","entities"])
        writer.writeheader()
        for record in records:
            writer.writerow({**record, **{k: json.dumps(record[k], ensure_ascii=False) for k in ("tokens","tags","entities")}})
    with (DATA / "ner_dataset.conll").open("w", encoding="utf-8") as f:
        for record in records:
            f.write(f"# {record['sentence_id']} | {record['text']}\n")
            f.writelines(f"{token}\t{tag}\n" for token,tag in zip(record["tokens"],record["tags"]))
            f.write("\n")
    tag_counts = collections.Counter(tag for r in records for tag in r["tags"])
    entity_counts = collections.Counter(e["label"] for r in records for e in r["entities"])
    stats = {"sentence_count": len(records), "token_count": sum(map(lambda r: len(r["tokens"]), records)),
             "entity_mention_count": sum(len(r["entities"]) for r in records),
             "entity_types": sorted(VALUES), "entity_mentions_by_type": dict(entity_counts),
             "bio_tag_counts": dict(tag_counts),
             "dataset_note": "Synthetic, template-generated portfolio dataset; not human-annotated or sourced from real records."}
    (DATA / "dataset_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(f"Generated {len(records)} sentences in {DATA}")

if __name__ == "__main__":
    main()
