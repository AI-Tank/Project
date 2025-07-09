import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from chromadb import PersistentClient
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain



dotenv.load_dotenv()

db_dir = os.path.join(os.getcwd(), "db")

openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

persistent_directory = os.path.join(db_dir, "chroma_db_openai")

def db_list() : 
    client = PersistentClient(path = persistent_directory)
    return [col.name for col in client.list_collections()]


def create_vector_store(file, embedding = openai_embeddings) :
    file_dir = os.path.join(os.getcwd(), "doctrine")
    loader = PyPDFLoader(os.path.join(file_dir, file))
    document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 300)
    texts = text_splitter.split_documents(document)
    file_name = os.path.splitext(os.path.basename(file))[0]

    if not file_name in db_list() :
        print(f"-----Creating Vector Store collection {file_name}-----")
        Chroma.from_documents(
            texts, embedding, persist_directory = persistent_directory, collection_name = file_name
        )
        print(f"-----Finished Creating Vector Store collection {file_name}-----")
    else :
        print(
            f"Vector Store collection {file_name} already exists. No need to Initialize"
        )


def query_vector_store(query, chat_history, dblist, search_type = "similarity", search_kwargs = {"k" : 5}) :

    store_name = "chroma_db_openai"


    if os.path.exists(persistent_directory) : 
        #print(f"----- Querying the Vectore Store {store_name} -----")
        model = ChatOpenAI()

        db = Chroma(
            persist_directory = persistent_directory,
            embedding_function = openai_embeddings
        )
        retriever = db.as_retriever(
            search_type = search_type,
            search_kwargs = search_kwargs
        )
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, just "
            "reformulate it if needed and otherwise return it as is")

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            model, retriever, contextualize_q_prompt
        )

        qa_system_prompt = (
            "You are an assistant for question-answering tasks. Use "
            "the following pieces of retrieved context to answer the "
            "question. If you don't know the answer, just say that you "
            "don't know. Use three sentences maximum and keep the answer "
            "concise."
            "\n\n"
            "{context}"
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )

        question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        
        result = rag_chain.invoke({"input" : query, "chat_history" : chat_history})


        '''
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
        '''
        
        return result['answer']
    else : 
        print(f"Vector store {store_name} does not exist.")