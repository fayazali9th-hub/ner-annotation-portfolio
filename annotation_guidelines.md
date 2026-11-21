# NER Annotation Guidelines

## 1. Objective
Label each token in a sentence using BIO tags for PERSON, ORG, LOC, DATE, and MONEY.

## 2. Label definitions
- **PERSON:** Full or partial personal names when used to identify a person.
- **ORG:** Companies, government bodies, educational institutions, charities, and other formal organizations.
- **LOC:** Geographical places such as cities, countries, regions, and named locations.
- **DATE:** Explicit dates and temporal expressions, including month/year expressions and relative dates.
- **MONEY:** Currency symbols/codes and monetary amounts. Keep the complete amount together as one entity.

## 3. BIO convention
- `B-TYPE`: first token of an entity.
- `I-TYPE`: every later token in the same entity.
- `O`: token outside all target entities.

Example: `Emily Carter joined Amazon.`
```text
Emily   B-PERSON
Carter  I-PERSON
joined  O
Amazon  B-ORG
.       O
```

## 4. Boundary rules
1. Include all tokens that form the named entity.
2. Do not include surrounding punctuation unless it is intrinsic to the entity.
3. Multi-token names receive one `B-` followed by `I-` tags.
4. Adjacent entities of the same type each begin with a new `B-` tag.
5. Every token must have exactly one tag.

## 5. Consistency rules
- An `I-TYPE` must follow `B-TYPE` or `I-TYPE` of the same type.
- A new entity always starts with `B-TYPE`.
- Use `O` for ordinary verbs, prepositions, articles, and punctuation outside entity spans.
- Do not infer entities that are not explicitly present in the text.

## 6. Review checklist
- [ ] Every person name is labeled PERSON.
- [ ] Every organization name is labeled ORG.
- [ ] Every geographical place is labeled LOC.
- [ ] Every date/time expression is labeled DATE.
- [ ] Every monetary amount is labeled MONEY.
- [ ] BIO boundaries and token/tag alignment are valid.
