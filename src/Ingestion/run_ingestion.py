from .Chunking import split_documents
from .DocLoad import load_markdown_folder
from .VectorDB import create_vector_store


def run_ingestion(folder_path, collection_name):
    documents = load_markdown_folder(folder_path)
    chunked_documents = split_documents(documents)
    vector_store = create_vector_store(collection_name)
    vector_store.add_documents(chunked_documents)

    print(
        f"Ingestion completed. {len(chunked_documents)} documents added to "
        f"collection '{collection_name}'."
    )
    return vector_store, chunked_documents

