import json
import os
from typing import Dict
from graph.compile import compile

import requests
import config
import os

def handler(event, context): 
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
    get_api_keys()
    print(os.environ['LANGCHAIN_API_KEY'])

    print(f"event is {event}")
    body = event["body"]
    
    validate_response = validate_inputs(body)
    if validate_response:
        return validate_response
    
    prompt = body['prompt']

    print(f"prompt is {prompt}")

    graph = compile()

    # Run
    inputs = {"question": prompt}
    for s in graph.stream(inputs):
      for key, value in s.items():
          print(f"(Node: '{key}')")

    if s["generate"]["generation"]:
        return build_response(
            {
                "status": "success",
                "message": s["generate"]["generation"]
            })
    else:
        return build_response(
            {
                "status": "error",
                "message": "Error during generation"
            })    


def validate_inputs(body: Dict):
    for input_name in ['prompt']:
        if input_name not in body:
            return build_response({
                "status": "error",
                "message": f"{input_name} missing in payload"
            })
    return ""

def build_response(body: Dict):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def get_api_keys():
    """Fetches the api keys saved in Secrets Manager"""

    headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
    secrets_extension_endpoint = "http://localhost:2773" + \
    "/secretsmanager/get?secretId=" + \
    config.config.API_KEYS_SECRET_NAME
  
    r = requests.get(secrets_extension_endpoint, headers=headers)
    secret = json.loads(json.loads(r.text)["SecretString"])

    os.environ['LANGCHAIN_API_KEY'] = secret['LANGCHAIN_API_KEY']
    os.environ['COHERE_API_KEY'] = secret['COHERE_API_KEY']
    os.environ['OPENAI_API_KEY'] = secret['OPENAI_API_KEY']

    return
