from tkinter import *
root = Tk()

def UploadExhibit1():
    root.fileName = filedialog.askopenfilename(filetypes = (("Sound Files",".wav"),("All Files","*.*") ))
    print(root.fileName)




def UploadExhibit2():
    root.fileName = filedialog.askopenfilename(filetypes = (("Sound Files",".wav"),("All Files","*.*") ))
    print(root.fileName)




def UploadExhibit3():
    root.fileName = filedialog.askopenfilename(filetypes = (("Sound Files",".wav"),("All Files","*.*") ))
    print(root.fileName)



def UploadExhibit4():
    root.fileName = filedialog.askopenfilename(filetypes = (("Sound Files",".wav"),("All Files","*.*") ))
    print(root.fileName)







root.geometry("1000x1000")

icon = PhotoImage(file="C:\\Users\\Vasu Jain\\AppData\\Local\\Programs\\Python\\Python35-32\\icon1.png")
icon1 = PhotoImage(file="C:\\Users\\Vasu Jain\\AppData\\Local\\Programs\\Python\\Python35-32\\foodboc.png")

root1 = Frame(root)
root1.pack()
frame1 = Frame(root1)
frame1.grid(row=0)
button1 = Button(frame1,text="Exhibit 1",image=icon1,command=UploadExhibit1)
button1.pack()
name1 = Label(frame1,text="Exhibit 1")
name1.pack()

frame2 = Frame(root1)
frame2.grid(row=1,column=0)
button2 = Button(frame2,text="Exhibit 2",image=icon,command=UploadExhibit2)
button2.pack()
name2 = Label(frame2,text="Exhibit 2")
name2.pack()



frame3 = Frame(root1)
frame3.grid(row=1,column=20)
button3 = Button(frame3,text="Exhibit 3",image=icon,command=UploadExhibit3)
button3.pack()
name3 = Label(frame3,text="Exhibit 3")
name3.pack()

frame4 = Frame(root1)
frame4.grid(row=2,column=10)
button4 = Button(frame4,text="Exhibit 4",image=icon,command=UploadExhibit4)
button4.pack()
name4 = Label(frame4,text="Exhibit 4")
name4.pack()

root.mainloop()
