from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

from src.Ingestion.run_ingestion import run_ingestion
from src.Ingestion.VectorDB import close_vector_store
from src.Config.models import get_llm
from src.Retrival.run_retrival import run_retrival


def main():
    vector_store = None

    try:
        vector_store, chunked_documents = run_ingestion("./knowledge-base", "my_collection")
        query = input("Ask a question: ").strip()

        if not query:
            return

        llm = get_llm()
        llm_response= run_retrival(query, vector_store, chunked_documents, llm)

        print("\nResponse from LLM:")
        print(llm_response)



    finally:
        if vector_store is not None:
            close_vector_store()

if __name__ == "__main__":
    main()
