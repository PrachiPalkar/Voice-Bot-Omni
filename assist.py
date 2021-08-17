import pyttsx3
import speech_recognition as sr
import os
import datetime
from time import strftime
import webbrowser
import smtplib 
import requests
import login
from email.mime.text import MIMEText
import subprocess
import pyautogui
import random
import pytz
import pickle
#import reminder
import covid
from newsapi.newsapi_client import NewsApiClient
#from quotes import random

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october","november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r =sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said=""
    
        try:
            said = r.recognize_google(audio)
            print("Me: " +said)

        except Exception as e:
            print("I couldn't hear you " + str(e))
            speak("I couldn't hear you")

        except sr.UnknownValueError():
            print("Omni: Sorry, I didn't get that")
            speak("Sorry, I didn't get that")

    return said

def greet(): 
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        print("Omni :Hello, Good Morning! ")
        speak("Hello! Good Morning! ")
    elif hour>=12 and hour<18:
        print("Omni: Hello, Good Afternoon! ")
        speak("Hello! Good Afternoon! ")
    else:
        print("Omni: Hello, Good Evening! ")
        speak("Hello! Good Evening!")

#    reminder.read_reminder()
    print("Omni: I'm Omni, your personal assistant, Tell me how can I help you?")
    speak("I'm Omni, your personal assistant, Tell me how can I help you?")

def current_time():
    current=strftime("%I:%M")
    print("Omni: Current time is " + " " + current)
    speak("Current time is" + current)

def current_date():
    dateM=strftime("%B:%d:%A:%Y")
    print("Omni: Today's date is "+dateM)
    speak("Today's date is "+dateM)

def current_day():
    dateM=strftime("%A")
    print("Omni: Today is " + dateM)
    speak("Today is " + dateM)

def current_month():
    dateM=strftime("%B")
    print( "Omni: Current month is " + dateM)
    speak( "current month is" + dateM)

def weather():
    speak("Please enter your city name")
    location = input("Omni: Enter your city name- ")
    print("Omni: showing the current weather")
    speak("This the current weather in"+location)
    user_api = "347496d31fd6873ba0c4e8a9c9dda7e2"

    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+user_api
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    #create variables to store and display data
    temp_city = ((api_data['main']['temp']) - 273.15)
    weather_desc = api_data['weather'][0]['description']
    hmdt = api_data['main']['humidity']
    wind_spd = api_data['wind']['speed']
    date_time = datetime.datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

    print ("-------------------------------------------------------------")
    print ("Weather Stats for - {}  || {}".format(location.upper(), date_time))
    print ("-------------------------------------------------------------")

    print ("Current temperature is: {:.2f} deg C".format(temp_city))
    print ("Current weather desc  :",weather_desc)
    print ("Current Humidity      :",hmdt, '%')
    print ("Current wind speed    :",wind_spd ,'kmph')

def mail():
    print("whom do you want to send?")
    speak("whom do you want to send? Enter the id")
    send_to=input("Enter the id:")
    print("what is the subject?")
    speak("what is the subject?")
    print("Listening..")
    sub = get_audio()
    while "I could't hear you" in sub:
        print("Please repeat")
        print("Listening..")
        sub= get_audio()
    print("what is the message?")
    speak("what is the message?")
    print("Listening..")
    m = get_audio()
    while "I could't hear you" in m:
        print("Please repeat")
        print("Listening..")
        m= get_audio()

    server=smtplib.SMTP_SSL('smtp.gmail.com',465)

    EMAIL=login.EMAIL
    PASSWORD=login.PASSWORD
    server.login(EMAIL,PASSWORD)

    message=MIMEText(m)
    message["From"]=EMAIL
    message["To"]=send_to
    message["Subject"]=sub

    server.sendmail(EMAIL,send_to,message.as_string())

    print("Mail is successfully sent")
    speak("Mail is successfully sent")

    server.quit()

def notepad(text): 
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])
    print("A note has been created successfully!")
    speak("A note has been created successfully!")
    
def openGmail(): 
        print("Omni: Opening Email Client")
        url="https://mail.google.com/mail/u/4/#inbox"
        speak("Opening Email Client")
        webbrowser.get().open(url)

