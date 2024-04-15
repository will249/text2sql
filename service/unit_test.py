import json
from graph.compile import compile
import os
from dotenv import load_dotenv

load_dotenv()

# Get list of example questions
with open('./utils/example_questions.json', 'r') as file:
    data = json.load(file)
questions = data['questions']
# questions = ["Return the tail numbers of all aircraft whose model is '787'"]

graph = compile()

for question in questions:
  inputs = {"question": question}
  print(question)
  for s in graph.stream(inputs):
      for key, value in s.items():
         print('')

  print(s['generate']['generation'])
  # Check whether graph completed successfully
    # assert "END" in s   ## Todo: confirm how langchain streams indicate completion
      
