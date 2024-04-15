from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_cohere import ChatCohere
from langchain_core.output_parsers import StrOutputParser

class Generator:
    def __init__(self, generator_model='cohere'):
        if generator_model == 'openai':
            llm = ChatOpenAI(model="gpt-4", temperature=0)
        else:
            llm = ChatCohere(model_name="command-r", temperature=0)

        prompt = PromptTemplate(
            template="""You are a postgres expert. Use the following pieces of retrieved context (relevant DB tables) to generate a syntactically correct SQL query that answers the user's question. When creating location-based queries, use tables containing GIS objects as this permits highly optimised geo-spatial querying. Only return the SQL query, with no explanation or preamble. If you can't formulate a valid query, just say that you don't know. \n Here is the retrieved context: \n\n {documents} \n\n Here is the user question: {question} \n""",
            input_variables=["question", "documents"],
        )
        self.generation_chain = prompt | llm | StrOutputParser()

    def generate(self, state):
        print("---GENERATING---")
        question = state["question"]
        documents = state["documents"]
        if not isinstance(documents, list):
            documents = [documents]

        generation = self.generation_chain.invoke({"documents": documents, "question": question})
        return {"documents": documents, "question": question, "generation": generation}