def Gmail(said): #opens mails from a person
    if "from" not in said:
        print("Omni: Please tell me whose mail is to be opened")
        speak("Please tell me whose mail is to be opened")
    name = said.split("from")[-1]
    url = "https://mail.google.com/mail/u/4/#search/" + name
    webbrowser.get().open(url)
    print("Omni: Here is what I found for " + name + "in gmail ")
    speak("Here is what I found for " + name + "in gmail")

def Drive(said): #opens file from drive
        print("Omni: Tell me the name of the file to view from drive")
        speak("Tell me the name of the file to view from drive")
        print("Listening..")
        file = get_audio()
        url = "https://drive.google.com/drive/u/4/search?q=" + file
        webbrowser.get().open(url)
        print("Omni: Here is what I found for " + file + "in drive ")
        speak("Here is what I found for " + file + "in drive")

def spotify(said): #plays song on spotify web
        song = said.split("play")[-1]
        url="https://open.spotify.com/search/"+song
        webbrowser.get().open(url)
        print("Omni: playing song" + song)
        speak(" playing song" + song)

def Youtube(said):  #opens youtube
        search_term = said.split("search")[-1]
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        print("Omni: Here is what I found for " + search_term)
        speak("Here is what I found for " + search_term)

def ss():
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('F:\Chatbot\screen.png')
        print("Omni: A screenshot has been taken successfully and saved as screen.png")
        speak("A screenshot has been taken successfully and saved as screen.png")

def game():
        print("Omni:Okay! We will play a game. Choose among rock, paper and scissor")
        speak("Okay! We will play a game. Choose among rock, paper and scissor")
        print("Listening..")

        pmove=get_audio()
        moves=["rock", "paper", "scissor"] 
#        while (pmove in moves):
        cmove=random.choice(moves)
        print("The computer chose " + cmove)
        speak("The computer chose " + cmove)
 #       speak("You chose " + pmove)

        if pmove==cmove:
            print("Omni: the match is draw")
            speak("the match is draw")
        elif pmove== "rock" and cmove== "scissor":
            print("Omni: You won!")
            speak("You won!")
        elif pmove== "rock" and cmove== "paper":
            print("Omni: Computer won!")
            speak("Computer won!")
        elif pmove== "paper" and cmove== "rock":
            print("Omni: You won!")
            speak("you won!")
        elif pmove== "paper" and cmove== "scissor":
            print("Omni: Computer won!")
            speak("Computer won!")
        elif pmove== "scissor" and cmove== "paper":
            print("Omni: You won!")
            speak("you won!")
        elif pmove== "scissor" and cmove== "rock":
            print("Omni: Computer won!")
            speak("Computer won!")

def quote():
#    print(random())
    quotes=['Self love is the greatest medicine.',
    'Believe you can and you’re halfway there.',
    'Be patient with yourself. Nothing in nature blooms all year.',
    'Every thought we think is creating our future.']
    rand=random.choice(quotes)
    print(rand)
    speak(rand)

def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

SERVICE= authenticate_google()

