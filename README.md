# Named Entity Recognition (NER) Annotation Portfolio

A reproducible NER annotation portfolio project demonstrating token-level BIO tagging for five entity types: **PERSON, ORGANIZATION, LOCATION, DATE, and MONEY**.

## Project scope

- 2,500 synthetic sentences
- BIO labels: `B-PERSON`, `I-PERSON`, `B-ORG`, `I-ORG`, `B-LOC`, `I-LOC`, `B-DATE`, `I-DATE`, `B-MONEY`, `I-MONEY`, and `O`
- Dataset exports: JSONL, CSV, and CoNLL
- Annotation guidelines and a Python validation script
- Entity and BIO-tag distribution report

> **Data transparency:** The included dataset is synthetic and generated from templates for portfolio practice. It is not human-annotated, independently reviewed, or sourced from real people or organizations. Do not describe it as a manually annotated production dataset.

## Repository structure

```text
ner-annotation-portfolio/
├── data/
│   ├── ner_dataset.jsonl
│   ├── ner_dataset.csv
│   ├── ner_dataset.conll
│   └── dataset_stats.json
├── docs/
│   └── annotation_guidelines.md
├── src/
│   ├── generate_dataset.py
│   └── validate_dataset.py
├── requirements.txt
└── README.md
```

## Entity schema

| Entity | Meaning | Example |
|---|---|---|
| PERSON | A person's name | Emily Carter |
| ORG | Company, institution, or organization | Amazon |
| LOC | City, country, region, or place | Seattle |
| DATE | Calendar date or time expression | January 12, 2025 |
| MONEY | Monetary amount | $2,500 |
| O | Token that is not part of a target entity | moved |

## BIO tagging example

Sentence: `Emily Carter joined Amazon in Seattle on January 12, 2025.`

```text
Emily       B-PERSON
Carter      I-PERSON
joined      O
Amazon      B-ORG
in          O
Seattle     B-LOC
on          O
January     B-DATE
12          I-DATE
,           I-DATE
2025        I-DATE
.           O
```

A `B-` tag marks the first token of an entity. An `I-` tag marks a subsequent token in the same entity. `O` means the token is outside all target entities.

## Quick start

This project uses Python's standard library; no third-party packages are required.

```bash
python src/validate_dataset.py
```

To regenerate the dataset:

```bash
python src/generate_dataset.py
```

The generator uses a fixed random seed so the output is reproducible.

## Dataset formats

- **JSONL:** one sentence record per line, including text, tokens, BIO tags, and entity character offsets.
- **CSV:** one sentence per row; list-valued fields are JSON-encoded.
- **CoNLL:** one token and BIO tag per line, with blank lines between sentences.

## Quality checks

The validator checks:
1. Required fields and unique sentence IDs.
2. Equal token and tag counts.
3. Allowed BIO tag names.
4. Valid BIO transitions (`I-` cannot start a sequence or follow `O`/a different entity type).
5. Dataset size and basic entity coverage.

## Limitations and next steps

This is a portfolio demonstration, not a benchmark dataset. Template-generated text has limited linguistic diversity and may not represent real-world ambiguity, spelling variation, nested entities, or domain-specific usage. A stronger production-style extension would add human review, adjudication, inter-annotator agreement, and a separately sourced evaluation set.

## Skills demonstrated

- Named entity annotation
- Tokenization and BIO sequence labeling
- Annotation guideline design
- Dataset formatting and export
- Python data validation
- Basic dataset quality reporting
