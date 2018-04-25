from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import socket
import sys
import random
import pyaudio
from hrtf import hrtf
import time
from datetime import datetime
from scipy.spatial import distance
from multiprocessing.pool import ThreadPool
import threading
import os
import UDPClient
import math
import numpy as np
from audiostream3D import AudioStream3D
from queue import Queue
q = Queue(1)

# Globals
NUM_EXHIBITS = 16
EXHIBIT_NAMES = ["Entrance", "School Lunch", "Holidays", "Restaurants",
                "Formals", "Events", "Import", "Staples", "Commissary",
                "Commissary", "Construction", "Trouble", "Meals To Go",
                "Cultural", "Panama", "Unique"]
EXHIBIT_COORD = [0, 108, 270, 404,
                564, 728, 890, 1051, 1228,
                1640, 1812, 1978, 2131,
                2326, 2500, 2674]
CHECKBOX_COL = 0
INDEX_COL = 1
EXHIBIT_COL = 2
BROWSE_BTN_COL = 3
FILE_COL = 4
EXHIBIT_Y = 300
stop_event = threading.Event()

# global user_loc

def getDistFromOrigin(x, y):
    return math.sqrt(math.pow(x,2) + math.pow(y,2))

def getDistFromExhibit(mobilex, mobiley, exhx, exhy):
    return math.sqrt(math.pow(mobilex - exhx, 2) + math.pow(mobiley - exhy,2))

class StreamThread(threading.Thread):
    def __init__(self, name, counter, app):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter
        self.app = app

        # Stream Config
        self.CHUNK = 1048576 # 2^16
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 2
        self.FRAMERATE = 44100

        # When no sounds are playing, return the zero array
        self.zeros_2channel = np.array([[0] * self.CHUNK, [0] * self.CHUNK], dtype='float32').T.tobytes()
        self.aIndex = 0
        self.increaseFlag = True

    def run(self):
        self.prog_start()

    def HRTFUpdate(self):
        """
        Updates the audio data based on the new azimuth and elevation of the user in realtime
        """
        self.fileName = q.get()
        print("Entering HRTF - received " + str(self.fileName))
        if self.fileName == None:
            print("Returning zeros...")
            return self.zeros_2channel
        else:

            # Mess with aIndex
            if self.aIndex == 24:
                self.increaseFlag = False
            elif self.aIndex == 0:
                self.increaseFlag = True

            if self.increaseFlag:
                self.aIndex += 1
            else:
                self.aIndex -= 1

            # Return soundToPlay audio file
            soundToPlay = hrtf(q.get(), self.aIndex, 8)
            print("Playing " + self.fileName + "...")
            return soundToPlay.tobytes()

    def prog_start(self):
        try:
            # Instantiate PyAudio
            p = pyaudio.PyAudio()

            # Instantiate a threading pool
            pool = ThreadPool(processes=1)

            # Open stream using callback
            stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.FRAMERATE, output=True)

            # Initialize current position in audio data and get first chunk
            self.currentPos = 0

            data = self.HRTFUpdate()
            data_chunk = data[self.currentPos:self.currentPos + self.CHUNK]

            while True:
                if stop_event.is_set():
                    break
                # Asynchronously call HRTF thread
                async_result = pool.apply_async(self.HRTFUpdate)

                # Play sound
                stream.write(data_chunk)

                # Update position in data
                self.currentPos += self.CHUNK

                # Retrieve the updated audio data
                try:
                    data = async_result.get()
                    if data == self.zeros_2channel:
                        self.currentPos = 0
                except IndexError:
                    break

                # Get new chunk of audio data to be streamed
                data_chunk = data[self.currentPos:self.currentPos + self.CHUNK]

            # Stop stream and PyAudio
            stream.stop_stream()
            stream.close()
            p.terminate()

        except Exception as e:
            print(e)

        return

class LocationThread(threading.Thread):
    def __init__(self, name, counter, app):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter
        self.app = app

    def run(self):
        self.prog_start()

    def prog_start(self):

        # Connect to Dashboard
        self.app.log.insertToLog("Establishing connection with Dashboard...")
        host = '127.0.0.1'
        port = 10000
        beacon_add = 23
        self.udp = UDPClient.udp_factory(host, port, beacon_add)
        self.app.log.insertToLog("Connection successfully established with Dashboard...")

        # Set sleep interval
        interval = 0.1

        # Get location data from Dashboard modem
        while True:
            try:
                if stop_event.is_set():
                    break
                else:
                    # global user_loc
                    user_loc = self.udp.request_position()
                    distance = None
                    fileName = None
                    for i in range(NUM_EXHIBITS):
                        if self.app.exhibit_table.enableDict[i+1].state()[0] == 'selected' and getDistFromExhibit(user_loc[0], user_loc[1], EXHIBIT_COORD[i], 300) < 200:
                            distance = getDistFromExhibit(user_loc[0], user_loc[1], EXHIBIT_COORD[i], 300)
                            fileName = self.app.exhibit_table.fileDict[i+1]["text"]
                            print(self.name, user_loc, distance, EXHIBIT_NAMES[i], fileName)
                            break
                    q.put(fileName)
                    if fileName == None:
                        print(self.name, user_loc, "not in range of selected exhibit")                    
            except OSError as e:
                print("Oh no something happened!!")
                print(e)

        # Close UDP socket
        self.udp.close()
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

        # Clear the stop event for threads
        stop_event.clear()

        # Enable/disable buttons
        self.exhibit_table.stop_btn.configure(state="enabled")
        self.exhibit_table.start_btn.configure(state="disabled")

        # Successfully write to log
        self.log.insertToLog("Localization Machine Booted...")

        # Start networking thread
        self.location_thread = LocationThread("location", 1, self)
        self.location_thread.start()

        self.stream_thread = StreamThread("stream", 1, self)
        self.stream_thread.start()

    def stop(self):

        stop_event.set()

        # Close UDP sockets
        self.log.insertToLog("Closing connection with Dashboard...")

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
