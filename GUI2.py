from tkinter import *
from tkinter import filedialog
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
CHECKBOX_COL = 0
INDEX_COL = 1
EXHIBIT_COL = 2
BROWSE_BTN_COL = 3
FILE_COL = 4
ZERO = 0

class AudioButton(Button):
    def __init__(self, master=None):
        super().__init__(master)

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
        self.run_btn = Button(self,text="RUN", style='PlayButton.TButton')
        self.run_btn.grid(row=19,column=1,pady=(20, 0))
        self.run_btn.configure(state="disabled")

        self.stop_btn = Button(self,text="STOP", style='StopButton.TButton')
        self.stop_btn.grid(row=19,column=2,pady=(20, 0))
        self.stop_btn.configure(state="disabled")

        self.clear_btn = Button(self,text="CLEAR")
        self.clear_btn.grid(row=19,column=3,pady=(20, 0))
        self.clear_btn.configure(state="disabled")

        self.clearall_btn = Button(self,text="CLEAR ALL")
        self.clearall_btn.grid(sticky="W", row=19,column=4,pady=(20, 0))
        self.clearall_btn.configure(state="disabled")

    def uploadAudioFile(self, file_num):
        chosen_file = filedialog.askopenfilename(filetypes = (("Sound Files",".wav"),("All Files","*.*") ))

        # Assign new file name
        self.fileDict[file_num] = Label(self, text=chosen_file)
        self.fileDict[file_num].grid(sticky="W", row=(file_num + 1), column=FILE_COL)

        # Switch state on according checkbox
        self.enableDict[file_num].config(state="normal")
        self.enableDict[file_num].state(['selected'])        

        # Since the user has uploaded at least one file, give them the ability to run the program
        self.run_btn.configure(state="enabled")

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
