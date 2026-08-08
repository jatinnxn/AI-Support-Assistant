from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

ROOT = Path(__file__).resolve().parent.parent

DB_DIR = ROOT / "vector_store"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory=str(DB_DIR),
    embedding_function=embeddings,
)

retriever = vector_db.as_retriever(
    search_kwargs={
        "k": 3
    }
)

def search_knowledge_base(query: str):

    results = retriever.invoke(query)

    return results

if __name__ == "__main__":

    query = input("Enter your query: ")

    results = search_knowledge_base(query)

    print("\n")

    print("=" * 60)

    print("TOP MATCHES")

    print("=" * 60)

    for index, doc in enumerate(results, start=1):

        print(f"\nMatch {index}")

        print("-" * 40)

        print("Source:")

        print(doc.metadata["source"])

        print()

        print(doc.page_content[:600])

        print("\n")