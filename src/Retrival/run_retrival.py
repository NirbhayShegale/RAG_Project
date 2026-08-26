from .QueryEnhancer import HYDE
from .Reranker import rerank_documents
from .RetrivalStrat import create_retriever
from .llmResponse import llm_response as generate_response

def run_retrival(query, vector_store, chunked_documents, llm):

    enhanced_query = HYDE(query, llm)

    retriever = create_retriever(vector_store, chunked_documents, llm)

    retrieved_docs = retriever.invoke(enhanced_query)

    reranked_docs,_ = rerank_documents(enhanced_query, retrieved_docs)

    response = generate_response(query, reranked_docs, llm)

    return response
