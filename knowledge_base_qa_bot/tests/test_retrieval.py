from app.retrieval import extract_answer, rank_sections, split_markdown_sections, tokenize, tokenize_meaningful


def test_tokenize_lowercases_words() -> None:
    assert tokenize("Hello, Retrieval!") == ["hello", "retrieval"]


def test_tokenize_meaningful_removes_stopwords() -> None:
    assert tokenize_meaningful("Who is he?") == []


def test_split_markdown_sections_uses_headings() -> None:
    sections = split_markdown_sections("# A\none\n\n## B\ntwo", "doc.md")

    assert [section["heading"] for section in sections] == ["A", "B"]


def test_rank_sections_returns_matching_section_first() -> None:
    sections = [
        {"source": "a.md", "heading": "A", "content": "Cats sleep."},
        {"source": "b.md", "heading": "B", "content": "Retrieval uses markdown sections."},
    ]

    ranked = rank_sections("markdown retrieval", sections)

    assert ranked[0]["source"] == "b.md"


def test_rank_sections_rejects_stopword_only_match() -> None:
    sections = [
        {"source": "a.md", "heading": "Pricing", "content": "The product is local and does not require paid APIs."}
    ]

    assert rank_sections("who is he?", sections) == []


def test_extract_answer_is_local_and_grounded() -> None:
    sections = [{"id": "doc.md#retrieval", "content": "Markdown KB retrieval indexes each heading section."}]

    assert extract_answer("How does retrieval work?", sections) == (
        "Markdown KB retrieval indexes each heading section. [doc.md#retrieval]"
    )
