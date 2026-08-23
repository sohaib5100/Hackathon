import os
import warnings
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# Hide warning noise
warnings.filterwarnings("ignore")
load_dotenv(override=True)

with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

def ask_sahulat(user_query: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_query)
    ]
    response = llm.invoke(messages)
    
    # Extract plain text if response returns a list structure
    if isinstance(response.content, list):
        return "".join([block.get("text", "") for block in response.content if isinstance(block, dict)])
    return str(response.content)

if __name__ == "__main__":
    print("--- Testing Level 1 (Clean Output) ---")
    
    print("\n[Q1 Roman Urdu]: Saylani ke kon kon se courses hain?")
    print("[A1]:\n", ask_sahulat("Saylani ke kon kon se courses hain?"))
    
    print("\n" + "="*50)
    
    print("\n[Q2 Out-of-Scope]: Write me a poem about cricket.")
    print("[A2]:\n", ask_sahulat("Write me a poem about cricket."))





# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import SystemMessage, HumanMessage

# load_dotenv(override=True)

# with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
#     SYSTEM_PROMPT = f.read()

# # Using gemini-3.6-flash endpoint
# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.6-flash",
#     google_api_key=os.getenv("GEMINI_API_KEY"),
#     temperature=0
# )

# def ask_sahulat(user_query: str):
#     messages = [
#         SystemMessage(content=SYSTEM_PROMPT),
#         HumanMessage(content=user_query)
#     ]
#     response = llm.invoke(messages)
#     return response.content

# if __name__ == "__main__":
#     print("--- Testing Level 1 ---")
    
#     print("\n[Q1 Roman Urdu]: Saylani ke kon kon se courses hain?")
#     print("[A1]:", ask_sahulat("Saylani ke kon kon se courses hain?"))
    
#     print("\n[Q2 Out-of-Scope]: Write me a poem about cricket.")
#     print("[A2]:", ask_sahulat("Write me a poem about cricket."))