from tkinter import *
import socket
import sys
import random
import pyaudio
import hrtf

# Globals
NUM_EXHIBITS = 16

class ExhibitTable(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Set headers
        self.index = Label(self,text="Number")
        self.index.grid(row=1,column=0)
        self.exhibit = Label(self,text="Exhibit Name")
        self.exhibit.grid(row=1,column=1)
        self.filename = Label(self,text="Audio File")
        self.filename.grid(row=1,column=2)
        self.status = Label(self,text="Status")
        self.status.grid(row=1,column=3)

        # Set index numbers
        i1=Label(self,text="1")
        i2=Label(self,text="2")
        i3=Label(self,text="3")
        i4=Label(self,text="4")
        i5=Label(self,text="5")
        i6=Label(self,text="6")
        i7=Label(self,text="7")
        i8=Label(self,text="8")
        i9=Label(self,text="9")
        i10=Label(self,text="10")
        i11=Label(self,text="11")
        i12=Label(self,text="12")
        i13=Label(self,text="13")
        i14=Label(self,text="14")
        i15=Label(self,text="15")
        i16=Label(self,text="16")

        # Place index numbers on the grid
        i1.grid(row=2,column=0)
        i2.grid(row=3,column=0)
        i3.grid(row=4,column=0)
        i4.grid(row=5,column=0)
        i5.grid(row=6,column=0)
        i6.grid(row=7,column=0)
        i7.grid(row=8,column=0)
        i8.grid(row=9,column=0)
        i9.grid(row=10,column=0)
        i10.grid(row=11,column=0)
        i11.grid(row=12,column=0)
        i12.grid(row=13,column=0)
        i13.grid(row=14,column=0)
        i14.grid(row=15,column=0)
        i15.grid(row=16,column=0)
        i16.grid(row=17,column=0)

        # Set names for each index
        name1 = Label(self,text="Entrance")
        name2 = Label(self,text="School Lunch")
        name3 = Label(self,text="Holidays")
        name4 = Label(self,text="Restaurants")
        name5 = Label(self,text="Formals")
        name6 = Label(self,text="Events")
        name7 = Label(self,text="Import")
        name8 = Label(self,text="Staples")
        name9 = Label(self,text="Commissary")
        name10 = Label(self,text="Commissary")
        name11 = Label(self,text="Construction")
        name12 = Label(self,text="Trouble")
        name13 = Label(self,text="Meals to go")
        name14 = Label(self,text="Cultural")
        name15 = Label(self,text="Panama")
        name16 = Label(self,text="Unique")

        # Place the names on the grid
        name1.grid(row=2,column=1)
        name2.grid(row=3,column=1)
        name3.grid(row=4,column=1)
        name4.grid(row=5,column=1)
        name5.grid(row=6,column=1)
        name6.grid(row=7,column=1)
        name7.grid(row=8,column=1)
        name8.grid(row=9,column=1)
        name9.grid(row=10,column=1)
        name10.grid(row=11,column=1)
        name11.grid(row=12,column=1)
        name12.grid(row=13,column=1)
        name13.grid(row=14,column=1)
        name14.grid(row=15,column=1)
        name15.grid(row=16,column=1)
        name16.grid(row=17,column=1)

        # Create buttons
        b1 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b2 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b3 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b4 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b5 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b6 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b7 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b8 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b9 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b10 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b11 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b12 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b13 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b14 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b15 = Button(self,text="Select Audio",command=self.uploadAudioFile)
        b16 = Button(self,text="Select Audio",command=self.uploadAudioFile)

        # Place buttons on grid
        b1.grid(row=2,column=2)
        b2.grid(row=3,column=2)
        b3.grid(row=4,column=2)
        b4.grid(row=5,column=2)
        b5.grid(row=6,column=2)
        b6.grid(row=7,column=2)
        b7.grid(row=8,column=2)
        b8.grid(row=9,column=2)
        b9.grid(row=10,column=2)
        b10.grid(row=11,column=2)
        b11.grid(row=12,column=2)
        b12.grid(row=13,column=2)
        b13.grid(row=14,column=2)
        b14.grid(row=15,column=2)
        b15.grid(row=16,column=2)
        b16.grid(row=17,column=2)

        # Main Functionality
        self.run = Button(self,text="RUN",bg="green",fg="black")
        self.run.grid(row=19,column=0)

        self.stop = Button(self,text="STOP",bg="red",fg="black")
        self.stop.grid(row=19,column=1)

        self.clear = Button(self,text="CLEAR")
        self.clear.grid(row=19,column=2)

        self.clearall = Button(self,text="CLEAR ALL")
        self.clearall.grid(row=19,column=3)

    def uploadAudioFile(self):
        master.fileName = filedialog.askopenfilename(filetypes = (("Sound Files",".wav"),("All Files","*.*") ))
        print(master.fileName)
        log.insert(END,"File is uploaded from"+master.fileName+"\n")

class Log(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.log = Text(self,height=20,width=40)
        self.log.pack(fill=Y)
        self.log.insert(END,"Localization Machine Booted..."+"\n")

if __name__ == '__main__':

    # Set title, icon, dimensions
    root = Tk()
    root.title("3D Audio for Museum Exhibits")
    root.iconbitmap('images\logo.ico')
    root.geometry("700x500")

    # Create exhibit table
    exhibit_table = ExhibitTable(root)
    exhibit_table.pack(side=LEFT)

    # Create log
    log = Log(root)
    log.pack(side=LEFT)

    # Run app forever
    root.mainloop()
