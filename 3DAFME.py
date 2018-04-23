from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import socket
import sys
import random
import pyaudio
import hrtf
import time
from datetime import datetime
from scipy.spatial import distance
from multiprocessing.pool import ThreadPool
import threading
import os
import UDPClient
import math

# Globals
NUM_EXHIBITS = 16
EXHIBIT_NAMES = ["Entrance", "School Lunch", "Holidays", "Restaurants",
                "Formals", "Events", "Import", "Staples", "Commissary",
                "Commissary", "Construction", "Trouble", "Meals To Go",
                "Cultural", "Panama", "Unique"]
EXHIBIT_COORD = [(0,0), (0,8.375), (0,16.75), (0,25.125),
                (0,33.5), (0,41.875), (0, 50.25), (0,58.625), (0,67),
                (0,75.375), (0,83.75), (0,92.125), (0,100.5),
                (0,108.875), (0,117.25), (0,125.635)]
CHECKBOX_COL = 0
INDEX_COL = 1
EXHIBIT_COL = 2
BROWSE_BTN_COL = 3
FILE_COL = 4

def getDistFromOrigin(x, y):
    return math.sqrt(math.pow(x,2) + math.pow(y,2))

def printHelloWorld():
    print("Hello World")
    return

class Log(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.log = Text(self,height=20,width=60)
        self.log.pack(fill=Y)
        self.log.configure(state="disabled")

    def insertToLog(self, text):
        self.log.configure(state="normal")
        self.log.insert(END,"[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "] " + text + "\n")
        self.log.configure(state="disabled")

class ExhibitTable(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Initialize empty file dictionary, button dictionary, and enable dictionary
        self.fileDict = {}
        self.buttonDict = {}
        self.varDict = {}
        self.enableDict = {}

        # Set headers
        self.index_header = Label(self,text="Number", font='Helvetica 10 bold')
        self.index_header.grid(row=1,column=INDEX_COL)
        self.exhibit_header = Label(self,text="Exhibit Name", font='Helvetica 10 bold')
        self.exhibit_header.grid(row=1,column=EXHIBIT_COL)
        self.filename_header = Label(self,text="Audio File", font='Helvetica 10 bold')
        self.filename_header.grid(row=1, column=BROWSE_BTN_COL)

        # Generate index labels, exhibit names, enable checkboxes, browse buttons, and file names
        for row in range(NUM_EXHIBITS):
            Label(self, text=str(row+1)).grid(row=(row+2), column=INDEX_COL)
            Label(self, text=EXHIBIT_NAMES[row]).grid(row=(row+2), column=EXHIBIT_COL)
            self.fileDict[row+1] = Label(self, text="")
            self.fileDict[row+1].grid(sticky="W", row=(row+2), column=FILE_COL)
            self.buttonDict[row+1] = Button(self,text="Browse")
            self.buttonDict[row+1].grid(row=(row+2),column=BROWSE_BTN_COL)
            self.varDict[row+1] = BooleanVar()
            self.enableDict[row+1] = Checkbutton(self, variable=self.varDict[row+1], state="disabled")
            self.enableDict[row+1].grid(sticky="E", row=(row+2), column=CHECKBOX_COL)

        # command=lambda: self.uploadAudioFile(row+1)
        self.buttonDict[1].config(command=lambda: self.uploadAudioFile(1))
        self.buttonDict[2].config(command=lambda: self.uploadAudioFile(2))
        self.buttonDict[3].config(command=lambda: self.uploadAudioFile(3))
        self.buttonDict[4].config(command=lambda: self.uploadAudioFile(4))
        self.buttonDict[5].config(command=lambda: self.uploadAudioFile(5))
        self.buttonDict[6].config(command=lambda: self.uploadAudioFile(6))
        self.buttonDict[7].config(command=lambda: self.uploadAudioFile(7))
        self.buttonDict[8].config(command=lambda: self.uploadAudioFile(8))
        self.buttonDict[9].config(command=lambda: self.uploadAudioFile(9))
        self.buttonDict[10].config(command=lambda: self.uploadAudioFile(10))
        self.buttonDict[11].config(command=lambda: self.uploadAudioFile(11))
        self.buttonDict[12].config(command=lambda: self.uploadAudioFile(12))
        self.buttonDict[13].config(command=lambda: self.uploadAudioFile(13))
        self.buttonDict[14].config(command=lambda: self.uploadAudioFile(14))
        self.buttonDict[15].config(command=lambda: self.uploadAudioFile(15))
        self.buttonDict[16].config(command=lambda: self.uploadAudioFile(16))

        # Create style for ttk buttons
        style = Style()
        style.configure('PlayButton.TButton', foreground='green')
        style.configure('StopButton.TButton', foreground='red')

        # Main Functionality
        self.start_btn = Button(self,text="RUN", style='PlayButton.TButton')
        self.start_btn.grid(row=19,column=1,pady=(20, 0))
        self.start_btn.configure(state="disabled")

        self.stop_btn = Button(self,text="STOP", style='StopButton.TButton')
        self.stop_btn.grid(row=19,column=2,pady=(20, 0))
        self.stop_btn.configure(state="disabled")

    def uploadAudioFile(self, file_num):
        chosen_file = filedialog.askopenfilename(filetypes = (("Sound Files",".wav"),("All Files","*.*") ))

        # Assign new file name
        self.fileDict[file_num] = Label(self, text=chosen_file)
        self.fileDict[file_num].grid(sticky="W", row=(file_num + 1), column=FILE_COL)

        # Switch state on according checkbox
        self.enableDict[file_num].config(state="normal")
        self.enableDict[file_num].state(['selected'])

        # Since the user has uploaded at least one file, give them the ability to run the program
        self.start_btn.configure(state="enabled")

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Create exhibit table
        self.exhibit_table = ExhibitTable(self)
        self.exhibit_table.pack(side=LEFT, padx=20, pady=20)

        # Create log
        self.log = Log(self)
        self.log.pack(side=LEFT, padx=20, pady=20)

        # Hook up the run function to the run button
        self.exhibit_table.start_btn.config(command=lambda: self.start())
        self.exhibit_table.stop_btn.config(command=lambda: self.stop())

    def start(self):

        # Get start time
        self.start_time = time.time()

        # Enable/disable buttons
        self.exhibit_table.stop_btn.configure(state="enabled")
        self.exhibit_table.start_btn.configure(state="disabled")

        # Successfully write to log
        self.log.insertToLog("Localization Machine Booted...")

        # Show the user's location in real-time
        os.system('python canvas.py')

        # Connect to Dashboard
        self.log.insertToLog("Establishing connection with Dashboard...")
        host = '127.0.0.1'
        port = 10000
        beacon_add = 23
        self.udp = UDPClient.udp_factory(host, port, beacon_add)
        self.log.insertToLog("Connection successfully established with Dashboard...")

        soundToPlay = []
        interval = 0.1
        pool = ThreadPool(processes=1)

        # Play 3D audio
        while True:

            # GET USER LOCATION FROM SENSOR
            try:
                async_result = pool.apply_async(self.udp.request_position)
                time.sleep(interval)
                user_loc = async_result.get()
            except OSError as e:
                print(e)

            # scale the sound's volume according to distance from exhibit
            # origin_dist = getDistFromOrigin(user_loc[0], user_loc[1])
            # print(origin_dist)

            # TEMPORARY VALUE

            # for i in range(1, NUM_EXHIBITS):
            #     if self.exhibit_table.enableDict[i].state()[0] == 'selected':
            #
            #         # scale the sound's volume according to distance from exhibit
            #         dist_from_exhibit = distance.euclidean(user_loc, EXHIBIT_COORD[i-1])
            #
            #         # Threshold for each exhibit distance
            #         if dist_from_exhibit < 5.0:
            #
            #             # GET AINDEX AND EINDEX based off user's orientation in regards to those exhibits
            #
            #             # TEMPORARY VALUES
            #             aIndex = 0 # To the left
            #             eIndex = 8 # About eye level
            #             sound = hrtf.hrtf(fileDict[i], aIndex, eIndex)
            #
            #             # scale the sound's volume using dist_form exhibit
            #             scale = 1 - 0.2 * dist_from_exhibit
            #             sound *= scale
            #
            #             soundToPlay = sound

        # Close UDP sockets
        self.log.insertToLog("Closing connection with Dashboard...")

    def stop(self):

        self.udp.close()

        # Get stop time
        self.stop_time = time.time()

        self.log.insertToLog("Shutting down Localization Machine...")
        self.log.insertToLog("Session Time: " + str(round(self.stop_time - self.start_time, 2)) + " seconds")

        # Enable/disable buttons
        self.exhibit_table.stop_btn.configure(state="disabled")
        self.exhibit_table.start_btn.configure(state="enabled")


if __name__ == '__main__':

    # Set title & icon
    root = Tk()
    root.title("3D Audio for Museum Exhibits")
    root.iconbitmap('images\logo.ico')

    # Create app
    app = Application(root)
    app.pack()

    # Run app forever
    root.mainloop()
