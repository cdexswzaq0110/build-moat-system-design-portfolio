import re
from typing import Any

from .indexer import (
    DOCS_DIR,
    INDEX_PATH,
    build_index,
    list_documents,
    load_index,
    parse_markdown_sections,
    rank_sections,
    tokenize,
    tokenize_meaningful,
)


def split_markdown_sections(content: str, source: str) -> list[dict[str, Any]]:
    return [
        {
            "id": section.id,
            "source": section.source,
            "heading": section.heading,
            "heading_path": section.heading_path,
            "content": section.content,
            "tokens": section.tokens,
        }
        for section in parse_markdown_sections(content, source)
    ]


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

    source_ids = [
        section.get("id") or f"{section.get('source', 'source')}#{section.get('heading', 'section')}"
        for section in sections
    ]
    answer = " ".join(candidate_sentences)
    if source_ids and not any(source_id in answer for source_id in source_ids):
        answer = f"{answer} [{source_ids[0]}]"
    return answer
