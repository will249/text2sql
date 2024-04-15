from langchain.schema import Document
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings

class Retriever:
    def __init__(self):
      loader = TextLoader("seed_db.sql")
      documents = loader.load()

      splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
          chunk_size=500, chunk_overlap=200
      )
      all_splits = splitter.split_documents(documents)

      embedding = CohereEmbeddings()

      self.vectorstore = Chroma.from_documents(
          documents=all_splits,
          collection_name="db-metadata-embeddings",
          embedding=embedding,
      )

    def retrieve(self, state):
      print("---RETRIEVING---")
      print(state)
      retriever = self.vectorstore.as_retriever()
      
      if state['rewrite_needed'] == 'yes':
          question = state["optimised_question"]
      else: 
          question = state["question"]

      documents = retriever.invoke(question)
      return {"documents": documents}