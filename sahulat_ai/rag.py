import os
from langchain_community.document_loaders import PyPDFDirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

DATA_DIR = "data/saylani_docs"
TXT_FILE = "data/knowledge_base.txt"

def initialize_rag():
    all_docs = []
    
    # 1. Load PDFs if present
    if os.path.exists(DATA_DIR) and os.listdir(DATA_DIR):
        pdf_loader = PyPDFDirectoryLoader(DATA_DIR)
        all_docs.extend(pdf_loader.load())

    # 2. Load Fallback Knowledge Base TXT
    if os.path.exists(TXT_FILE):
        txt_loader = TextLoader(TXT_FILE, encoding="utf-8")
        all_docs.extend(txt_loader.load())

    if not all_docs:
        print("[RAG]: Warning - No knowledge documents found.")
        return None

    # Smart Recursive Text Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(all_docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    return vectorstore.as_retriever(search_kwargs={"k": 3})








# import os
# from langchain_community.document_loaders import PyPDFDirectoryLoader
# from langchain_text_splitters import CharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings

# DATA_DIR = "data/saylani_docs"

# def initialize_rag():
#     if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
#         print("[RAG]: Warning - 'data/saylani_docs' folder is empty or missing.")
#         return None

#     loader = PyPDFDirectoryLoader(DATA_DIR)
#     documents = loader.load()

#     text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     docs = text_splitter.split_documents(documents)

#     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     vectorstore = FAISS.from_documents(docs, embeddings)
#     return vectorstore.as_retriever(search_kwargs={"k": 3})