

from dotenv import load_dotenv
load_dotenv()
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.tools import tool

# 🔧 Tools define karo (same jaisa pehle kiya tha)
@tool
def add_numbers(a: int, b: int) -> int:
    """Do numbers ko jodta hai (adds two numbers)"""
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Do numbers ko multiply karta hai"""
    return a * b

# 🤗 Free Hugging Face model use karo
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",  # free model
    task="text-generation",
    max_new_tokens=512,
    provider="auto",   # HF khud best free provider chunega
)

chat_model = ChatHuggingFace(llm=llm)

# Tools bind karo
llm_with_tools = chat_model.bind_tools([add_numbers, multiply_numbers])

response = llm_with_tools.invoke("7 aur 3 ko multiply karo")
print(response.tool_calls)