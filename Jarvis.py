# Import Modules
import os
import re
import pyowm
import shlex
import urllib
import pyttsx3
import smtplib
import datetime
import wikipedia
import subprocess
import webbrowser as wb
import speech_recognition as sr
from pyowm import OWM
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen


engine = pyttsx3.init()
newVoiceRate = 190
engine.setProperty('rate', newVoiceRate)

# Response function
def response(audio):
    engine.say(audio)
    engine.runAndWait()

# Time function
def time():
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    response(Time)

# Date function
def date():
    Year = int(datetime.datetime.now().year)
    Month = int(datetime.datetime.now().month)
    Date = int(datetime.datetime.now().day)
    response("Today's date is")
    response(Date)
    response(Month)
    response(Year)

# Function to take command
def takeCommand():
    ear = sr.Recognizer()
    
    with sr.Microphone(device_index = 2) as source:
        print("Listening....")
        ear.adjust_for_ambient_noise(source = source, duration = 1)
        ear.pause_threshold = 2
        audio = ear.listen(source)
    
    try:
        print("Recognising...")
        command = ear.recognize_google(audio)
        print(command)
    
    except Exception as e:
        print("Error :  " + str(e))
        response("Sorry I didn't get that...")
 
        return "None"
    return command

# Wish function
def wishme():
    response("Welcome back sir!")

    Hour =datetime.datetime.now().hour
    if Hour >= 6 and Hour < 12:
        response("Good morning!")
    elif Hour >= 12 and Hour < 18:
        response("Good afternoon!")
    elif Hour >= 18 and Hour <= 24 :
        response("Good evening!")
    else:
        return None

    response("How can i help you?")

def leave():
    Hour =datetime.datetime.now().hour
    if Hour >= 0 and Hour < 6:
        response("Have a good night sir!")
    elif Hour >= 6 and Hour < 18:
        response("Have a good day sir!")
    elif Hour >= 18 and Hour < 24 :
        response("Have a good night sir!")
    else:
        #response("")
        return None

# Send email 
def sendemail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()


## Main Function
    
if __name__ == "__main__":

    response("hello")

    while True:
        command = takeCommand().lower()
        print(command)

# Ask time
        if "the time" in command:
            time()

# Ask Date         
        elif "date" in command:
            date()

# Search anything on wikipedia        
        elif "wikipedia" in command:
            response("Searching...")
            command = command.replace("wikipedia", "")
            result = wikipedia.summary(command, sentences = 2)
            response(result)

# Quit the Assistant        
        elif "bye" in command:
            leave()
            quit()

# Logout user from computer
        elif "logout" in command:
            os.system("shutdown - 1")   

# Shutdown computer
        elif "shutdown" in command:
            os.system("shutdown /s /t 1")

# Restart computer
        elif "restart" in command:
            os.system("shutdown /r /t 1")

# Play any song on youtube
        elif "play" in command:
            response("What should i play?")
            song = takeCommand()
            url = 'https://www.youtube.com/results?search_command=' + song
            wb.get().open_new(url)

# Weather and temperature of any city
        elif 'current weather' in command:
            reg_ex = re.search('current weather in (.*)', command)
            if reg_ex:
                city = reg_ex.group(1)
                owm = OWM(api_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
                mgr = owm.weather_manager()
                obs = mgr.weather_at_place(city)
                w = obs.weather
                k = w.status
                x = w.temperature(unit='celsius')
                response('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))

# Start any system app
        elif 'launch' in command:
            #args = shlex.split(command)
            reg_ex = re.search('launch (.*)', command)
            if reg_ex:
                appname = reg_ex.group(1)
                appname1 = appname+".app"
                subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE, shell=True)
                response('I have launched the desired application')

# News function
        elif 'news for today' in command:
            try:
                news_url="https://news.google.com/news/rss"
                Client=urlopen(news_url)
                xml_page=Client.read()
                Client.close()
                soup_page=soup(xml_page,"xml")
                news_list=soup_page.findAll("item")
                for news in news_list[:15]:
                    response(news.title.text.encode('utf-8'))
            except Exception as e:
                    print(e)

# Remember function
        elif "remember that" in command:
            response("What should i remember?")
            data = takeCommand()
            response("I will remember that" + data)
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

# Remind what told to remember
        elif "know anything" in command:
            remember = open("data.txt", "r")
            response("You to me to remember that" + remember.read())

# Ask about anything 
        elif 'tell me about' in command:
            reg_ex = re.search('tell me about (.*)', command)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    ny = wikipedia.page(topic)
                    response(ny.content[:500].encode('utf-8'))
            except Exception as e:
                    response(e)