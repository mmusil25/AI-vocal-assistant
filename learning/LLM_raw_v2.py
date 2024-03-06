#main.ipynb
import os # for accessing environment variables
from abc import ABC, abstractmethod # abstract class, dont worry about this yet I will explain later in another article

# imports from langchain package
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from decouple import config



OPENAI_API_KEY = config("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=OPENAI_API_KEY) # Language Model
chat_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY) # Another LLM interface

question = "What is the meaning of life?"
# use llm.predict to get the answer
answer = llm.predict(question).strip()
print(question)
print(answer)
# use chat_model.predict to get the answer
answer = chat_model.predict(question).strip()
print(question)
print(answer)