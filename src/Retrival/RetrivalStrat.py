from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever, MultiQueryRetriever

def create_retriever(vector_store, chunked_documents, llm, k=3):
    bm25_retriever = BM25Retriever.from_documents(chunked_documents, k=k)
    retriever = vector_store.as_retriever(search_kwargs={"k": k})

    ensemble_retriever = EnsembleRetriever(retrievers=[retriever, bm25_retriever], weights=[0.5, 0.5])

    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=ensemble_retriever,
        llm=llm
    )
    
    return multi_query_retriever