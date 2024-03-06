#main.ipynb
import os # for accessing environment variables
from abc import ABC, abstractmethod # abstract class, dont worry about this yet I will explain later in another article

# imports from langchain package
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from decouple import config
import speech_recognition as sr
import pyttsx3


r = sr.Recognizer()
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


OPENAI_API_KEY = config("OPENAI_API_KEY")
llm = OpenAI(openai_api_key=OPENAI_API_KEY) # Language Model
chat_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY) # Another LLM interface

with sr.Microphone() as source2:

    r.adjust_for_ambient_noise(source2, duration=0.2)
    print("Listening")
    audio2 = r.listen(source=source2)
    MyText = r.recognize_google(audio2)
    MyText = MyText.lower()

    print("Did you say " + MyText)
    #SpeakText(MyText)

    #question = "What is the meaning of life?"
    question = MyText
    # use llm.predict to get the answer
    answer = llm.predict(question).strip()
    print(question)
    print(answer)
    # use chat_model.predict to get the answer
    answer = chat_model.predict(question).strip()
    print(question)
    print(answer)