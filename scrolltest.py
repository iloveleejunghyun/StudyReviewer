# from tkinter import *
# root=Tk()
# frame=Frame(root,width=300,height=300)
# frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)
# canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
# # canvas=Canvas(frame)
# vbar=Scrollbar(frame,orient=VERTICAL)
# vbar.pack(side=RIGHT,fill=Y)
# vbar.config(command=canvas.yview)
# canvas.config(width=300,height=300)
# canvas.config(yscrollcommand=vbar.set)

# qPic = PhotoImage(file="1.png")

# label1 = Label(canvas)
# label1.config(image=qPic)
# label1.pack()
# # label2 = Label(canvas)
# # label2.config(image=qPic)
# # label2.pack()
# # label3 = Label(canvas)
# # label3.config(image=qPic)
# # label3.pack()
# # canvas.config(image=qPic)

# #canvas.create_image(0, 0, image=qPic, anchor=NW)
# canvas.pack(side=LEFT,expand=True,fill=BOTH)
# canvas.config(scrollregion=(0,0,qPic.width(),1500))
# root.mainloop()


import tkinter as tk  # python 3
# import Tkinter as tk  # python 2

# qPic = None
class QAFrame(tk.Frame):
    def __init__(self, root, focusOnQEntry, focusOnAEntry):

        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0, background="#DCDCDC")
        self.frame = tk.Frame(self.canvas, background="#DCDCDC")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        # self.vsb.pack(side="right", fill="y")
        # self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)



        self.qEntry = tk.Entry(self.frame)
        self.qEntry.bind("<FocusIn>", focusOnQEntry)
        # self.qEntry.pack()

        # self.qPic = tk.PhotoImage(file="1.png")
        self.qLabel = tk.Label(self.frame)
        # self.qLabel.config(image=self.qPic)
        # self.qLabel.pack()


        self.aEntry = tk.Entry(self.frame)
        self.aEntry.bind("<FocusIn>", focusOnAEntry)
        # self.aEntry.pack()

        self.aLabel = tk.Label(self.frame)
        # self.aLabel.config(image=self.qPic)
        # self.aLabel.pack()
        
        self.qPic = tk.PhotoImage(file="1.png")
        self.aPic = tk.PhotoImage(file="1.png")
        
        self.populate()


    def updateQLabel(self, pic):
        self.qPic = pic
        self.qLabel.config(image=self.qPic)

        width = max(self.qPic.width(), self.aPic.width())
        height = self.qPic.height() + self.aPic.height() + 70
        print(self.qPic.width(), self.aPic.width(),self.qPic.height(), self.aPic.height())
        print(width, " ", height)
        print(self.winfo_screenheight())
        self.canvas.config(width = width)
        self.canvas.config(height = min(height, self.winfo_screenheight()-200))
        self.canvas.config(scrollregion=(0,0, width, height))

    def updateALabel(self, pic):
        # self.aLabel.config(image=pic)
        self.aPic = pic
        self.aLabel.config(image=self.aPic)

        width = max(self.qPic.width(), self.aPic.width())
        height = self.qPic.height() + self.aPic.height() + 50
        print(self.qPic.width(), self.aPic.width(),self.qPic.height(), self.aPic.height())
        print(width, " ", height)
        self.canvas.config(width = width)
        self.canvas.config(height = min(height, self.winfo_screenheight()-150))

        self.canvas.config(scrollregion=(0,0, width, height))

    def hideALabel(self):
        self.aLabel.pack_forget()

    def showALabel(self):
        self.aLabel.pack()


    def populate(self):
        '''Put in some fake data'''
        # for row in range(100):
        #     tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1", 
        #              relief="solid").grid(row=row, column=0)
        #     t="this is the second column for row %s" %row
        #     tk.Label(self.frame, text=t).grid(row=row, column=1)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def pack(self):
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.qEntry.pack(expand=True, fill='x')
        self.qLabel.pack()
        self.aEntry.pack(expand=True, fill='x')
        self.aLabel.pack()
        tk.Frame.pack(self, side='top',fill="both", expand=True)
        self.canvas.config(height =70) # minimum height
        
if __name__ == "__main__":
    root=tk.Tk()
    entry = tk.Entry(root, text="terwrwe")
    global qPic
    qPic = tk.PhotoImage(file="2.png")
    frame = QAFrame(root, None, None)
    entry.pack()
    frame.pack()
    frame.updateQLabel(pic=qPic)
    frame.updateALabel(pic=qPic)
    root.mainloop()