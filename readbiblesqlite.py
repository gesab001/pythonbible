#!/usr/bin/python3
import os
import _thread
import sqlite3
from datetime import datetime
import time
import math
from tkinter import *

def retrieve(id):
        conn = sqlite3.connect('./kjv.db')
        cursor = conn.execute("SELECT * FROM  bible4 WHERE ID=(?)", (id,))
        for row in cursor:
                text = row[4]
                book = row[1].strip()
                #book = book.split(" ")
                #name = book[len(book)-1]
                reference = book + " " + str(row[2]) + ":" + str(row[3])
                return [text, reference]
        #print ("Operation done successfully");
        conn.close()

def setCurrentDate():
    fmt = '%S'
    now = datetime.now()
    now = datetime.strftime(now, fmt)
    #newMinute = datetime.mktime('00', fmt)
    currentDate = datetime.strptime(now, fmt)
    #print(currentDate)
    #time.sleep(1)

def getCurrentID():   
    #minutesPastSinceLaunch = (currentDate - launchDate )
    fmt = '%Y-%m-%d %H:%M:%S'
    now = datetime.now()
    now = datetime.strftime(now, fmt)
    launchDate = datetime.strptime('2018-06-23 14:45:00', fmt)
    currentDate = datetime.strptime(now, fmt)
    # Convert to Unix timestamp
    d1_ts = time.mktime(launchDate.timetuple())
    d2_ts = time.mktime(currentDate.timetuple())
    # They are now in seconds, subtract and then divide by 60 to get minutes.
    result = int(d2_ts-d1_ts) / 60
    result = round(result)+1
    while result>31102:
       result-=31102
    return result

def autoMode():
    id = getCurrentID()
    word  = retrieve(id)
    #time.sleep(1)
    return word
    #setCurrentDate()

def getFontSize():
    import tkinter as tk
    from tkinter import font
    x = tk.Tk()
    screenSize = [x.winfo_screenwidth(), x.winfo_screenheight()]
    setFontSize = round(screenSize[0]/30)
    #getFont = font.Font(size=setFontSize)
    return setFontSize

def changeVerse():
    text = autoMode()
    word = text[0]
    reference = text[1]
    wordString.set(word)
    referenceString.set(reference) 

global master 

master = Tk()

global wordLabel
global referenceLabel
def displayText():
    #master = Tk()
    text = autoMode()
    word = text[0]
    reference = text[1]
    global wordLabel
    global referenceLabel
    w = '400'
    h = '100'
    master.geometry('{}x{}'.format(w,h))
    master.attributes('-fullscreen', True)
    #w = Label(master, text="Hello, world!")
    #w = Label(master, textvariable=v, font=("Helvetica", 16), anchor=W, justify=LEFT) 
    wordString = StringVar()
    referenceString = StringVar()
    wrapperLength = getFontSize()*25
    #Label(master, textvariable=v).pack()
    wordLabel = Label(master, text=word, font=("Helvetica", getFontSize()), wraplength = wrapperLength, anchor=CENTER, justify=CENTER, pady=50, bd=10)
    referenceLabel = Label(master, text=reference, font=("Helvetica", getFontSize()-20), wraplength = wrapperLength, anchor=CENTER, justify=CENTER, bd=10)
    wordLabel.grid(column=0, row=0)
    referenceLabel.grid(column=0, row=5)
    master.columnconfigure(0, weight=1)
    master.rowconfigure(0, weight=1)
    #w.pack()
    text = autoMode()
    word = text[0]
    reference = text[1]
    #wordString.set(word)
    referenceString.set(reference)
    #master.after(60000, displayText())
    #_thread.start_new_thread(master.mainloop())
    
def Refresher():
    #global wordLabel
    text = autoMode()
    word = text[0]
    reference = text[1]
    wordLabel.configure(text=word)
    referenceLabel.configure(text=reference)
    master.after(1000, Refresher) # every second...

#master = Tk()
#Refresher()
displayText()
#displayText()
Refresher()
master.mainloop()
  
def delete(number):    
        conn = connect()
        cursor = conn.execute("DELETE FROM PRAYERS WHERE ID=(?)", (number,));
        conn.commit()
        conn.close()
        retrieve()

def createMultiple():
    filepath = input("type filepath: ")
    prayers = [line.strip() for line in open(filepath, 'r')]
    print (len(prayers))
    print ("thanks = t")
    print ("requests = r ")
    type = ""
    choice = input("option: ")
    if choice == "t":
       type = "thanks"
    if choice == "r":
       type = "requests"
    for aprayer in prayers:
        confirm = input("confirm : ")
        conn = connect()
        conn.execute("INSERT INTO PRAYERS (WHAT, TYPE) VALUES(?, ?)", (aprayer, type,));
        conn.commit()
        print ("prayer added successfully");
        conn.close()  


