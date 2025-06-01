import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage


dotenv.load_dotenv()

db_dir = os.path.join(os.getcwd(), "db")

openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

persistent_directory = os.path.join(db_dir, "chroma_db_openai")


def query_vector_store(query, search_type = "similarity", search_kwargs = {"k" : 5}) :
    store_name = "chroma_db_metadata"
    if os.path.exists(persistent_directory) : 
        print(f"----- Querying the Vectore Store {store_name} -----")
        db = Chroma(
            persist_directory = persistent_directory,
            embedding_function = openai_embeddings
        )
        retriever = db.as_retriever(
            search_type = search_type,
            search_kwargs = search_kwargs
        )
        relevant_docs = retriever.invoke(query)
        print(f"----- Relevant Documents for {store_name} -----")
        for i, doc in enumerate(relevant_docs, 1) : 
            print(f"Document {i} : {doc.page_content}")
            if doc.metadata : 
                print(f"Source : {doc.metadata.get("source", "Unknown")}\n")
        combined_input = (
            "Here are some documents that might help answer the question : "
            + query
            + "\n\n Relevant Documents:\n"
            + "\n\n".join([doc.page_content for doc in relevant_docs])
            + "\n\n Please provide an answer based only on the provided documents"
        )

        messages = [
            SystemMessage(content = "You are a helpful assistant"),
            HumanMessage(content = combined_input)
        ]
        model = ChatOpenAI()
        messages = model.invoke(messages)

        
        return messages.content
    else : 
        print(f"Vector store {store_name} does not exist.")