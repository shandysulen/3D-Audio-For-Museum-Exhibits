import tkinter as tk
root = tk.Tk()

def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))


button = tk.Button(root,
                   text="PLAY",
                   )
button.pack(side=tk.RIGHT)

tfield = tk.Entry(root)
tfield.pack(side=tk.RIGHT)
label = tk.Label(root,text="Enter Location to play Sound")
label.pack(side=tk.LEFT)

#root.bind('<Motion>', motion)
root.mainloop()
