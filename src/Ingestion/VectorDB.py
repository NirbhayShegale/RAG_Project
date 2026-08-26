from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_huggingface import HuggingFaceEndpointEmbeddings

embeddings = HuggingFaceEndpointEmbeddings(
    model="BAAI/bge-m3"
)

client = QdrantClient(path="qdrant.db")


def create_vector_store(collection_name):

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
    )

    vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings,
    )

    return vector_store


def close_vector_store():
    """Release the local Qdrant database before Python shuts down."""
    client.close()
