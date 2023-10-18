import speech_recognition as sr
import pyttsx3

import os 
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

import openai
openai.api_key = OPENAI_KEY

# convert text to speech
def SpeakText(command):

  # Initialize engine
  engine = pyttsx3.init()
  engine.say(command)
  engine.runAndWait()

# Initialize recognizer
r = sr.Recognizer()

def record_text():
  # Loop in case of errors
  while(1):
    try:
      # Use microphone as input source
      with sr.Microphone() as source2:

        # Prepare recognizer for input
        r.adjust_for_ambient_noise(source2, duration=0.2)

        print("I'm listening")

        # Listen's for user input
        audio2 = r.listen(source2)

        # Use Google to recognize audio
        MyText = r.recognize_google(audio2)

        return MyText
      
    except sr.RequestError as e:
      print("Could not request results: {0}".format(e))

    except sr.UnknownValueError:
      print("Unknown error occured")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):

  response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5,
  )

  message = response.choices[0].message.content
  messages.append(response.choices[0].message)
  return message

messages = [{"role": "user", "content": "Please act like Jarvis from Iron Man."}]
while(1):
  text = record_text()
  messages.append({"role": "user", "content":text})
  response = send_to_chatGPT(messages)
  SpeakText(response)

  print(response)