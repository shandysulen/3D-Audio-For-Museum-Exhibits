from tkinter import *
from tkinter.ttk import *
import socket
import sys
import random
import pyaudio
import hrtf

# Globals
NUM_EXHIBITS = 16
EXHIBIT_NAMES = ["Entrance", "School Lunch", "Holidays", "Restaurants",
                "Formals", "Events", "Import", "Staples", "Commissary",
                "Commissary", "Construction", "Trouble", "Meals To Go",
                "Cultural", "Panama", "Unique"]

class AudioButton(Button):
    def __init__(self, master=None):
        super().__init__(master)

class ExhibitTable(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Initialize empty file dictionary, button dictionary, and enable dictionary
        self.fileDict = {}
        self.buttonDict = {}
        self.enableDict = {}

        # Set headers
        self.index_header = Label(self,text="Number", font='Helvetica 10 bold')
        self.index_header.grid(row=1,column=0)
        self.exhibit_header = Label(self,text="Exhibit Name", font='Helvetica 10 bold')
        self.exhibit_header.grid(row=1,column=1)
        self.filename_header = Label(self,text="Audio File", font='Helvetica 10 bold')
        self.filename_header.grid(row=1,column=2)
        self.enable_header = Label(self,text="Enable", font='Helvetica 10 bold')
        self.enable_header.grid(row=1,column=3)

        # Generate index labels and exhibit names
        for row in range(NUM_EXHIBITS):
            Label(self, text=str(row+1)).grid(row=(row+2), column=0)
            Label(self, text=EXHIBIT_NAMES[row]).grid(row=(row+2), column=1)
            self.fileDict[row+1] = Button(self,text="Select Audio",command=self.uploadAudioFile).grid(row=(row+2),column=2)
            print(self.fileDict[row+1])

        # Create style for ttk buttons
        style = Style()
        style.configure("TButton", foreground="green", background="white", relief="flat")

        # Main Functionality
        self.run = Button(self,text="RUN")
        self.run.grid(row=19,column=0,pady=(20, 0))

        self.stop = Button(self,text="STOP")
        self.stop.grid(row=19,column=1,pady=(20, 0))

        self.clear = Button(self,text="CLEAR")
        self.clear.grid(row=19,column=2,pady=(20, 0))

        self.clearall = Button(self,text="CLEAR ALL")
        self.clearall.grid(row=19,column=3,pady=(20, 0))

    def uploadAudioFile(self):
        master.fileName = filedialog.askopenfilename(filetypes = (("Sound Files",".wav"),("All Files","*.*") ))
        print(master.fileName)
        log.insert(END,"File is uploaded from"+master.fileName+"\n")

class Log(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.log = Text(self,height=20,width=40)
        self.log.pack(fill=Y)
        self.log.configure(state="disabled")

    def insertToLog(self, text):
        self.log.configure(state="normal")
        self.log.insert(END, text + "\n")
        self.log.configure(state="disabled")

if __name__ == '__main__':

    # Set title & icon
    root = Tk()
    root.title("3D Audio for Museum Exhibits")
    root.iconbitmap('images\logo.ico')

    # Create exhibit table
    exhibit_table = ExhibitTable(root)
    exhibit_table.pack(side=LEFT, padx=20, pady=20)

    # Create log
    log = Log(root)
    log.pack(side=LEFT, padx=20)

    # Successfully write to log
    log.insertToLog("Localization Machine Booted...")

    # Run app forever
    root.mainloop()
