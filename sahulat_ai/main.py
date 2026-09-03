import os
import warnings
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

warnings.filterwarnings("ignore")
load_dotenv(override=True)

app = FastAPI(
    title="SahulatAI API with Memory",
    description="Saylani Welfare AI Agent with Session Memory",
    version="2.0.0"
)

# Schemas
class QueryRequest(BaseModel):
    session_id: str = "default_user"
    query: str

class QueryResponse(BaseModel):
    session_id: str
    query: str
    response: str

# In-memory session store for chat history
sessions_db: Dict[str, List] = {}

retriever = None
llm = None
SYSTEM_PROMPT = ""

@app.on_event("startup")
def startup_event():
    global retriever, llm, SYSTEM_PROMPT
    
    if os.path.exists("prompts/system_prompt.txt"):
        with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
            SYSTEM_PROMPT = f.read()
            
    if os.path.exists("data/knowledge_base.txt"):
        loader = TextLoader("data/knowledge_base.txt", encoding="utf-8")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
        docs = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )

@app.get("/")
def home():
    return {"status": "online", "message": "SahulatAI with Memory Running!"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    try:
        session_id = request.session_id
        if session_id not in sessions_db:
            sessions_db[session_id] = []

        # Retrieve RAG context
        context = ""
        if retriever:
            relevant_docs = retriever.invoke(request.query)
            context = "\n".join([doc.page_content for doc in relevant_docs])

        # Build message history payload
        messages = [SystemMessage(content=f"{SYSTEM_PROMPT}\n\nContext:\n{context}")]
        
        # Append previous conversation messages
        messages.extend(sessions_db[session_id])
        
        # Append current user query
        messages.append(HumanMessage(content=request.query))

        # Get response from model
        res = llm.invoke(messages)
        
        if isinstance(res.content, list):
            output_text = "".join([b.get("text", "") for b in res.content if isinstance(b, dict)])
        else:
            output_text = str(res.content)

        # Update in-memory chat history
        sessions_db[session_id].append(HumanMessage(content=request.query))
        sessions_db[session_id].append(AIMessage(content=output_text))

        return QueryResponse(session_id=session_id, query=request.query, response=output_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))














# import os
# import warnings
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from dotenv import load_dotenv

# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import CharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import SystemMessage, HumanMessage

# warnings.filterwarnings("ignore")
# load_dotenv(override=True)

# # FastAPI App Setup
# app = FastAPI(
#     title="SahulatAI API",
#     description="Saylani Welfare AI Customer Support Agent",
#     version="1.0.0"
# )

# # Request & Response Schemas
# class QueryRequest(BaseModel):
#     query: str

# class QueryResponse(BaseModel):
#     query: str
#     response: str

# # Global Variables Initialization
# retriever = None
# llm = None
# SYSTEM_PROMPT = ""

# @app.on_event("startup")
# def startup_event():
#     global retriever, llm, SYSTEM_PROMPT
    
#     # Load System Prompt
#     if os.path.exists("prompts/system_prompt.txt"):
#         with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
#             SYSTEM_PROMPT = f.read()
            
#     # Load Knowledge Base & VectorDB
#     if os.path.exists("data/knowledge_base.txt"):
#         loader = TextLoader("data/knowledge_base.txt", encoding="utf-8")
#         documents = loader.load()
#         text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
#         docs = text_splitter.split_documents(documents)
#         embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#         vectorstore = FAISS.from_documents(docs, embeddings)
#         retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

#     # LLM Init
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-3.6-flash",
#         google_api_key=os.getenv("GEMINI_API_KEY"),
#         temperature=0
#     )

# @app.get("/")
# def home():
#     return {"status": "online", "message": "SahulatAI Backend Running Successfully!"}

# @app.post("/ask", response_model=QueryResponse)
# def ask_question(request: QueryRequest):
#     if not request.query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
#     try:
#         # Step 1: Retrieve context
#         context = ""
#         if retriever:
#             relevant_docs = retriever.invoke(request.query)
#             context = "\n".join([doc.page_content for doc in relevant_docs])
        
#         # Step 2: Formulate Prompt
#         formatted_prompt = f"""{SYSTEM_PROMPT}

# Context:
# {context}

# User Question: {request.query}
# Answer:"""  

#         # Step 3: Invoke LLM
#         res = llm.invoke([HumanMessage(content=formatted_prompt)])
        
#         # Format Response Output
#         if isinstance(res.content, list):
#             output_text = "".join([b.get("text", "") for b in res.content if isinstance(b, dict)])
#         else:
#             output_text = str(res.content)

#         return QueryResponse(query=request.query, response=output_text)

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
