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
import pyaudio
import wave
import soundfile

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

def list_devices():
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    for i in range(0, device_count):
        info = p.get_device_info_by_index(i)
        print("Device {} = {}".format(info["index"], info["name"]))

def list_input_devices(show=True):
    input_device_array=[]
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range (0,numdevices):
        if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                if show: print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
                input_device_array.append("Input Device id " + str(i) + " - " + p.get_device_info_by_host_api_device_index(0,i).get('name'))
    return input_device_array

def list_output_devices(show=True):
    output_device_array = []
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range (0,numdevices):
        if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                if show: print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
                output_device_array.append("Output Device id " + str(i) + " - " + p.get_device_info_by_host_api_device_index(0,i).get('name'))
    return output_device_array

def listen(source, recognizer=r, window=None):
    recognizer.adjust_for_ambient_noise(source, duration=0.2)
    print("Listening")
    if window is not None:
        window['-MLINE-'].update("\n" + "Listening" + "\n", append=True, autoscroll=True)
        window.refresh()
    audio2 = r.listen(source=source)
    MyText = r.recognize_google(audio2)
    MyText = MyText.lower()
    if window is not None:
        window['-MLINE-'].update("Customer input: " + MyText, append=True, autoscroll=True)
    return MyText

def AI_response_to_speech(question):
    # use chat_model.predict to get the answer
    answer = chat_model.predict(question).strip()
    print(question)
    print(answer)
    return answer

def get_first_integer(string):
    return integer

def pa_play_wav(filename, device = None):
    
    CHUNK = 1023
    data, samplerate = soundfile.read(filename)
    soundfile.write('new.wav', data, samplerate, subtype='PCM_16')

    with wave.open('new.wav', 'rb') as wf:
        # Instantiate PyAudio and initialize PortAudio system resources (1)
        p = pyaudio.PyAudio()

        # Open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Play samples from the wave file (3)
        while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
            stream.write(data)

        # Close stream (4)
        stream.close()

        # Release PortAudio system resources (5)
        p.terminate()

def outputspeech(prompt, audio_name):
    audio_array = generate_audio(prompt, history_prompt="v2/en_speaker_3")
    # save audio to disk
    write_wav(audio_name, SAMPLE_RATE, audio_array)
    pa_play_wav(audio_name)
    return 

if __name__ == "__main__":
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
            outputspeech(ans, "audio/tempAudio" + str(i) + ".wav")




