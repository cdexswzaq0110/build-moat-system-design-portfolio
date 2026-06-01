import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs" / "sample"
KB_DIR = ROOT_DIR / ".kb"
INDEX_PATH = KB_DIR / "index.json"
TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "does",
    "for",
    "from",
    "he",
    "how",
    "i",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "what",
    "who",
    "why",
    "with",
}


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]


def tokenize_meaningful(text: str) -> list[str]:
    return [token for token in tokenize(text) if token not in STOPWORDS and len(token) > 1]


def split_markdown_sections(content: str, source: str) -> list[dict[str, Any]]:
    headings = list(HEADING_PATTERN.finditer(content))
    if not headings:
        return [
            {
                "id": f"{source}#document",
                "source": source,
                "heading": "Document",
                "content": content.strip(),
            }
        ]

    sections: list[dict[str, Any]] = []
    for index, heading in enumerate(headings):
        start = heading.start()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
        title = heading.group(2).strip()
        section_content = content[start:end].strip()
        sections.append(
            {
                "id": f"{source}#{title.lower().replace(' ', '-')}",
                "source": source,
                "heading": title,
                "content": section_content,
            }
        )
    return sections


def build_index(docs_dir: Path = DOCS_DIR, index_path: Path = INDEX_PATH) -> list[dict[str, Any]]:
    docs_dir.mkdir(parents=True, exist_ok=True)
    sections: list[dict[str, Any]] = []

    for markdown_file in sorted(docs_dir.glob("*.md")):
        content = markdown_file.read_text(encoding="utf-8")
        sections.extend(split_markdown_sections(content, markdown_file.name))

    KB_DIR.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(sections, ensure_ascii=False, indent=2), encoding="utf-8")
    return sections


def load_index(index_path: Path = INDEX_PATH) -> list[dict[str, Any]]:
    if not index_path.exists():
        return []
    return json.loads(index_path.read_text(encoding="utf-8"))


def rank_sections(question: str, sections: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
    query_terms = tokenize_meaningful(question)
    if not query_terms:
        return []

    document_frequencies = Counter()
    section_tokens: list[list[str]] = []
    for section in sections:
        tokens = tokenize_meaningful(section["content"])
        section_tokens.append(tokens)
        document_frequencies.update(set(tokens))

    ranked: list[dict[str, Any]] = []
    total_documents = max(len(sections), 1)
    query_counter = Counter(query_terms)

    for section, tokens in zip(sections, section_tokens):
        token_counter = Counter(tokens)
        score = 0.0
        for term, query_count in query_counter.items():
            if token_counter[term] == 0:
                continue
            inverse_document_frequency = math.log((1 + total_documents) / (1 + document_frequencies[term])) + 1
            score += query_count * token_counter[term] * inverse_document_frequency
        if score >= 2.0:
            ranked.append({**section, "score": round(score, 4)})

    return sorted(ranked, key=lambda section: section["score"], reverse=True)[:limit]


def extract_answer(question: str, sections: list[dict[str, Any]]) -> str:
    query_terms = set(tokenize_meaningful(question))
    if not query_terms:
        return "I cannot confirm the answer from the knowledge base."
    candidate_sentences: list[str] = []

    for section in sections:
        body = "\n".join(
            line.strip()
            for line in section["content"].splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
        sentences = re.split(r"(?<=[.!?])\s+", body)
        for sentence in sentences:
            if query_terms.intersection(tokenize(sentence)):
                cleaned = sentence.strip()
                if cleaned and cleaned not in candidate_sentences:
                    candidate_sentences.append(cleaned)
            if len(candidate_sentences) >= 3:
                break
        if len(candidate_sentences) >= 3:
            break

    if not candidate_sentences:
        return "I cannot confirm the answer from the knowledge base."

    return " ".join(candidate_sentences)
