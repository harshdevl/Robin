from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
from playsound import playsound
from demo import download_songs, download_video, download_playlist
import smtplib
import requests
import urllib.request
from loadmodel import detect_harsh
from use import classify
from music import search_song, play_songs


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
Voice_rate = 200
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate' , Voice_rate)

def response(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        response("Good Morning sir")
        if hour >=3 and hour <= 5:
            response("sir your up to late i think you should get some sleep now")

    elif hour>=12 and hour<17:
        response("Good Afternoon sir")   

    else:
        response("hello sir Good Evening")  


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  
        print("Listening...")
        # r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print("User said:", query)

    except Exception as e:
        # print(e)    
        print("can you say that again please i didn't get it properly...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


def gettime():
    strTime = datetime.datetime.now().strftime('%I:%M:%S %p')    
    response(f"sir, the time is {strTime}")

def play_music():
    music_dir = 'D:/python_project/project_jarvis/songs_by_jarvis'
    songs = os.listdir(music_dir)
    print(songs)    
    os.startfile(os.path.join(music_dir, songs[0]))

def open_browser(num):
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

    if num == 2:
        webbrowser.get(chrome_path).open("youtube.com")
    elif num == 3:
        webbrowser.get(chrome_path).open("google.com")
    elif num == 4:
        url = 'https://www.youtube.com/watch?v=RgKAFK5djSk&list=RDRgKAFK5djSk&start_radio=1&t=0'
        webbrowser.get(chrome_path).open(url)
    elif num == 5:
        url = 'https://www.youtube.com/watch?v=Te8Z_Oy7yUE&list=PLw0OS4SJWbYBjpgcIQvCWyaffXd6w_DG4'
        webbrowser.get(chrome_path).open(url)
        response('done sir')
    elif num == 6:
        url = 'https://www.youtube.com/watch?v=II2EO3Nw4m0&list=RDII2EO3Nw4m0&start_radio=1'
        webbrowser.get(chrome_path).open(url)


def write_diary():
    f = open(r"mydiary.txt", "a")
    response('opening diary sir..')
    time_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    f.write(time_now)
    while True:
        inputs = takeCommand().lower()
        f.write("\n"+inputs)
        if 'close the diary' in inputs:
            f.close()
            response('closing the diary sir')
            break


def setname(name1):
   global name
   name = name1

def getname():
    return name     


def delete_diary():
    os.remove('mydiary.txt')
    response('diary has been removed sir!')

if __name__ == "__main__":
    name = 'robin'
    playbutton = ''
    response("initiating identification")
    access = detect_harsh()
    if access:
        response('access granted')
        
        wishMe()
    else:
        response('access has been denied by Harsh')
    while access:
    # if 1:
        query = takeCommand().lower()
        setname(name)
        name = getname()
        if name in query:
            try:
                playbutton.click()
            except:
                # Logic for executing tasks based on query
                if 'wikipedia' in query:
                    response('Searching Wikipedia...')
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    response("According to Wikipedia")
                    print(results)
                    response(results)

                elif 'open youtube' in query:
                    value = 2
                    open_browser(value)

                elif 'open google' in query:
                    value = 3
                    open_browser(value)

                elif 'play music' in query:
                    response('what would you like sir...')
                    query = takeCommand().lower()
                    url = search_song(query)
                    playbutton = play_songs(url)
                    
                    # play_music()

                elif 'what' in query and  'time' in query:
                    gettime()

                elif 'email to person' in query:
                    try:
                        response("What should I say?")
                        content = takeCommand()
                        to = "personemail@gmail.com"    
                        sendEmail(to, content)
                        response("Email has been sent!")
                    except Exception as e:
                        print(e)
                        response("Sorry my friend person. I am not able to send this email")

                elif 'sleep time' in query or 'you can rest now' in query:
                    response('okay sir have a good day')
                    break
                elif 'what is your name' in query:
                    name = getname()
                    response(name + " is my name sir")

                elif 'change your name' in query:
                    response('then what will be my name sir')
                    tempname = takeCommand().lower()
                    setname(tempname)
                    name = getname()

                elif 'get news' in query:
                    response("News for today...")
                    url = ('http://newsapi.org/v2/top-headlines?country=in&apiKey=f3ef8f0f1939482491de40ee5f8686df')
                    news = requests.get(url)
                    news_dict = news.json()
                    arts = news_dict['articles']

                    for articles in arts:
                        try:

                            response(articles['title'])
                            response('')
                        except:
                            response(articles['title'].encode('utf-8'))

                elif 'give me a weather of' in query:
                    place = query[20:]
                    url ="http://api.weatherstack.com/current?access_key=4d84d938c204df5773539c9affb09078&query="+place
                    responses = requests.get(url)
                    weather = responses.json()
                    try:
                        temp = weather['current']['temperature']
                        response("temprature is")
                        response(temp)
                        des = weather['current']['weather_descriptions']
                        dire = weather['current']['wind_dir']
                        humidity = weather['current']['humidity']
                        uv =weather['current']['uv_index']
                        response("weather is")
                        response(des)
                        response("wind directions is")
                        response(dire)
                        response("humidity")
                        response(humidity)
                        response("U v index")
                        response(uv)
                    except:
                        response("try again")            

                elif 'open diary' in query:
                    write_diary()
                
                elif 'delete diary' in query:
                    delete_diary()

                elif 'play english songs' in query:
                    value = 4
                    open_browser(value)   


                elif 'funtime' in query:
                    value = 5
                    open_browser(value)

                elif 'hindi songs' in query:
                    value = 6
                    open_browser(value)

                elif 'download' in query and  'song' in query:
                    response('which song you would like me to donwload sir?')
                    query = takeCommand().lower()
                    url = search_song(query)
                    download_songs(url)
                    response('download has been completed')

                elif 'download' in query and 'video' in query:
                    response('which video you would like me to donwload sir?')
                    query = takeCommand().lower()
                    url = search_song(query)
                    download_video(query)
                    response('work done sir')

                elif 'download' in query and 'playlist' in query:
                    response('which playlist you would like me to donwload sir?')
                    query = takeCommand().lower()
                    url = search_song(query)
                    download_playlist(url)
                    response('work done sir')

                elif 'cheer me up' in query or 'chair me up' in query:
                    playsound('cheer_by_jarvis/cheer.mp3')


                else:
                    response_from_chat = classify(query)
                    response(response_from_chat)
