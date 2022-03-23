import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import os
from os import system, name
from time import sleep
import warnings
import sys,tty,termios,csv
from datetime import datetime
import pandas as pd

def getch(char_width=1):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(char_width)
    finally:
        termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
    return ch

def writeNewDev(deviceID,UIN):
    filename = '/Volumes/devicesAll.csv'
    os.system('chflags nouchg {}'.format(filename))#make file writeable
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Device ID','Device Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'Device ID': deviceID,'Device Type':UIN})
    os.system('chflags uchg {}'.format(filename))#make file non writeable

def logNewDevice():
    system("clear")
    print("Preparing to register new device..")
    sleep(2)
    newDevice = capWeb()
    system("clear")
    print("Please type a device identifier (e.g. 'Dell XPS 13 7930')")
    UIN = input("")
    writeNewDev(newDevice,UIN)

def readUIN():
    system("clear")
    UIN = input("Please swipe card or type 'register' to register a new device\n")
    return UIN
    
def readTicketNum():
    system("clear")
    netID = input("Please enter Ticket Number\n")
    return netID

def capWeb():
    system("clear")
    print("Scan the QR code on the bottom of your device when the window pops up")
    warnings.filterwarnings("ignore")
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_PLAIN
    x = True
    while x:
        _, frame = cap.read()
        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            #cv2.putText(frame, str(obj.data), (50, 50), font, 2,(255, 0, 0), 3)
            x = False
        frame = cv2.flip(frame,1)
        cv2.imshow("frame",frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    stringOut = str(obj.data)[2:len(str(obj.data))-1]
    return stringOut

def writeDevOut(UINStr, deviceID, ticketNum):
    filename = "/Volumes/devicesOut.csv"
    os.system('chflags nouchg {}'.format(filename))#make file writeable
    df = pd.read_csv(filename)
    df.to_csv(filename, index=False)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['User UIN', 'Device ID', 'Ticket Number', 'Log Date + Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'User UIN': UINStr,'Device ID': deviceID, 'Ticket Number': ticketNum,'Log Date + Time': str(datetime.now())})
    os.system('chflags uchg {}'.format(filename))#make file non writeable
    
def writeDevIn(deviceID):
    filename = "/Volumes/devicesOut.csv"
    filename2 = "/Volumes/devicesOutEdited.csv"
    os.system('chflags nouchg {}'.format(filename))#make file writeable
    df = pd.read_csv(filename)
    df.to_csv(filename, index=False)
    with open('/Volumes/devicesOut.csv', 'r') as csvfile, open('/Volumes/devicesOut.csv', 'w') as csvedit:
        writer = csv.writer(csvedit)
        for row in csv.reader(csvfile):
            if row[1] != deviceID:
                writer.writerow(row)
    os.remove(filename)
    os.rename(filename2,filename)
    os.system('chflags uchg {}'.format(filename))#make file non writeable

def writeCSV(UINStr, deviceID, ticketNum, inOrOut):
    filename = "/Volumes/devicesLog.csv"
    os.system('chflags nouchg {}'.format(filename))#make file writeable
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['User UIN', 'Device ID', 'Device In/Out', 'Ticket Number', 'Log Date + Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'User UIN': UINStr,'Device ID': deviceID,'Device In/Out': inOrOut,'Ticket Number': ticketNum,'Log Date + Time': str(datetime.now())})
    os.system('chflags uchg {}'.format(filename))#make file non writeable
    
def inOutPrompt():
    while True:
        system("clear")
        print("Is this device coming in or going out? (Type 'i' or 'o')\n")
        getch2 = getch()
        if(getch2 == 'i' or getch2 == 'o'):
            system("clear")
            return getch2
        else:
            system("clear")
            print("Wrong input, type either 'i' or 'o' with no quotes\n")
            input("Press any key to try again...")

def tryThis():
    UINString = readUIN()
    if(UINString == "register"):
        logNewDevice()
    else:
        deviceIDString = capWeb()
        ticketNumber = readTicketNum()
        inOrOut = inOutPrompt()
        if(inOrOut == 'i'):
            print(UINString+" is checking in "+ deviceIDString+" under ticket number " + ticketNumber+"\n")
            print("Press enter to continue or 'r' to try again if the info above is not correct\n")
        else:
            print(UINString+" is checking out "+ deviceIDString+" under ticket number " + ticketNumber+"\n")
            print("Press enter to continue or 'r' to try again if the info above is not correct\n")
        getch2 = getch() 
        if (getch2 != 'r'):
            if(inOrOut == 'o'):
                writeDevOut(UINString,deviceIDString,ticketNumber)
            else:
                writeDevIn(deviceIDString)
            writeCSV(UINString,deviceIDString,ticketNumber, inOrOut)
        else:
            system("clear")
        
def main():
    while True:
        tryThis()
    
if __name__ == '__main__':
    main()