#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import libraries needed
import speech_recognition as sr
import math
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
from Adafruit_IO import Client, Feed, RequestError
import json
import requests


# In[2]:


engine = pyttsx3.init('sapi5')       #sapi5 is the text to speech engine for Microsoft
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) #Here 0 is for MALE voice and 1 is for FEMALE voice


# In[3]:


#Function which speaks whatever the information is given to it
def speak(text):
    engine.say(text)
    engine.runAndWait()


# In[4]:


#This function defines how to greet user based upon the current time 
def greeting():
    hour = datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good Morning Sir")
        print("Good Morning Sir")
    elif hour>=12 and hour<16:
        speak("Good afternoon Sir")
        print("Good afternoon Sir")
    else :
        speak("Good Evening Sir")
        print("Good Evening Sir")


# In[5]:


#The command function that listens to the user input
def command():
    global elapsed_time
    recognize = sr.Recognizer()
    with sr.Microphone() as source:
        start_time = time.time()
        print("Listening....")
        audio = recognize.listen(source)
        try:
            statement = recognize.recognize_google(audio,language = 'en-in')
            print(f"user said:{statement}\n")
        except Exception as exp:
            elapsed_time = time.time() - start_time
            speak("I didn't quite get that kindly repeat")
            return "None"
        return statement    


# In[6]:


#This function is for setting up the remote control of light
def setuplight():
    global digital
    global aio
    
    ADAFRUIT_IO_USERNAME = "sankalp_21878"
    ADAFRUIT_IO_KEY = "aio_rpYR85vs9ojkcE6H2OzKYU3deTmH"
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    try: # if we have a 'digital' feed
        digital = aio.feeds('led')
    except RequestError: # create a digital feed
        feed = Feed(name="digital")
        digital = aio.create_feed(feed)


# In[7]:


#This function is for switching light off
def lightoff():
    print('Condition -> ', "Light Off")
    aio.send(digital.key, 0)


# In[8]:


#This function is for switching light on
def lighton():
    print('Condition -> ', "Light On")
    aio.send(digital.key, 1)


# In[9]:


#startup function
def startup():
    while True:
        text = command()
        if text.lower() == wake:
            print("Jarvis is here sir")
            speak("Jarvis is here sir")
            greeting()
            setuplight()
            break


# In[10]:


counter = 0
wake = "Lexi"
startup()

#This is the main function
if __name__ == '__main__':
    while True:
        if counter > 0:
            speak("What more can I do for you sir?")
        else:
            speak("Hello sir, What can I do for you?")
        counter+=1
        statement = command().lower()
        if statement == 0:
            if math.floor(elapsed_time) >= 15:
                break
            else:
                continue

        if wake in statement:
            if "good bye" in statement or "ok bye" in statement or "stop" in statement:
                speak("Good bye sir")
                print("Good bye sir")
                startup()
                counter = 0


            if "wikipedia" in statement:
                speak("Searching in Wikepedia...")
                statement = statement.replace("Wikipedia","")
                results = wikipedia.summary(statement, sentences = 3)
                speak("Sir this is what I have found on Wikipedia")
                print(results)
                speak(results)

            elif "open youtube" in statement:
                webbrowser.open_new_tab("https://youtube.com")
                speak("I have opened the youtube sir")

            elif "open google" in statement:
                webbrowser.open_new_tab("https://google.com")
                speak("I have opened the google sir")

            elif "open gmail" in statement:
                webbrowser.open_new_tab("gmail.com")
                speak("I have opened the gmail sir")

            elif "time" in statement:
                time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time right now is {time} sir")

            elif "camera" in statement or "take a photo" in statement:
                ec.capture(0,"Photo","img.jpg")

            elif "search" in statement:
                statement = statement.replace("search","")
                webbrowser.open_new_tab(statement)

            elif "turn on" in statement or "switch on" in statement:
                lighton()
                speak("Turning on the light sir")
                print("Turning on the light sir")

            elif "turn off" in statement or "switch off" in statement:
                lightoff()
                speak("Turning off the light sir")
                print("Turning off the light sir")

            elif "who are you" in statement or "what can you do" in statement:
                speak("I am Jarvis, your personal assistant who does what you ask me to do")

            elif "who made you" in statement or "who created you" in statement:
                speak("I was built by Sankalp Singh")
                print("I was built by Sankalp Singh")

            elif "log off" in statement or "shutdown" in statement:
                speak("Okay sir the device will shut down in a few seconds please save all your files")
                os.system("shutdown /s /t 1");


# In[ ]:




