import datetime
import os
import random
import sys
import time
import webbrowser
import PyPDF2
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit as kit
import requests
import speech_recognition as sr
import wikipedia
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gui import Ui_MainWindow


engine = pyttsx3.init('sapi5')
newVoiceRate = 160
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voices', voices[0].id)
engine.setProperty("rate", newVoiceRate)


def speak(audio):
    engine.say(audio)
    # ui = Ui_MainWindow()
    # ui.textBrowser.setText(audio)
    print(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 8 and hour < 12:
        time1 = datetime.datetime.now()
        time1 = time1.strftime("%I:%M %p")
        speak(f"good morning, its {time1}")
    elif hour >= 12 and hour <= 16:
        time1 = datetime.datetime.now()
        time1 = time1.strftime("%I:%M %p")
        speak(f"good afternoon, its {time1}")
    else:
        time1 = datetime.datetime.now()
        time1 = time1.strftime("%I:%M %p")
        speak(f"good evening, its {time1}")
    speak("I am your robot assistant sir. please tell me how can i help you")


class Mainthrea(QThread):
    def __init__(self):
        super(Mainthrea, self).__init__()



    def run(self):
        self.work()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening...")
            r.pause_threshold = 2
            audio = r.listen(source, timeout=2, phrase_time_limit=5)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-IN')
            us = query
            print(f"user said: {us}")



        except Exception as e:
            speak("Sorry sir, I didn't get you")
            speak("Say that again please...")
            return "none"
        return query

    def work(self):
        wish()
        while True:
            try:
                self.query = self.takecommand().lower()

                if "open notepad" in self.query:
                    npath = "C:\\WINDOWS\\system32\\notepad"
                    os.startfile(npath)

                elif "hello" in self.query:
                    speak("Hey Atishay tell me work to do")
                    continue

                elif "open command prompt" in self.query:
                    npath = "C:\\WINDOWS\\system32\\cmd"
                    os.startfile(npath)

                elif "open adobe reader" in self.query:
                    npath = "C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32"
                    os.startfile(npath)


                elif "play music" in self.query:
                    musicd = "D:\\songs"
                    songs = os.listdir(musicd)
                    ran = random.choice(songs)
                    os.startfile(os.path.join(musicd, ran))

                elif "ip address" in self.query:
                    ip = get("https://api.ipify.org").text
                    speak(f"your IP address is {ip}")

                elif "wikipedia" in self.query:
                    speak("searching wikipedia....")
                    self.query = self.query.replace("wikipedia", "")
                    result = wikipedia.summary(self.query, sentences=2)
                    speak("according to wikipedia")
                    speak(result)

                elif "open youtube" in self.query:
                    webbrowser.open("youtube.com")

                elif "open facebook" in self.query:
                    webbrowser.open("facebook.com")

                elif "open instagram" in self.query:
                    webbrowser.open("instagram.com")

                elif "open google" in self.query:
                    speak("Sir, what should i search on google")
                    search = self.takecommand().lower()
                    kit.search(search)

                elif "send message" in self.query:
                    speak("Sir please, tell whatsapp mobile number")
                    phone = self.takecommand().lower()
                    speak("Sir please, tell me the msg")
                    msg = self.takecommand().lower()
                    hour = int(datetime.datetime.now().hour)
                    min = int(datetime.datetime.now().minute)
                    min += 1
                    # print(hour)
                    # print(min)
                    kit.sendwhatmsg(f"+91{phone}", f"{msg}", hour, min)

                elif "play song on youtube" in self.query:
                    speak("sir please, tell me the song name ")
                    song = self.takecommand().lower()
                    kit.playonyt(song)

                elif "open whatsapp" in self.query:
                    webbrowser.open("https://web.whatsapp.com/")

                elif "writing" in self.query:
                    speak("sir, please tell me what you want to write")
                    content = self.takecommand().lower()
                    kit.text_to_handwriting(f"{content}")

                elif "shutdown" in self.query:
                    kit.shutdown(time=300)
                    speak("PC will be shutdown in 5 minutes")

                elif "cancel power off" in self.query:
                    kit.cancelShutdown()

                elif "tell me a joke" in self.query:
                    joke = pyjokes.get_joke()
                    speak(joke)

                elif "set alarm" in self.query:
                    speak("sir, please tell me the hour")
                    hr = int(self.takecommand().lower())
                    speak("sir, please tell me the minute")
                    min1 = int(self.takecommand().lower())
                    hrc = int(datetime.datetime.now().hour)
                    mic = int(datetime.datetime.now().minute)
                    if hr == hrc and min1 == mic:
                        musicd = "D:\\songs"
                        songs = os.listdir(musicd)
                        ran = random.choice(songs)
                        os.startfile(os.path.join(musicd, ran))

                elif "switch the window" in self.query:
                    pyautogui.keyDown("alt")
                    pyautogui.press("tab")
                    pyautogui.keyUp("alt")

                elif "exit" in self.query:
                    pyautogui.keyDown("alt")
                    pyautogui.press("F4")

                elif "screenshot" in self.query:
                    speak("sir please hold the screen for few seconds, i am taking screenshot")
                    time.sleep(3)
                    im = pyautogui.screenshot("screenshot.png")
                    speak("i am done sir, screenshot is saved in our main folder.")


                elif "can you search in my insta" in self.query:
                    with open('account.txt', 'r') as ac:
                        info = ac.read().split()
                        email = info[0]
                        pas = info[1]
                    speak("sir, tell me what you want to search")
                    com = self.takecommand().lower()

                    op = Options()
                    op.add_argument("start-maximized")

                    driver = webdriver.Chrome(options=op)
                    driver.get("https://www.instagram.com/")

                    emailxpath = '//*[@id="loginForm"]/div/div[1]/div/label/input'
                    passxpath = '//*[@id="loginForm"]/div/div[2]/div/label/input'
                    notnowxpath = '/html/body/div[4]/div/div/div/div[3]/button[2]'
                    loginxpath = '//*[@id="loginForm"]/div/div[3]/button/div'
                    searchxpath = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'
                    notnow = '//*[@id="react-root"]/section/main/div/div/div/div/button'

                    time.sleep(2)

                    driver.find_element_by_xpath(emailxpath).send_keys(email)
                    time.sleep(0.5)
                    driver.find_element_by_xpath(passxpath).send_keys(pas)
                    time.sleep(0.5)
                    driver.find_element_by_xpath(loginxpath).click()
                    time.sleep(4)
                    driver.find_element_by_xpath(notnow).click()
                    time.sleep(2)
                    driver.find_element_by_xpath(notnowxpath).click()
                    time.sleep(1)
                    driver.find_element_by_xpath(searchxpath).send_keys(com)

                elif "can you see my insta message" in self.query:
                    with open('account.txt', 'r') as ac:
                        info = ac.read().split()
                        email = info[0]
                        pas = info[1]

                    op = Options()
                    op.add_argument("start-maximized")

                    driver = webdriver.Chrome(options=op)
                    driver.get("https://www.instagram.com/")

                    emailxpath = '//*[@id="loginForm"]/div/div[1]/div/label/input'
                    passxpath = '//*[@id="loginForm"]/div/div[2]/div/label/input'
                    notnowxpath = '/html/body/div[4]/div/div/div/div[3]/button[2]'
                    loginxpath = '//*[@id="loginForm"]/div/div[3]/button/div'
                    msgxpath = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/a'
                    notnow = '//*[@id="react-root"]/section/main/div/div/div/div/button'

                    time.sleep(2)

                    driver.find_element_by_xpath(emailxpath).send_keys(email)
                    time.sleep(0.5)
                    driver.find_element_by_xpath(passxpath).send_keys(pas)
                    time.sleep(0.5)
                    driver.find_element_by_xpath(loginxpath).click()
                    time.sleep(4)
                    driver.find_element_by_xpath(notnow).click()
                    time.sleep(2)
                    driver.find_element_by_xpath(notnowxpath).click()
                    time.sleep(1)
                    driver.find_element_by_xpath(msgxpath).click()

                elif "can you comment in my insta post" in self.query:
                    with open('account.txt', 'r') as ac:
                        info = ac.read().split()
                        email = info[0]
                        pas = info[1]
                    speak("sir, tell me what you want to comment")
                    com = self.takecommand().lower()

                    op = Options()
                    op.add_argument("start-maximized")

                    driver = webdriver.Chrome(options=op)
                    driver.get("https://www.instagram.com/")

                    emailxpath = '//*[@id="loginForm"]/div/div[1]/div/label/input'
                    passxpath = '//*[@id="loginForm"]/div/div[2]/div/label/input'
                    notnowxpath = '/html/body/div[4]/div/div/div/div[3]/button[2]'
                    notnow = '//*[@id="react-root"]/section/main/div/div/div/div/button'
                    loginxpath = '//*[@id="loginForm"]/div/div[3]/button/div'
                    comxpath = '//*[@id="react-root"]/section/main/section/div/div[2]/div/article[1]/div[3]/section[3]/div/form/textarea'
                    postbtxpath = '//*[@id="react-root"]/section/main/section/div/div[2]/div/article[1]/div[3]/section[3]/div/form/button[2]'

                    time.sleep(2)

                    driver.find_element_by_xpath(emailxpath).send_keys(email)
                    time.sleep(0.5)
                    driver.find_element_by_xpath(passxpath).send_keys(pas)
                    time.sleep(0.5)
                    driver.find_element_by_xpath(loginxpath).click()
                    time.sleep(4)
                    driver.find_element_by_xpath(notnow).click()
                    time.sleep(2)
                    driver.find_element_by_xpath(notnowxpath).click()
                    time.sleep(1)
                    driver.find_element_by_xpath(comxpath).click()
                    driver.find_element_by_xpath(comxpath).send_keys(com)
                    time.sleep(0.5)
                    driver.find_element_by_xpath(postbtxpath).click()

                elif "instagram profile" in self.query or "profile on instagram" in self.query:
                    speak("sir please, enter the user name correctly.")
                    profilen = input("Enter user name hare:")
                    webbrowser.open(f"www.instagram.com/{profilen}")
                    speak(f"sir, here is the profile of the user {profilen}")

                elif "where i am" in self.query or "where we are" in self.query:
                    speak("wait sir, let me check")
                    try:
                        ip = get("https://api.ipify.org").text
                        url = 'https://get.geojs.io/v1/ip/geo/' + ip + '.json'
                        geo_req = requests.get(url)
                        geo_location = geo_req.json()
                        city = geo_location['city']
                        state = geo_location['region']
                        country = geo_location['country']

                        speak(f"sir, we are in {city} city, {state} state of {country} country")
                    except Exception as e:
                        speak("sorry sir,due to network issues i am not able to find where we are.")

                elif "read pdf" in self.query:
                    pdf = open('MediciEffect.pdf', 'rb')
                    pdfrreader = PyPDF2.PdfFileReader(pdf)
                    pages = pdfrreader.numPages
                    speak(f"Total numbers of pages in this book {pages}")
                    speak("sir please enter the pages number i have to read")
                    pageno = int(input("Please enter the page number: "))
                    pagereader = pdfrreader.getPage(pageno)
                    text = pagereader.extractText()
                    speak(text)

                elif "sleep" in self.query or "you can sleep now" in self.query:
                    speak("Ok sir, i am going to sleep now you can call me anytime.")
                    break

                elif "goodbye" in self.query or "bye" in self.query or "thank you" in self.query:
                    speak("thanks for using me sir, have a good day")
                    sys.exit()

                speak("sir, do you have any other work")
            except Exception as e:
                speak("Sorry sir, i am facing some issues please tell me some other work")


startExe = Mainthrea()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start)



    def start(self):
        self.ui.movie = QtGui.QMovie("../../Downloads/CorruptLinearElk-size_restricted.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../Downloads/45-REC-unscreen.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../Downloads/ezgif.com-gif-maker (5).gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExe.start()


app = QApplication(sys.argv)
robot = Main()
robot.show()
exit(app.exec_())

