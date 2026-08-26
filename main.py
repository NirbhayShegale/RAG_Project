from dotenv import load_dotenv
import uuid
load_dotenv()

from src.Ingestion.run_ingestion import run_ingestion
from src.Ingestion.VectorDB import close_vector_store
from src.Graph.state import RAGState
from src.Graph.graph import workflow


def main():
    vector_store = None

    try:
        vector_store, chunked_documents = run_ingestion("./knowledge-base", "my_collection")

        thread_id = str(uuid.uuid4())
        config = {
            "configurable": {
                "thread_id": thread_id,
                "vector_store": vector_store,
                "chunked_documents": chunked_documents,
            }
        }
        first_turn = True

        while True:
            query = input("You: ").strip()

            if not query:
                continue
            if query.lower() in ("quit", "exit", "q"):
                break

            if first_turn:
                turn_input: RAGState = {"Userquery": query, "messages": []}
                first_turn = False
            else:
                turn_input = {"Userquery": query}

            final_state = workflow.invoke(turn_input, config=config)
            print(f"AI:{final_state['response'].content}\n")

    finally:
        if vector_store is not None:
            close_vector_store()


if __name__ == "__main__":
    main()
