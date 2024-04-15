def decide_to_generate(state):

    print("---ASSESS GRADED DOCUMENTS---")
    question = state["question"]
    rewrite_needed = state["rewrite_needed"]
    documents = state["documents"]

    if rewrite_needed == "yes":
        print("------decision: No documents relevant to question, rewriting---")
        return "rewrite"
    else:
        print("------decision: Generate---")
        return "generate"