from typing import List
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph
from graph.nodes.retriever import Retriever
from graph.nodes.grader import DocumentGrader
from graph.nodes.rewriter import QuestionRewriter
from graph.nodes.generator import Generator
from graph.edges.decide_to_generate import decide_to_generate
from graph.edges.evaluation import Evaluator

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        optimised_question: question optimised for vector search
        rewrite_question: str
        generation: LLM generation
        documents: list of documents 
    """
    question : str
    optimised_question: str
    rewrite_needed: str
    generation : str
    documents : List[str]



def compile():
  retriever = Retriever()
  grader = DocumentGrader()
  rewriter = QuestionRewriter()
  generator = Generator()
  evaluator = Evaluator()

  workflow = StateGraph(GraphState)

  # Define nodes
  workflow.add_node("retrieve", retriever.retrieve)
  workflow.add_node("grade_documents", grader.grade_documents)
  workflow.add_node("rewrite_question", rewriter.rewrite_question)
  workflow.add_node("generate", generator.generate)

  # Build graph
  workflow.set_entry_point("retrieve")
  workflow.add_edge("retrieve", "grade_documents")
  workflow.add_conditional_edges(
      "grade_documents",
      decide_to_generate,
      {
          "rewrite": "rewrite_question", # Failed grading => re-rewrite question
          "generate": "generate", 
      },
  )
  workflow.add_edge("rewrite_question", "retrieve")
  workflow.add_conditional_edges(
      "generate",
      evaluator.evaluate,
      {
          "fail": "generate", # Failed eval => re-generate 
          "success": END,
      },
  )

  # Compile and return
  app = workflow.compile()

  return app