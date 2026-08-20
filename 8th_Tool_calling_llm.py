from langchain_core.tools import tool 
from langchain_anthropic import ChatAnthropic


# Tool define karo bss ek function pr tool laga doo 

@tool

def add_numbers( a: int , b : int ) -> int :
    """do numbers ko jodta hai (adds two number )"""
    return a + b 


@tool 

def Multiply_number(a : int , b : int ) -> int : 
    """ do numbers ko multiply karta hai (Multiply two number )"""

    return a * b 


#  LLm ko batao ki ye tools avalable hai 
 
llm  = ChatAnthropic (model = "claud-sonnet-4-6")
llm_with_tools  = llm.bind_tools([add_numbers,Multiply_number])

response = llm_with_tools.invoke ("5 and 10 ko multiply karo ")

print (response.tool_calls)




