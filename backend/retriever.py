from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

class Retriever:
    def __init__(self, url):
        self.url = url
        self.loader = WebBaseLoader(self.url)
        self.embeddings = OpenAIEmbeddings()

    def load_and_split(self):
        documents = self.loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        return docs

    def build_vector_store(self, docs):
        vector_store = FAISS.from_documents(docs, self.embeddings)
        return vector_store

    def get_relevant_info(self, query, vector_store):
        results = vector_store.similarity_search(query)
        return results
