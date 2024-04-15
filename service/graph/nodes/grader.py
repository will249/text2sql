from langchain_cohere import ChatCohere
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")

class DocumentGrader:
    def __init__(self):
        preamble = """You are a grader assessing relevance of a retrieved document to a user question. \n If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
        llm = ChatCohere(model="command-r", temperature=0)
        structured_llm_grader = llm.with_structured_output(
            GradeDocuments, preamble=preamble
        )
        grade_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "human",
                    "Retrieved document: \n\n {document} \n\n User question: {question}",
                )
            ]
        )
        self.retrieval_grader = grade_prompt | structured_llm_grader

    def grade_documents(self, state):
        print("---CHECKING DOCUMENT RELEVANCE---")
        question = state["question"]
        documents = state["documents"]
        
        # Filter for relevant docs
        filtered_docs = []
        rewrite_needed = "no"
        for i, d in enumerate(documents):
            grade = self.retrieval_grader.invoke(
                {"question": question, "document": d.page_content}
            ).binary_score
            if grade == "yes":
                print(f"------grader: document {i+1} relevant---")
                filtered_docs.append(d)
            else:
                print(f"------grader: document {i+1} not relevant---")
        if len(filtered_docs) == 0:
            rewrite_needed = "yes"
        return {"documents": filtered_docs, "rewrite_needed": rewrite_needed}