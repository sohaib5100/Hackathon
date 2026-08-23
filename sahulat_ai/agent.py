import os
from typing import Dict, List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from rag import initialize_rag

load_dotenv(override=True)

# System Prompt Load
SYSTEM_PROMPT = ""
if os.path.exists("prompts/system_prompt.txt"):
    with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()

# Models & Retrives Init
retriever = initialize_rag()
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

# In-Memory Store
sessions_db: Dict[str, List] = {}

def get_agent_response(session_id: str, user_query: str) -> str:
    if session_id not in sessions_db:
        sessions_db[session_id] = []

    context = ""
    if retriever:
        docs = retriever.invoke(user_query)
        context = "\n\n".join([d.page_content for d in docs])

    messages = [SystemMessage(content=f"{SYSTEM_PROMPT}\n\nRetrieved Documents:\n{context}")]
    messages.extend(sessions_db[session_id])
    messages.append(HumanMessage(content=user_query))

    res = llm.invoke(messages)

    if isinstance(res.content, list):
        output = "".join([b.get("text", "") for b in res.content if isinstance(b, dict)])
    else:
        output = str(res.content)

    sessions_db[session_id].append(HumanMessage(content=user_query))
    sessions_db[session_id].append(AIMessage(content=output))

    return output