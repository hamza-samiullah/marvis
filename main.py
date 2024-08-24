import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os


recognizer = sr.Recognizer()
engine = pyttsx3.init()

#NEWSAPI Key here
API_KEY = "NEWS_API_KEY"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Initialize pygame mixer
    pygame.mixer.init()


    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")  # Replace with your MP3 file path

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Check every 10 milliseconds
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    #Openai API Key here!
    client = OpenAI(api_key="YOU_API_KEY")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant named as Marvis. Just like Alexa and google cloud."},
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return print(completion.choices[0].message.content)


def ProcessCommand(command):
    if "open google" in command.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://www.facebook.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)

    elif "news" in command.lower():
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=pk&category=business&apiKey={API_KEY}")
        if response.status_code == 200:
            data = response.json()

            # Extract and print the titles of the articles
            articles = data.get('articles', [])
            for i, article in enumerate(articles):
                speak(article['title'])

        speak("Here are the latest news")
    else:
        output = aiProcess(command)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Marvis...")
    # obtain audio from the microphone
    while True:
        r = sr.Recognizer()
        # recognize speech using google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
            print("Recognizing...")
            word = r.recognize_google(audio)
            if(word.lower() == "Marvis"):
                print("Yah")
                with sr.Microphone() as source:
                    print("Listening...")
                    c_audio = r.listen(source, timeout=3, phrase_time_limit=2)
                    command = r.recognize_google(c_audio)
                    ProcessCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
