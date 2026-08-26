from langchain_core.messages import HumanMessage, SystemMessage

def HYDE(query, llm):
    messages = [
        SystemMessage(content="""You are generating a hypothetical document to improve retrieval for a search system.
        Given the following question, write a short passage that would plausibly contain the answer.
        Write it as if it were an excerpt from a real document (e.g. a research paper, article, or technical report) — not as a direct answer to the question, and not addressed to the reader.
        Do not hedge, do not say "I don't know," and do not include disclaimers.
        Write confidently, using domain-appropriate terminology, even if some details are invented.
        Keep it to 3-5 sentences."""),
        HumanMessage(content=query)
    ]
    response = llm.invoke(messages)
    return response.content