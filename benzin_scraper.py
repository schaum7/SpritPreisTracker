import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from time import sleep
from bs4 import BeautifulSoup
from csv import writer

def get_spritpreise():
    r = requests.get("https://www.tankstellenpreise.de/benzinpreise-letzlingen.html")

    soup = BeautifulSoup(r.content,"html.parser")

    _,_,datum,zeit,_ = soup.find(class_="datum mbottom").text.strip().split(" ")

    preis_diesel = soup.find(class_="pfdiesel").text
    preis_super = soup.find(class_="pfe5").text
    preis_e10 = soup.find(class_="pfe10").text

    with open('Benzinpreise.csv',"a", newline='') as f:
        w = writer(f)
        w.writerow([datum,zeit,preis_diesel,preis_super,preis_e10])


scheduler = BlockingScheduler()
scheduler.add_job(get_spritpreise, 'interval', minutes=30)
scheduler.start()