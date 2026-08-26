from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {question}
""")

def llm_response(query, reranked_docs, llm):
    context = "\n\n".join(document.page_content for document in reranked_docs)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"context": context, "question": query})

    return response
