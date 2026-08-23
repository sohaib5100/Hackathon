import os
import warnings
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

warnings.filterwarnings("ignore")
load_dotenv(override=True)

# 1. Load Knowledge Base Document
loader = TextLoader("data/knowledge_base.txt", encoding="utf-8")
documents = loader.load()

# 2. Split Document into Chunks
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = text_splitter.split_documents(documents)

# 3. Local Free Embeddings Model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Create FAISS Vector Database
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 5. LLM Initialization
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

def ask_with_rag(query: str) -> str:
    # Relevant chunks search karein
    relevant_docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    
    prompt = f"""Use only the context provided below to answer the user question.
Context:
{context}

Question: {query}
Answer:"""

    response = llm.invoke([HumanMessage(content=prompt)])
    
    if isinstance(response.content, list):
        return "".join([b.get("text", "") for b in response.content if isinstance(b, dict)])
    return str(response.content)

if __name__ == "__main__":
    print("--- Testing Level 2 (RAG Search) ---")
    
    q1 = "Saylani ke head office ka address kya hai?"
    print(f"\nUser: {q1}")
    print(f"Bot: {ask_with_rag(q1)}")

    q2 = "Kya courses ki koi fees hoti hai?"
    print(f"\nUser: {q2}")
    print(f"Bot: {ask_with_rag(q2)}")