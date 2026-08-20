#  TypedDict VS Pydentic sew State Define karna 


# AAb tkk use kara 

from typing import TypedDict

class MyState(TypedDict):
    message: str 
    count : int 


# Isme ek kami hai agar tumne galti sew count mai string dal di toh bhi ye chal jayega jo badme error de sakta hai 


# New method  Production level ke liye. 

from pydantic import BaseModel

class Mystate(BaseModel):
    message: str
    count : int 

# Isme aab agar koi node count main string dalne ki koshish karega toh isme error aa jayega that's it.