from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma

# Project root
ROOT = Path(__file__).resolve().parent.parent

# Knowledge base directory
KB_DIR = ROOT / "knowledge-base"

# Chroma database location
DB_DIR = ROOT / "vector_store"

loader = DirectoryLoader(
    KB_DIR,
    glob="**/*.md",
    loader_cls=TextLoader,
)

documents = loader.load()

print("=" * 60)
print("DOCUMENT LOADING")
print("=" * 60)

print(f"Documents Loaded: {len(documents)}")

print("\nFirst Document Metadata")

print(documents[0].metadata)

print("\nFirst 500 Characters\n")

print(documents[0].page_content[:500])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100,
)

chunks = text_splitter.split_documents(documents)

print("\n" + "=" * 60)
print("CHUNKING")
print("=" * 60)

print(f"Total Chunks: {len(chunks)}")

print("\nSample Chunk Metadata\n")

print(chunks[0].metadata)

print("\nChunk Text\n")

print(chunks[0].page_content)

print("\n" + "=" * 60)
print("LOADING EMBEDDING MODEL")
print("=" * 60)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded successfully!")

print("\n" + "=" * 60)
print("CREATING VECTOR DATABASE")
print("=" * 60)

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(DB_DIR)
)

print("Vector database created successfully!")

collection = vector_db.get()

print("\n" + "=" * 60)
print("VECTOR DATABASE")
print("=" * 60)

print(f"Total Stored Chunks: {len(collection['ids'])}")

print(f"Database Location: {DB_DIR}")