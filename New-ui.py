from tkinter import *



root = Tk()

root.geometry("1000x1000")

def set_text(text1,text2):
    print(text1 + text2)







def UploadExhibit1():
    root.fileName = filedialog.askopenfilename(filetypes = (("Sound Files",".wav"),("All Files","*.*") ))
    print(root.fileName)
    namefile = root.fileName
    filepath.insert(0,namefile)
    




def create_window():
    window = Toplevel(root)
    window.geometry("300x300")
    num = Label(window,text="Audio Number")
    num.grid(row=0)
    entry1 = Entry(window)
    entry1.grid(row=0,column=1)
    name = Label(window,text="Exhibit Name")
    entry2=Entry(window)
    name.grid(row=1,column=0)
    entry2.grid(row=1,column=1)
    fileselect = Label(window,text="Select Audio File")
    fileselect.grid(row=2,column=0)
    filepath = Entry(window)
    filepath.grid(row=2,column=1)
    index = entry1.get()
    nameindex = entry2.get()
    selectB = Button(window,text="Select Audio",command= set_text(index,nameindex))
    selectB.grid(row=3,column=1)
    
     

    

section1 = Frame(root,width=600, height=1000)
section1.pack(side=LEFT)
mape= Frame(section1,bg="white",width=600, height=1000)
mape.grid(row=0,column=10)

section2 = Frame(root,width=400, height=1000)
section2.pack(side=RIGHT)

frame1 = Frame(section2)
frame1.grid(row=1)

run = Button(frame1,text="RUN",bg="green",fg="black")
run.grid(row=0,column=0)

stop = Button(frame1,text="STOP",bg="red",fg="black")
stop.grid(row=0,column=2)

clear = Button(frame1,text="CLEAR")
clear.grid(row=0,column=4)

clearall = Button(frame1,text="CLEAR ALL")
clearall.grid(row=0,column=6)


frame2 = Frame(section2)
frame2.grid(row=0)


##frame 2 UI


frame21 = Frame(frame2)
frame21.pack()

Part3 = Label(frame21,text="Exhibit Audio List")
Part3.grid(row=0,column=1)


b = Button(frame21, text="Add Audio", command=create_window)
b.grid(row=0,column=2)

index = Label(frame21,text="Number")
index.grid(row=1,column=0)
exhibit = Label(frame21,text="Exhibit Name")
exhibit.grid(row=1,column=1)
filename = Label(frame21,text="Audio File")
filename.grid(row=1,column=2)
status = Label(frame21,text="Status")
status.grid(row=1,column=3)
i1=Label(frame21,text="1")
i2=Label(frame21,text="2")
i3=Label(frame21,text="3")
i4=Label(frame21,text="4")
i5=Label(frame21,text="5")
i6=Label(frame21,text="6")
i7=Label(frame21,text="7")
i8=Label(frame21,text="8")
i9=Label(frame21,text="9")
i10=Label(frame21,text="10")
i11=Label(frame21,text="11")
i12=Label(frame21,text="12")
i13=Label(frame21,text="13")
i14=Label(frame21,text="14")
i15=Label(frame21,text="15")
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

name1 = Label(frame21,text="School Lunch")
name2 = Label(frame21,text="Holidays")
name3 = Label(frame21,text="Restaurants")
name4 = Label(frame21,text="Formals")
name5 = Label(frame21,text="Events")
name6 = Label(frame21,text="Import")
name7 = Label(frame21,text="Staples")
name8 = Label(frame21,text="Commissary")
name9 = Label(frame21,text="Commissary")
name10 = Label(frame21,text="Construction")
name11 = Label(frame21,text="Trouble")
name12 = Label(frame21,text="Meals to go")
name13 = Label(frame21,text="Cultural")
name14 = Label(frame21,text="Panama")
name15 = Label(frame21,text="Unique")


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

b1 = Button(frame21,text="Select Audio")
b2 = Button(frame21,text="Select Audio")
b3 = Button(frame21,text="Select Audio")
b4 = Button(frame21,text="Select Audio")
b5 = Button(frame21,text="Select Audio")
b6 = Button(frame21,text="Select Audio")
b7 = Button(frame21,text="Select Audio")
b8 = Button(frame21,text="Select Audio")
b9 = Button(frame21,text="Select Audio")
b10 = Button(frame21,text="Select Audio")
b11 = Button(frame21,text="Select Audio")
b12 = Button(frame21,text="Select Audio")
b13 = Button(frame21,text="Select Audio")
b14 = Button(frame21,text="Select Audio")
b15= Button(frame21,text="Select Audio")

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



 























root.mainloop()

