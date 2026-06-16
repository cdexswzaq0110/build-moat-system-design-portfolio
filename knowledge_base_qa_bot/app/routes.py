from fastapi import APIRouter

from .retrieval import (
    DOCS_DIR,
    INDEX_PATH,
    build_index,
    extract_answer,
    list_documents,
    load_index,
    rank_sections,
)
from .schemas import ChatRequest, ChatResponse, DocumentsResponse, IndexResponse, Source


router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/metadata")
def metadata() -> dict:
    documents = [path.name for path in sorted(DOCS_DIR.glob("*.md"))] if DOCS_DIR.exists() else []
    sections = load_index()
    return {
        "documents": documents,
        "indexed_sections": len(sections),
        "index_exists": INDEX_PATH.exists(),
    }


@router.get("/documents", response_model=DocumentsResponse)
def documents() -> DocumentsResponse:
    sections = load_index()
    document_list = list_documents(sections)
    return DocumentsResponse(
        files_indexed=len(document_list),
        sections_indexed=len(sections),
        documents=document_list,
    )


@router.post("/index", response_model=IndexResponse)
def index_documents() -> IndexResponse:
    sections = build_index()
    return IndexResponse(status="indexed", count=len(sections))


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    sections = load_index()
    if not sections:
        return ChatResponse(answer="Knowledge base is empty. Run /index first.", sources=[])

    ranked_sections = rank_sections(request.question, sections)
    if not ranked_sections:
        return ChatResponse(answer="I cannot confirm the answer from the knowledge base.", sources=[])

    answer = extract_answer(request.question, ranked_sections)
    sources = [
        Source(
            source=section.get("id", section["source"]),
            heading=" > ".join(section.get("heading_path") or [section["heading"]]),
            score=section["score"],
            content=section["content"][:240],
        )
        for section in ranked_sections
    ]
    learning_focus = (
        f"Strongest match: {sources[0].heading} (score {sources[0].score})."
        if sources
        else ""
    )
    return ChatResponse(answer=answer, sources=sources, learning_focus=learning_focus)
