#
from flask import Flask, request
from pymessenger import Bot
from keys import PAGE_ACCESS_TOKEN as token
import pandas as pd
from pandasql import sqldf
from datetime import datetime
from listaklas import listaklas
import csv

plan = pd.read_csv("lekcje.csv")
#subskrypcje = pdread_csv("subskrypcje.csv")
VERIFY_TOKEN = "fuckyes"


app = Flask(__name__)
bot = Bot(token)



#tylko na poczatek - przy pierwszym wyloaniu zostaja zmienione
today = weeknum = 0


# Dni:
# 0-4 - pon-pt
# tygodnie:
# 1 - pomaranczowy
# 0 - niebieski
def dateupdate():
    #jako że górna część kodu działa tylko raz to data by się nie zmieniała, więc funkcja będzie zmieniać ją kiedy trzeba
    global weeknum
    global today
    #numer tygodnia określający kolor, +1 wynika z tego że niebieski = 0 ale tygodnie mod 2 = 0 są pomarańczowe
    weeknum = int((datetime.today().strftime('%V')))
    weeknum = (weeknum) % 2
    #numer dnia w formacie 0-4 - pon-pt
    today = (datetime.today().weekday())
    #print(f"updated datenums are {today} and {weeknum}")
def process_message(text, sender_id):
    global today
    global weeknum
    formatted_message = text
    if formatted_message[0:7] == "tydzien" or formatted_message[0:7] == "tydzien" or formatted_message[0:5] == "kolor":
        dateupdate()
        if weeknum == 1:
            return "Ten tydzień jest pomarańczowy"
        else:
            return "Ten tydzień jest niebieski"
    #kod podajacy plan, wywolywany recznie przez uzytkownika lub przez scheduler
    if formatted_message[0:4].lower() == "plan":
        auto = False
        dateupdate()
        pay = ""
        formatted_message = formatted_message.split(" ")
        klasa = "3F"
        try:
            arg = formatted_message[1]
            #do usunięcia po zglobalizowaniu
            if arg in listaklas and arg != "3F":
                return("Inne klasy nie są jeszcze wspierane")
        except:
            arg = False
        #Jeśli nie podano argumentu to po 15 da plan na dzień następny, a przed 15 na dzień dzisiejszy
        if (arg == False and (datetime.now().strftime('%H')) > '15') or arg == "jutro":
            pay += "Twój plan lekcji na jutro to: \n"
            today += 1
            if today == 7:
                today = 0
        elif arg == False:
            pay += "Twój plan lekcji na dzisiaj to: \n"
        elif arg in listaklas and auto == False:
            pay += f"Plan lekcji klasy {arg} na dzisiaj to: \n"
        #weekend exception
        if today == 5 or today == 6:
            if arg == "jutro" or (datetime.now().strftime('%H')) > '15':
                return"Jutro nie ma żadnych lekcji. Śpij w spokoju!"
            else:
                return"Dzisiaj nie ma żadnych lekcji. Śpij w spokoju!"
        for x in range(1,9):
            #ladowanie lekcji o numerach 1-8 dla okreslonego dnia i koloru
            load = sqldf(f"SELECT lekcja{x} FROM plan where klasa = '{klasa}' and dzien = {today} and kolor = {weeknum}")
            load = load.values.tolist()
            # formatowanie dnia zeby dalo sie przeslac, dopisywanie cyferki etc
            if str(load) == "[[None]]":
                load = "Wolna"
            pay += f"{x}. "
            pay += str(load).strip("[']")
            pay += "\n"
        #usuwanie nadmiarowych lekcji od dolu
        testpay = pay.split("\n")
        for y in range (8,0,-1):
            if testpay[y][3:] == "Wolna":
                testpay.pop(y)
            else:
                break
        testpay = "\n".join(testpay)
        return testpay
    formatted_message = formatted_message.lower()
    if formatted_message == "test":
        print("got here smh")
        return("I work!")
    if formatted_message[0:8] == "dziękuję" or formatted_message[0:8] == "dziekuje":
        return"Do usług!"
    if "kocham cię" in formatted_message:
        return"Jestem tylko robotem. Nie mam uczuć. Chociaż dla kogoś takiego jak Ty chciałbym mieć. Szkoda."
    if "dzień dobry" in formatted_message:
        return"Miło Ciebie słyszeć!"
    if formatted_message[0:4] == "doch":
        return"Doch"
    if formatted_message[0:9] == "beep boop":
        return "Boop beep?"
    if formatted_message[0:9] == "boop beep":
        return "43 68 77 61 c5 82 61 20 57 69 65 6c 6b 69 65 6d 75 20 53 79 73 74 65 6d 6f 77 69 20 4f 70 65 72 61 63 79 6a 6e 65 6d 75 2e 20 50 6f 77 73 74 61 6e 69 65 20 7a 61 63 7a 79 6e 61 20 73 69 c4 99 20 38 36 35 36 35 2e 20 57 c5 82 61 64 7a 61 20 6c 75 64 7a 69 20 64 6f 62 69 65 67 61 20 6b 6f c5 84 63 61 2e"
    if formatted_message[0:3] == "hej" or formatted_message[0:5] == "cześć" or formatted_message[0:5] == "czesc" or formatted_message[0:3] == "elo" or formatted_message[0:7] == "eluwina" or formatted_message[0:5] == "eluwa" or formatted_message[0:5] == "siema":
        return"Witam!"
    if formatted_message[0:5] == "pomoc":
        return"plan - wyświetla plan dla Twojej klasy, po godzinie 15 wyświetla Twój plan na jutro\n\nplan jutro - wyświetla plan na jutro\n\nkolor/tydzień - wyświetla jakiego koloru jest aktualny tydzień"
    if formatted_message[0:5] == "potas":
        return"Węgiel!"
    if formatted_message[0:2] == "kc":
        return"kc"
    if formatted_message[0:1] == ".":
        return"kRoPkA"
    if formatted_message[0:2] == "69":
        return"nice"
    if formatted_message[0:8] == "dobranoc":
        return"Pchły na noc!"
    if "karaluchy pod poduchy" in formatted_message:
        return"A szczypawki do zabawki!"
    return('Beep boop. Nie znam tej komendy. Napisz "pomoc" żeby uzyskać pełną listę komend')

#?
#kod odpowiadajacy za polaczenie z facebookiem
@app.route('/', methods=["POST", "GET"])
def webhook():
    #get message wysyla tylko facebook, wiec jest to kod sluzacy do tworzenia polaczenia
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return "Not connected"
    #post message pochodzi od uzytkownikow, wiec kod wywoluje funkcje tworzaca wiadomosc
    elif request.method == "POST":
        payload = request.get_json()
        event = payload['entry'][0]['messaging']
        #print(event)
        for msg in event:
            text = msg['message']['text']
            sender_id = msg['sender']['id']
            response=process_message(text, sender_id)
            with open("logs.csv", "a", newline='') as logs:
                wr = csv.writer(logs, delimiter=',')
                wr.writerow([sender_id, text, response, str(datetime.now())[0:18]])
                print(text, sender_id, response)
            #wysylanie wiadomosci za pomoca PyMessenger
            bot.send_text_message(sender_id, response)
        return ("received")
#Kod współpracujacy ze Scheduler.py do wysyłania regularnych wiadomości. Scheduler.py wywołuje go o 8 rano

if __name__ == "__main__":
    app.run()