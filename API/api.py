import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

from src.Ingestion.VectorDB import close_vector_store
from src.Ingestion.run_ingestion import run_ingestion
from src.Graph.graph import workflow
from src.Graph.state import RAGState


class ChatRequest(BaseModel):
    query: str = Field(min_length=1)
    session_id: str | None = None  


class ChatResponse(BaseModel):
    answer: str
    session_id: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    project_root = Path(__file__).resolve().parents[1]
    app.state.vector_store, app.state.chunked_documents = run_ingestion(
        project_root / "knowledge-base", "my_collection"
    )
    yield
    close_vector_store()


app = FastAPI(title="Aria API", lifespan=lifespan)


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    session_id = req.session_id or str(uuid.uuid4())

    config = {"configurable": {
        "thread_id": session_id,
        "vector_store": app.state.vector_store,
        "chunked_documents": app.state.chunked_documents,
    }}

    turn: RAGState = (
        {"Userquery": req.query, "messages": []}
        if req.session_id is None
        else {"Userquery": req.query}
    )

    try:
        state = workflow.invoke(turn, config=config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return ChatResponse(answer=state["response"].content, session_id=session_id)

