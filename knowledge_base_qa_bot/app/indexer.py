import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs" / "sample"
KB_DIR = ROOT_DIR / ".kb"
INDEX_PATH = KB_DIR / "index.json"
TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "does",
    "for",
    "from",
    "he",
    "how",
    "i",
    "in",
    "is",
    "it",
    "my",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "what",
    "when",
    "who",
    "why",
    "with",
    "you",
    "your",
}


@dataclass
class Section:
    id: str
    source: str
    heading: str
    heading_path: list[str]
    content: str
    tokens: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "heading": self.heading,
            "heading_path": self.heading_path,
            "content": self.content,
            "tokens": self.tokens,
        }


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9_]+", "-", text.lower()).strip("-")
    return slug or "section"


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]


def tokenize_meaningful(text: str) -> list[str]:
    return [token for token in tokenize(text) if token not in STOPWORDS and len(token) > 1]


def parse_markdown_sections(content: str, source: str) -> list[Section]:
    sections: list[Section] = []
    heading_stack: list[tuple[int, str]] = []
    current_heading: str | None = None
    current_path: list[str] = []
    current_lines: list[str] = []

    def flush_section() -> None:
        if current_heading is None:
            return
        body = "\n".join(current_lines).strip()
        if not body:
            return
        heading_text = " ".join(current_path)
        sections.append(
            Section(
                id=f"{source}#{slugify(current_heading)}",
                source=source,
                heading=current_heading,
                heading_path=current_path.copy(),
                content=body,
                tokens=tokenize_meaningful(f"{heading_text}\n{body}"),
            )
        )

    for line in content.splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            flush_section()
            level = len(match.group(1))
            heading = match.group(2).strip()
            heading_stack = [
                (stack_level, stack_heading)
                for stack_level, stack_heading in heading_stack
                if stack_level < level
            ]
            heading_stack.append((level, heading))
            current_heading = heading
            current_path = [stack_heading for _, stack_heading in heading_stack]
            current_lines = []
            continue
        current_lines.append(line)

    flush_section()
    if sections:
        return sections

    body = content.strip()
    if not body:
        return []
    return [
        Section(
            id=f"{source}#document",
            source=source,
            heading="Document",
            heading_path=["Document"],
            content=body,
            tokens=tokenize_meaningful(body),
        )
    ]


def build_index(docs_dir: Path = DOCS_DIR, index_path: Path = INDEX_PATH) -> list[dict[str, Any]]:
    docs_dir.mkdir(parents=True, exist_ok=True)
    sections: list[Section] = []
    for markdown_file in sorted(docs_dir.glob("*.md")):
        sections.extend(parse_markdown_sections(markdown_file.read_text(encoding="utf-8"), markdown_file.name))

    payload = {
        "sections": [section.to_dict() for section in sections],
        "stats": build_stats(sections),
    }
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return [section.to_dict() for section in sections]


def load_index(index_path: Path = INDEX_PATH) -> list[dict[str, Any]]:
    if not index_path.exists():
        return []
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return payload.get("sections", [])


def build_stats(sections: list[Section]) -> dict[str, Any]:
    doc_freq = Counter()
    total_tokens = 0
    for section in sections:
        total_tokens += len(section.tokens)
        doc_freq.update(set(section.tokens))
    return {
        "files_indexed": len({section.source for section in sections}),
        "sections_indexed": len(sections),
        "avg_doc_len": total_tokens / len(sections) if sections else 0,
        "doc_freq": dict(sorted(doc_freq.items())),
    }


def list_documents(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    documents: dict[str, list[dict[str, str]]] = {}
    for section in sections:
        heading_path = section.get("heading_path") or [section["heading"]]
        documents.setdefault(section["source"], []).append(
            {
                "source": section.get("id", f"{section['source']}#{section['heading']}"),
                "heading": " > ".join(heading_path),
            }
        )
    return [
        {"file": file, "sections": file_sections}
        for file, file_sections in sorted(documents.items())
    ]


def rank_sections(question: str, sections: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
    query_terms = tokenize_meaningful(question)
    if not query_terms:
        return []

    section_tokens = [
        section.get("tokens") or tokenize_meaningful(f"{section.get('heading', '')}\n{section['content']}")
        for section in sections
    ]
    document_frequencies = Counter()
    for tokens in section_tokens:
        document_frequencies.update(set(tokens))

    total_documents = max(len(sections), 1)
    avg_doc_len = sum(len(tokens) for tokens in section_tokens) / total_documents
    query_counter = Counter(query_terms)
    ranked: list[dict[str, Any]] = []

    for section, tokens in zip(sections, section_tokens):
        token_counter = Counter(tokens)
        section_len = len(tokens) or 1
        score = 0.0
        for term, query_count in query_counter.items():
            term_frequency = token_counter[term]
            if term_frequency == 0:
                continue
            idf = math.log(1 + (total_documents - document_frequencies[term] + 0.5) / (document_frequencies[term] + 0.5))
            denominator = term_frequency + 1.5 * (1 - 0.75 + 0.75 * section_len / max(avg_doc_len, 1))
            score += query_count * idf * (term_frequency * 2.5) / denominator
        heading_tokens = set(tokenize_meaningful(" ".join(section.get("heading_path") or [section.get("heading", "")])))
        score += sum(1 for term in query_terms if term in heading_tokens) * 0.35
        if score > 0:
            ranked.append({**section, "score": round(score, 4)})

    return sorted(ranked, key=lambda section: section["score"], reverse=True)[:limit]
