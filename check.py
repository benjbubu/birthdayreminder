#Check script.
#Get today's date
#Compare today's date with the date in csv file (each line in first column)
#Notify the user by mail and/or gotify

import csv
from datetime import datetime
import sys
import json
from smtplib import SMTP
from email.message import EmailMessage
import requests

#Get the config file from command line options
if len(sys.argv) < 2:
    print("Please specify in argument a json config file")
    print("I.E : python3 check.py config.json")
    exit()
else:
    json_file = sys.argv[1]
    #print("Config file will be", json_file)

#opening configfile

with open(json_file) as config_file:
    data = json.load(config_file)
birthdaylist = data['list_path']
notifemail = data['email']
smtpServer = data['smtpServer']
port = data['port']
my_email = data['my_email']
my_password = data['password']
use_gotify = data['use_gotify']
use_emailnotif = data['use_emailnotif']
gotify_url = data['gotify_url']
gotify_token = data['gotify_token']

#Function to compare today's date with each row of the csv file
def checkbirthday():
    today = datetime.now()
    formatoday = today.strftime("%d/%m")

    #print("Today is", formatoday, "and it's the Birthday of:")

    #Creating an empty list to gather matching results
    result = []

    with open(birthdaylist, encoding="utf8", newline='') as csvfile:
        reader = csv.reader(csvfile)
        #do not show the first header line
        next(reader)
        #list the date of each line
        for date_anniv, annee, prenom, nom in reader:
            if date_anniv == formatoday:
                todayear = int(today.year)
                birthyear = int(annee)
                age = todayear - birthyear

                #Add matching item into the list
                result.append([prenom, nom, age])

    # la fonction retourne la liste de ce qu'elle a trouvé
    return result

#Function to send the notification by mail
def sendmail():
    mailtosend = EmailMessage()
    msg = f"Today is {datetime.now().strftime('%d/%m')} and it's the following persons birthday  :\n"
    for prenom, nom, age in output:
        msg += f"# {prenom} {nom} ({age} ans)\n"
    mailtosend['Subject'] = f"You have {len(output)} birthday to enjoy today !"
    mailtosend['From'] = f"Birthday Reminder <{my_email}>"
    mailtosend['To'] = notifemail
    mailtosend.set_content(msg)

    serveur = SMTP(host=smtpServer, port=port)
    serveur.starttls()
    serveur.login(user=my_email, password=my_password)

    serveur.send_message(mailtosend)
    serveur.quit()

def gotify():
    gotifymsg = ""
    gtfyfullurl = f"{gotify_url}/message?token={gotify_token}"
    for prenom, nom, age in output:
        gotifymsg += f"{prenom} {nom} ({age} ans)\n"
    requests.post(gtfyfullurl, json={
        "message": gotifymsg,
        "priority": 10,
        "title": "Birthday Reminder"
    })



#Calling the check and sending the notification if there are results.

output = checkbirthday()

#Sending mail if parameter is on True in config.json (default mode)
if output and use_emailnotif:
    sendmail()

#Sending gotify push message if parameter is on True in config.json
if output and use_gotify:
    gotify()


