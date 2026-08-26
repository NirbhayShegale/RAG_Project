from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

def split_documents(documents):

    split = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    return split.split_documents(documents)