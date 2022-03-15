import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from os import system, name
import os
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from time import sleep
import warnings
import sys,os,msvcrt,csv
from datetime import datetime
import pandas as pd

def writeNewDev(deviceID,UIN):
    filename = 'C:\devicesAll.csv'
    os.chmod(filename,S_IWUSR|S_IREAD)#make file writable
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Device ID','Device Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'Device ID': deviceID,'Device Type':UIN})
    os.chmod(filename,S_IREAD|S_IRGRP|S_IROTH)#lock file

def logNewDevice():
    system("cls")
    print("Preparing to register new device..")
    sleep(2)
    newDevice = capWeb()
    system("cls")
    print("Please type a device identifier (e.g. 'Dell XPS 13 7930')")
    UIN = input("")
    writeNewDev(newDevice,UIN)

def readUIN():
    system("cls")
    UIN = input("Please swipe card or type 'register' to register a new device\n")
    return UIN
    
def readTicketNum():
    system("cls")
    netID = input("Please enter Ticket Number\n")
    return netID

def capWeb():
    system("cls")
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
    filename = "C:/devicesOut.csv"
    os.chmod(filename,S_IWUSR|S_IREAD)#make file writable
    df = pd.read_csv(filename)
    df.to_csv(filename, index=False)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['User UIN', 'Device ID', 'Ticket Number', 'Log Date + Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'User UIN': UINStr,'Device ID': deviceID, 'Ticket Number': ticketNum,'Log Date + Time': str(datetime.now())})
    os.chmod(filename,S_IREAD|S_IRGRP|S_IROTH)#lock file
    
def writeDevIn(deviceID):
    filename = "C:/devicesOut.csv"
    filename2 = "C:/devicesOutEdited.csv"
    os.chmod(filename,S_IWUSR|S_IREAD)#make file writable
    df = pd.read_csv(filename)
    df.to_csv(filename, index=False)
    with open('C:/devicesOut.csv', 'r') as csvfile, open('C:/devicesOutEdited.csv', 'w') as csvedit:
        writer = csv.writer(csvedit)
        for row in csv.reader(csvfile):
            if row[1] != deviceID:
                writer.writerow(row)
    os.remove(filename)
    os.rename(filename2,filename)
    os.chmod(filename,S_IREAD|S_IRGRP|S_IROTH)#lock file

def writeCSV(UINStr, deviceID, ticketNum, inOrOut):
    filename = "C:/devicesLog.csv"
    os.chmod(filename,S_IWUSR|S_IREAD)#make file writable
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['User UIN', 'Device ID', 'Device In/Out', 'Ticket Number', 'Log Date + Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'User UIN': UINStr,'Device ID': deviceID,'Device In/Out': inOrOut,'Ticket Number': ticketNum,'Log Date + Time': str(datetime.now())})
    os.chmod(filename,S_IREAD|S_IRGRP|S_IROTH)#lock file
    
def inOutPrompt():
    while True:
        system("cls")
        print("Is this device coming in or going out? (Type 'i' or 'o')\n")
        getch2 = msvcrt.getch()
        getchIn = str(getch2)[2:len(str(getch2))-1]
        if(getchIn == "i" or getchIn == "o"):
            system("cls")
            return getchIn
        else:
            system("cls")
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
        if(inOrOut == "i"):
            print(UINString+" is checking in "+ deviceIDString+" under ticket number " + ticketNumber+"\n")
            print("Press enter to continue or 'r' to try again if the info above is not correct\n")
        else:
            print(UINString+" is checking out "+ deviceIDString+" under ticket number " + ticketNumber+"\n")
            print("Press enter to continue or 'r' to try again if the info above is not correct\n")
        getch2 = msvcrt.getch() 
        getchIn = str(getch2)[2:len(str(getch2))-1]
        if (getchIn != "r"):
            if(inOrOut == "o"):
                writeDevOut(UINString,deviceIDString,ticketNumber)
            else:
                writeDevIn(deviceIDString)
            writeCSV(UINString,deviceIDString,ticketNumber, inOrOut)
        else:
            system("cls")
        
def main():
    while True:
        tryThis()
    
if __name__ == '__main__':
    main()