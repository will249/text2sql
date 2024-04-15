from langchain.schema import Document
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings


def embed():
  loader = TextLoader("../../seed_db.sql")
  documents = loader.load()

  splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
      chunk_size=500, chunk_overlap=200
  )
  all_splits = splitter.split_documents(documents)

  embedding = CohereEmbeddings()

  vectorstore = Chroma.from_documents(
      documents=all_splits,
      collection_name="db-metadata-embeddings",
      embedding=embedding,
  )
  return vectorstore

