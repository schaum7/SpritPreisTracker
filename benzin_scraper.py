import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from time import sleep
from bs4 import BeautifulSoup
from csv import writer

def get_spritpreise():
    r = requests.get("https://www.tankstellenpreise.de/benzinpreise-letzlingen.html")

    soup = BeautifulSoup(r.content,"html.parser")

    _,_,datum,zeit,_ = soup.find(class_="datum mbottom").text.strip().split(" ")
    row = [datum,zeit]
    
    row.append(soup.find(class_="pfdiesel").text) # Diesel
    row.append(soup.find(class_="pfe5").text) # Super
    row.append(soup.find(class_="pfe10").text) # E10

    with open('Benzinpreise.csv',"a", newline='') as f:
        w = writer(f)
        w.writerow(row)
    
    print("wrote: ", row)


scheduler = BlockingScheduler()
scheduler.add_job(get_spritpreise, 'interval', minutes=30)
scheduler.start()