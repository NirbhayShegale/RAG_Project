import cohere


def rerank_documents(query, documents):
    seen = set()
    deduped_docs = []
    for doc in documents:
        content = doc.page_content.strip()
        if content and content not in seen:
            seen.add(content)
            deduped_docs.append(doc)

    if not deduped_docs:
        raise ValueError("Retrieval returned no non-empty documents to rerank.")

    reranking_model = cohere.ClientV2()
    response = reranking_model.rerank(
        model="rerank-v3.5",
        query=query,
        # Cohere accepts text strings, not LangChain Document instances.
        documents=[doc.page_content for doc in deduped_docs],
        top_n=4,
    )

    reranked_docs = []

    for result in response.results:
        doc = deduped_docs[result.index]
        reranked_docs.append(doc)

    return reranked_docs, response
