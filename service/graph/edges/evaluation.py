from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

class ValidityEval(BaseModel):
    """Binary score for validity of generated SQL query."""
    binary_score: str = Field(description="Generated query is valid SQL, 'yes' or 'no'")

class AnswerEval(BaseModel):
    """Binary score to assess whether generated SQL query answers the user's question."""
    binary_score: str = Field(description="Generated query addresses the question, 'yes' or 'no'")

class IdempEval(BaseModel):
    """Binary score for whether SQL query is idempotent."""
    binary_score: str = Field(description="Generated query is idempotent, 'yes' or 'no'")

class Evaluator:
    def __init__(self):
        self.llm = ChatCohere(model="command-r", temperature=0)

        preamble = """You are a SQL expert assessing the validity of a SQL query generated from text. If the query parses as valid SQL, give a binary score of 'yes', otherwise give a binary score 'no'. Provide the binary score as JSON with a single key 'score' and no explanation."""
        self.structured_evaluator = self.llm.with_structured_output(ValidityEval, preamble=preamble)
        validity_prompt = ChatPromptTemplate.from_messages([("human", "Generated SQL query: \n\n {generation}")])
        self.validity_evaluator = validity_prompt | self.structured_evaluator

        preamble = """You are a SQL expert that can determine whether a SQL query addresses / resolves a question \n Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question. \n Provide the binary score as JSON with a single key 'score' and no explanation."""
        self.structured_evaluator = self.llm.with_structured_output(AnswerEval, preamble=preamble)
        answer_prompt = ChatPromptTemplate.from_messages([("human", "User question: \n\n {question} \n\n Generated SQL query: \n\n {generation}")])
        self.answer_evaluator = answer_prompt | self.structured_evaluator

        preamble = """You are a SQL expert assessing whether a generated SQL query permanently \n alters the database. (i.e. whether it deletes, inserts, or updates entries in database tables, or deletes tables). \n Permit JOINS and string functions that only temporarily alter the data returned by the query). \n If the query does indeed leave the data unchanged, give a binary score of 'yes', otherwise give a binary score 'no'. Provide the binary score as JSON with a single key 'score' and no explanation."""
        self.structured_evaluator = self.llm.with_structured_output(IdempEval, preamble=preamble)
        idemp_prompt = ChatPromptTemplate.from_messages([("human", "Generated SQL query: \n\n {generation}")])
        self.idemp_evaluator = idemp_prompt | self.structured_evaluator

    def evaluate(self, state):
        print("---EVALUATING GENERATION---")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]

        if self.validity_evaluator.invoke({"generation": generation}).binary_score == "yes":
            print("------decision: query is valid sql---")
        else:
            print("------decision: query is not valid sql---")
            print(generation)
            return "fail"

        if self.answer_evaluator.invoke({"question": question, "generation": generation}).binary_score == "yes":
            print("------decision: query answers user's question---")
        else:
            print("------decision: query does not answer user's question---")
            print(generation)
            return "fail"

        if self.idemp_evaluator.invoke({"generation": generation}).binary_score == "yes":
            print("------decision: query is idempotent---")
        else:
            print("------decision: query is not idempotent---")
            print(generation)
            return "fail"

        return "success"