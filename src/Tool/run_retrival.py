from ..Retrival.QueryEnhancer import HYDE
from ..Retrival.Reranker import rerank_documents
from ..Retrival.RetrivalStrat import create_retriever
from ..Graph.state import RAGState
from ..Config.models import get_llm
from ..Config.logger import get_logger
from langchain_core.runnables import RunnableConfig

log = get_logger(__name__)


def retrival(query, vector_store, chunked_documents):
    llm = get_llm()
    enhanced_query = HYDE(query, llm)
    log.debug(f"HYDE: '{query}' -> '{enhanced_query}'")

    retriever = create_retriever(vector_store, chunked_documents, llm)
    retrieved_docs = retriever.invoke(enhanced_query)

    reranked_docs, rerank_response = rerank_documents(enhanced_query, retrieved_docs)

    log.info(f"Retrieved {len(retrieved_docs)} docs -> reranked to {len(reranked_docs)}")
    for i, doc in enumerate(reranked_docs):
        score = round(rerank_response.results[i].relevance_score, 4)
        src = doc.metadata.get("source", "unknown")
        log.info(f"  [{i+1}] score={score}  src={src}")

    return reranked_docs


def run_retrival(state: RAGState, config: RunnableConfig):
    cfg = config.get("configurable", {})
    vector_store = cfg["vector_store"]
    chunked_documents = cfg["chunked_documents"]

    reranked_docs = retrival(state['Userquery'], vector_store, chunked_documents)
    context_str = "\n\n".join(doc.page_content for doc in reranked_docs)
    log.info(f"Context built: {len(context_str)} chars")
    return {"Context": context_str}