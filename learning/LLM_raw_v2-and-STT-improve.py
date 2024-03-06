from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from decouple import config
import speech_recognition as sr
import pyttsx3
import time
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from decouple import config
from langchain.memory import ConversationBufferWindowMemory

r = sr.Recognizer()
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""You are a very professional AI customer service bot. You are
    currently having a conversation with a human. Answer the questions
    in a kind and friendly tone without a sense of humor.
    
    chat_history: {chat_history},
    Human: {question}
    AI:"""
)

chat_model = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY")) # Another LLM interface
memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)
llm_chain = LLMChain(
    llm=chat_model,
    memory=memory,
    prompt=prompt
)
with sr.Microphone() as source2:

    r.adjust_for_ambient_noise(source2, duration=0.2)
    print("Listening")
    audio2 = r.listen(source=source2)
    MyText = r.recognize_google(audio2)
    MyText = MyText.lower()

    print("Did you say " + MyText)

    question = MyText
    # use chat_model.predict to get the answer
    answer = chat_model.predict(question).strip()
    print(question)
    print(answer)