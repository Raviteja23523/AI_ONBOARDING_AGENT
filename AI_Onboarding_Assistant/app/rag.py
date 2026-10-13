from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def build_retriever():

    documents = []

    data_path = Path(__file__).resolve().parent.parent / "data"

    for file in data_path.glob("*.md"):
        loader = TextLoader(str(file), encoding="utf-8")
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

