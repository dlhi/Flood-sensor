import serial
import time
from tkinter import *
from datetime import datetime
import pyaudio
import wave
import os

PORT = "COM6"
BAUD = 9600
ser = serial.Serial(PORT,BAUD, timeout=None)
# Make a tkinter window
root = Tk()
# Restrict the user from resizing the GUI
root.resizable(width=False, height=False)
# log1, log2, and log3 are text boxes, must be global var in order to access in main as initialized in __init__
global running, alarm, floodStatus, stopAlarm, timeComparison, log1, log2, log3
# True if GUI is operational, false when terminated
running = True
# True if alarm is on, false otherwise
alarm = False
# True if alarm is stopped, false otherwise
stopAlarm = False
# True if flood is present, false otherwise
floodDetected = False

# The flood detectors out in the field
fd1 = "42.349992,-71.107870";

# Add the flood detectors to a list
listOfFloodDetectors = []
listOfFloodDetectors.append(fd1)

# Create the class for the GUI to run
class Application:

    def __init__(self):
        root.title("Flood Detector 1.0")
        self.color = StringVar()

        ft = Label(root, text="Flood Detector Status", bg="lightgreen", fg="black", font='None, 24')
        ft.grid(row=0, column=0, columnspan=3,sticky="WE")

        self.canvas = Canvas(root, width=340, height=120, bg="lightcyan")
        self.canvas.grid(row=1,column=0, columnspan=2, sticky="WE")

        self.oval_red = self.canvas.create_oval(10, 10, 110, 110, fill="white")
        self.oval_yellow = self.canvas.create_oval(120, 10, 220, 110, fill="white")
        self.oval_green = self.canvas.create_oval(230, 10, 330, 110, fill="white")

        self.color.set('G')
        self.canvas.itemconfig(self.oval_green, fill="green")

        fd = Label(root, text="Flood Detectors Deployed", bg="lightgreen", fg="black", font='None, 15')
        fd.grid(row=2, column=0, columnspan=3, sticky="WE")

        # make a text box to put the serial output
        global log1
        log1 = Text(root, width=50, height=8, takefocus=0, font="Calibri, 10")
        log1.grid(row=3, column=0, sticky="we")
        log1.insert(END, "Locations given in (LATITUDE, LONGITUDE).\n")
        # log1.insert(END, "Click coordinates to open in Google Maps.\n\n")
        log1.insert(END, "Flood Detector 1: " + fd1 + "\n")

        # make a scrollbar for textbox 1
        scrollbar1 = Scrollbar(root)
        # attach text box to scrollbar
        log1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.grid(row=3, column=1, sticky="ns")
        scrollbar1.config(command=log1.yview)

        fd = Label(root, text="Flood Detector Status", bg="lightgreen", fg="black", font='None, 15')
        fd.grid(row=4, column=0, columnspan=3, sticky="WE")

        global log2
        log2 = Text(root, width=50, height=8, takefocus=0, font="Calibri, 10")
        log2.grid(row=5, column=0, sticky="we")

        # make a scrollbar for textbox 2
        scrollbar2 = Scrollbar(root)
        # attach text box to scrollbar
        log2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.grid(row=5, column=1, sticky="ns")
        scrollbar2.config(command=log1.yview)

        one = Button(root, text="Exit", bg="red", fg="white", command = self.quit)
        one["height"] = 2  # set the height of the button to 2 characters tall
        one["width"] = 12  # set the button width to 12 characters wide
        one.grid(row=5,column=2,sticky="nesw")

        stop = Button(root, text="Stop Alarm", bg="yellow", fg="black", command=self.stopAlarmLoop)
        stop["height"] = 2  # set the height of the button to 2 characters tall
        stop["width"] = 12  # set the button width to 12 characters wide
        stop.grid(row=3, column=2, sticky="nswe")

        openFile = Button(root, text="Open File", bg="green", fg="black", command=self.openFileToScreen)
        openFile["height"] = 2  # set the height of the button to 2 characters tall
        openFile["width"] = 12  # set the button width to 12 characters wide
        openFile.grid(row=1, column=2, sticky="nswe")

        text1 = Label(root, text="Program Feed", bg="lightgreen", fg="black", font='None, 15')
        text1.grid(row=6, column=0, columnspan=3, sticky="WE")

        global log3
        log3 = Text(root, width=50, height=8, takefocus=0, font="Calibri, 10")
        log3.grid(row=7, column=0, sticky="we")

        # make a scrollbar for textbox 2
        scrollbar3 = Scrollbar(root)
        # attach text box to scrollbar
        log3.config(yscrollcommand=scrollbar3.set)
        scrollbar3.grid(row=7, column=1, sticky="ns")
        scrollbar3.config(command=log3.yview)

        filler = Label(root, bg="lightgreen")
        filler.grid(row=7, column=2, sticky="WESN")
        #
        # filler2 = Label(root, bg="lightgreen")
        # filler2.grid(row=1, column=2, sticky="WESN")

    def on_RadioChange(self, c):
        color = c

        if color == 'R':
            self.canvas.itemconfig(self.oval_red, fill="red")
            self.canvas.itemconfig(self.oval_yellow, fill="white")
            self.canvas.itemconfig(self.oval_green, fill="white")
        elif color == 'Y':
            self.canvas.itemconfig(self.oval_red, fill="white")
            self.canvas.itemconfig(self.oval_yellow, fill="yellow")
            self.canvas.itemconfig(self.oval_green, fill="white")
        elif color == 'G':
            self.canvas.itemconfig(self.oval_red, fill="white")
            self.canvas.itemconfig(self.oval_yellow, fill="white")
            self.canvas.itemconfig(self.oval_green, fill="green")

    def createNewFile(self):
        file = open("Flood_Detector.txt", 'a+')

        # Returns a string representing the date when flood detected
        _date = str(datetime.today())

        file.write("Flood Detector Application - Date Run: ")
        file.write(_date + '\n')

        file.close()

        with open('Flood_Detector_ToREAD.txt', 'a+') as output, open('Flood_Detector.txt', 'r') as input:
            while True:
                data = input.read(100000)
                if data == '':  # end of file reached
                    break
                output.write(data)

    def quit(self): #define the function to kill the program
        global running
        running = False

    def playAlarm(self):
        chunk = 1024
        # open the file for reading.
        wf = wave.open('alarm.wav', 'rb')

        # create an audio object
        p = pyaudio.PyAudio()

        # open stream based on the wave object which has been input.
        stream = p.open(format=
                        p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read data (based on the chunk size)
        data = wf.readframes(chunk)
        check = True
        # play stream (looping from beginning of file to the end)

        t_end = time.time() + 3

        while data != '' and time.time() < t_end:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(chunk)
            root.update()

        # cleanup stuff.
        stream.close()
        p.terminate()

    # False when alarm is off, true when alarm is on
    def stopAlarmStatus(self):
        global alarm
        alarm = False

    # True if no flood, false if flood
    def floodStatusChange(self, str):
        global floodDetected
        if str == 't':
            floodDetected = True

        if str == 'f':
            floodDetected = False

    def stopAlarmLoop(self):
        global stopAlarm
        stopAlarm = True

    def openFileToScreen(self):
        os.system('Flood_Detector.txt')

# Initialize the GUI
a = Application()
# Create a new Flood_Detector.txt if not created already
a.createNewFile()
file = open("Flood_Detector.txt", 'a+')

# After x time, the access point will poll the flood detector and check to see if it is operational
start = time.time()
# Variable to sent to check if flood detector is still functional
polling = 1

# Variable to reset polling in textbox 3 to reduce cluttering of text
timesToPoll = 0

while running:
    # Must update the GUI regularly
    root.update()
    # Check to see if flood detector sent anything

    if ser.inWaiting() > 0:
        # If so, read and decode the message and check its contents
        myData = ser.readline()
        string = str(myData.decode().strip('\r\n'))

        print(string)
        # If there is a flood, read-in data should snot be a '0' char; if so, then there is no flood
        if string != '0':
            # Decode data and strip excess characters
            file.write(myData.decode('utf-8').strip('\r\n'))
            # Write into the file the time flood was detected
            file.write(" Time: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\n')
            a.on_RadioChange('R')
            a.floodStatusChange('t')

            floodCoord = myData[2:]
            floodHeight = myData[0]
            for floodCoord in listOfFloodDetectors:
                log2.insert(END, "Flood detected at: " + floodCoord + '\n')
                log2.insert(END, "The height is at: " + str((int(floodHeight) - 48) * 6) + " inches.\n\n")
                log2.see("end")


            # If button has been pressed, keep the alarm off
            # There must be two phases as the button command only works once, must be kept off or the main
            #   while loop will keep the alarm on
            alarm = True

            # When flood is detected for the first time, keep playing alarm until the stop-button is pressed by user
            if alarm and floodDetected and not stopAlarm:
                a.playAlarm()

            # Time ending constant to check if flood has receded
            if stopAlarm:
                time.sleep(1)

        elif string == '0':
            a.floodStatusChange('f')
            a.on_RadioChange('G')
            stopAlarm = False

    # This checks if the flood detector is connected
    # If connected, the exception will print: this means that the flood detector is connected
    # If the try code runs, this means that the flood detector is not connected
    #   The light will be changed to yellow, indicating a disconnected flood detector
    else:
        # Test the port
        print("Testing Serial Port ... ")
        ser.write(str(chr(polling)).encode())
        print("Serial Data Sent")
        time.sleep(1.5)
        if ser.inWaiting() > 0:
            log2.delete(1.0, 'end')
            print("Online")
            log3.insert(END, fd1 + " is online!\n")
            log3.see("end")
        else:
            print("Offline")
            a.on_RadioChange('Y')
            log2.insert(END, "The flood detector at: " + fd1 + " is offline.\n")
            log2.see("end")


    end = time.time()

    # In order to poll, x time must have passed, the alarm should not be on, and there should not be a flood detected
    #   nor a deactivated flood detector
    if end - start > 3 and not alarm and not floodDetected:
        print("Sending Serial Data ... ")
        log3.insert(END, "Sending Serial Data ... \n")
        ser.write(str(chr(polling)).encode())
        print("Serial Data Sent")
        log3.insert(END, "Serial Data Sent ... \n\n")
        start = time.time()
        timesToPoll+=1
        if(timesToPoll == 15):
            timesToPoll = 0;
            log3.delete(1.0, END)
            log3.insert(END, "Resetting ... \n\n")
        log3.see("end")

ser.close() #close the serial communication
file.close() # Close the file
root.destroy() #destroy the GUI
