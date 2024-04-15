from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

class QuestionRewriter:
    def __init__(self):
        preamble = """You are an expert at re-writing questions so that they are optimized \n for vectorstore retrieval. Take the original question and create an improved question. \n """
        llm = ChatCohere(model="command-r", temperature=0).bind(preamble=preamble)
        rewrite_prompt = lambda x: ChatPromptTemplate.from_messages(
            [HumanMessage(f"Original question: {x['question']} \nNew question: ")]
        )
        self.question_rewriter = rewrite_prompt | llm | StrOutputParser()

    def rewrite_question(self, state):
        print("---REWRITING QUESTION---")
        question = state["question"]
        optimised_question = self.question_rewriter.invoke({"question": question})
        return {"optimised_question": optimised_question}