import os
import warnings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

import model

# Suppress specific warning
warnings.filterwarnings("ignore", message="Streaming with Pydantic response_format not yet supported.")

load_dotenv()  # This loads the environment variables from .env

#model = "gpt-3.5-turbo"
#model = 'gpt-4-turbo-preview'
model = "gpt-4o-mini"

llm = ChatOpenAI(model=model)
structured_llms = dict()

def model_for(output_type: type):
    return structured_llms.setdefault(output_type.__name__, llm.with_structured_output(output_type, method="json_schema"))

def ask(prompt, conversation=None, output_type=None):
    m = ("human", prompt)
    if conversation is None:
        messages = [m]
    else:
        conversation.append(m)
        messages = conversation
    
    if output_type is not None:
        m = model_for(output_type) 
        response = m.invoke(messages)

        if conversation != None:
            conversation.append(str(response))
        return response
    else:
        response = llm.invoke(messages)
        if conversation != None:
            conversation.append(response)
        return response.content
