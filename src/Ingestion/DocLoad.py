from pathlib import Path
import frontmatter
from langchain_core.documents import Document
from langchain_core.documents import Document

def load_markdown_folder(folder_path):
    Temp = []
    for file_path in Path(folder_path).rglob("*.md"):   

        post = frontmatter.load(file_path)

        metadata = dict(post.metadata)

        content = post.content

        Temp.append({
            "content": content,
            "metadata": {
                **metadata,
                "source": str(file_path),
                "file_name": file_path.name,
                "file_type": "markdown"
            }
        })

    final_documents = []
    for doc in Temp:
        final_documents.append(
            Document(
                page_content=doc["content"],
                metadata=doc["metadata"]
            )
        )

    return final_documents

# documents = load_markdown_folder("./knowledge-base")

