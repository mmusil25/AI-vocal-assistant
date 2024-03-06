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
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import pygame
#initialize the audio player
pygame.init()
#Speech recognition encoder
r = sr.Recognizer()

# Setup for Open AI chatbot
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

# download and load all TTS models
preload_models(text_use_gpu=True, coarse_use_gpu=True, fine_use_gpu=True, codec_use_gpu=True)

def listaudio_devices():
    return

def listen(source, recognizer=r):
    recognizer.adjust_for_ambient_noise(source, duration=0.2)
    print("Listening")
    audio2 = r.listen(source=source)
    MyText = r.recognize_google(audio2)
    MyText = MyText.lower()
    return MyText


def AI_response_to_speech(question):
    # use chat_model.predict to get the answer
    answer = chat_model.predict(question).strip()
    print(question)
    print(answer)
    return answer

def outputspeech(prompt, audio_name):
    audio_array = generate_audio(prompt, history_prompt="v2/en_speaker_3")
    # save audio to disk
    write_wav(audio_name, SAMPLE_RATE, audio_array)
    my_sound = pygame.mixer.Sound(audio_name)
    my_sound.play()
    return 

with sr.Microphone() as source2:
    i = 0
    while True:
        i = i + 1
        try:
            input = listen(source = source2, recognizer=r)
        except:
            continue
        print("Customer input " + input)
        ans = AI_response_to_speech(input)
        outputspeech(ans, "/audio/tempAudio" + str(i) + ".wav")




