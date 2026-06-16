from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)


class Source(BaseModel):
    source: str
    heading: str
    score: float
    content: str = ""


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    learning_focus: str = ""


class IndexResponse(BaseModel):
    status: str
    count: int


class DocumentSection(BaseModel):
    source: str
    heading: str


class DocumentInfo(BaseModel):
    file: str
    sections: list[DocumentSection]


class DocumentsResponse(BaseModel):
    files_indexed: int
    sections_indexed: int
    documents: list[DocumentInfo]