def get_events(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('Omni: No upcoming events found.')
        speak('No upcoming events found.')
    else:
        print(f"You have {len(events)} events on this day.")
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            if "T" in start:
                start_time = str(start.split("T")[1].split("-")[0])
                if int(start_time.split(":")[0]) < 12:
                    start_time = start_time + "am"
                else:
                    start_time = str(int(start_time.split(":")[0])-12)
                    start_time = start_time + "pm"
                speak(event["summary"] + " at " + start_time)
            else:
                speak(event["summary"])

def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:  
        year = year+1
    
    if month == -1 and day != -1:  
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month
    
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  # FIXED FROM VIDEO
        return datetime.date(month=month, day=day, year=year)

def create_event(said,service): #add events to calendar
    print("Omni: When do you have this event")
    speak("When do you have this event")
    print("Listening..")
    text = get_audio().lower()
    while text.isdigit() == False:
        print("Omni:Please repeat")
        speak("Please repeat")
        print("Listening..")
        text= get_audio() 
    date= get_date(text)
#   print("what is the event:")
#    print("Listening..")
    summary = input("what is the event:")
    speak("Please enter the event name")
    start = date.isoformat()
    event_result = service.events().insert(calendarId='primary',
       body={
           "summary": summary,
           "description": '',
           "start": {"date": start, "timeZone": 'Asia/Kolkata'},
           "end": {"date": start, "timeZone": 'Asia/Kolkata'},
            }
      ).execute()
    print("Omni: Event has been created successfully!")
    speak("Event has been created successfully!")
    print("summary: ", event_result['summary'])
    print("starts on: ", event_result['start']['date'])
    # print("ends at: ", event_result['end']['dateTime'])
    speak(event_result["summary"]  + " on " + start)

def news():
    newsapi = NewsApiClient(api_key="87fb7cc4ac7f484f95709cf359c20117")
    print("Omni:What topic you need the news about")
    speak("What topic you need the news about")
    print("Listening..")
    topic = get_audio().lower()
    data = newsapi.get_top_headlines(q=topic, language="en", page_size=5)
    newsdata = data["articles"]
    for y in newsdata:
        print("Omni:"+y["description"])
        speak(y["description"])
        continue

def chat():
    while True: 
        print("Listening..")
        text = get_audio().lower()

        if "weather" in text:
            weather()
        
        elif "time" in text:
            current_time()
        
        elif "date" in text:
            current_date()
        
        elif "day" in text and "today" not in text:
            current_day()
            
        elif "month" in text:
            current_month()

        elif "send mail" in text:
            mail() 

        elif "note" in text or "write this" in text or "notepad" in text or "remember this" in text:
            speak("What would you like me to make a note of? ")
            print("Omni: What would you like me to make a note of? ")
            note = get_audio()
            while "I could't hear you" in note:
                print("Omni: Please repeat")
                print("Listening..")
                note= get_audio()
            notepad(note)
            
        elif "gmail" in text and 'from' not in text:
            openGmail()  
            
        elif "mail from" in text:
            Gmail(text)  
            
        elif "song" in text or "spotify" in text:
            spotify(text)

        elif "youtube" in text:
            Youtube(text)

        elif "drive" in text:
            Drive(text)

        elif "capture" in text or "my screen"in text or "screenshot" in text:
            ss()

        elif "game" in text:
            game()

        elif "what do i have" in text or "do i have" in text or "am i busy" in text:
            date = get_date(text)
            get_events(date, SERVICE)

        elif "event"in text:
            create_event(text,SERVICE)

        elif "ok" in text:
            print("Omni: I would love to help you more.")
            speak("I would love to help you more.")

        elif "thank" in text:
            print("Omni: Anytime! I would love to help you more.")
            speak("Anytime! I would love to help you more.")

        elif "your name" in text or "what's your name" in text:
                    print("Omni: My name is Omni")
                    speak("My name is Omni")

        elif "how are you" in text:
                    print("Omni: I'm doing good. What about you?")
                    speak("I'm doing good. What about you?")

        elif "good" in text or "great" in text:
                    print("Omni: That's great!")
                    speak("That's great!")

        elif "are you a robot" in text:
                    print("Omni: Yes, I am a robot and That makes it ideal for keeping things you share with me private.")
                    speak("Yes, I am a robot and That makes it ideal for keeping things you share with me private.")
        
        elif "are you a human" in text:
                    print("Omni: No, I am a robot. That makes it ideal for keeping things you share with me private.")
                    speak("No, I am a robot. That makes it ideal for keeping things you share with me private.")
        
        elif "who are you" in text or "define yourself" in text: 
                    speak ("Omni: Your personal Assistant. You can command me to perform various tasks")
                    print("Your personal Assistant. You can command me to perform various tasks")
        
        elif "who made you" in text or "created you" in text: 
                  print("Omni: I have been created by humans.")
                  speak("I have been created by humans.")

        elif "stop" in text or "quit" in text or "exit" in text:
            quote()
            print("Omni: I hope I assisted you well. Hope to talk to you soon!") 
            speak("I hope I assisted you well. Hope to talk to you soon")                                                                                                                                                               
            exit()                                                      

        elif "bye" in text:
            quote()
            print("Omni: I hope I assisted you well. Hope to talk to you soon, Bye!") 
            speak("I hope I assisted you well. Hope to talk to you soon, Bye!")                                                                                                                                                               
            exit()

        elif "news" in text:
            news()

        elif "covid" in text:
            print("Omni: What information do you want me to give you related to COVID?")
            speak("What information you want me to give you related to COVID?")
            covid.main()

def main():
    print("Welcome to the virtual voice assistant!")
    greet() 
    chat()
   
if __name__ == '__main__':
   main()
