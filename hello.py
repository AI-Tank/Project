def hello(name):
    return f"{name}님 hello"

from query import query_vector_store

def chat() :
   while True : 
      query = input("Q: ")
      completion = query_vector_store(query)
      print(f"A: {completion}")