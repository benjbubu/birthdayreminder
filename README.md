# Birthday Reminder
===================
----
You forgot all birthdates of your friends and your family ?

You are tired to use Facebook for it ? 

Want simple notification reminder system without using Monica ?

-------



This is for you : BirthdayReminder

One CSV list to remind them all

Notify you by mail (and maybe gotify)

See the current list in HTML (and maybe update it directly on the web page)

----- 

Usage 

Edit config.json and change everything needed

Add some people in your list.csv

Add a crontab each day like this : 0 2 * * * /usr/bin/python3 /path/to/check.py config.json 2>&1

Each day at 2AM, the script will check the csv file you fill into the config.json file and notify you if this is the Birthday of someone in your list.


Requirements :
Python3 at least
Requests (for gotify)


