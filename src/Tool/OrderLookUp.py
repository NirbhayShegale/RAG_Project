import json
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from src.Graph.state import RAGState
from src.Config.models import get_llm
from src.Config.logger import get_logger

log = get_logger(__name__)


class orderid(BaseModel):
    order_id: str | None

parser = PydanticOutputParser(pydantic_object=orderid)

prompt = ChatPromptTemplate.from_template(
"""
you are genius at extracting order numbers from text.
 
your job is to extract the order number from the sentence and return it in the following format:
text: "{query}"

if the order number is not present in the sentence, return None.

{format_instructions}
""")


def extract_order_id(query: str, llm):
    chain = prompt | llm | parser
    answer = chain.invoke({"query": query,"format_instructions": parser.get_format_instructions()})

    return answer.order_id

with open("data\\orders.json", "r") as file:
    data = json.load(file)
    
def get_order_details(order_id: str):
    for i, order in enumerate(data["orders"]):
        if order["order_id"] == order_id:
            return order
    return None


def order_lookup_tool(query: str, llm) -> dict | None:
    order_id = extract_order_id(query, llm)
    if order_id is None:
        return None

    order_details = get_order_details(order_id)
    return order_details

def run_order_lookup(state: RAGState):
    order_details = order_lookup_tool(state['Userquery'], get_llm())
    if order_details is not None:
        log.info(f"OrderLookup: found {order_details.get('order_id')} status={order_details.get('status')}")
        return {"Context": json.dumps(order_details)}
    else:
        log.info("OrderLookup: not found")
        return {"Context": "No order details found."}