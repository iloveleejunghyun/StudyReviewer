
import tkinter as tk  # python 3
# import Tkinter as tk  # python 2

# qPic = None
class QAFrame(tk.Frame):
    def __init__(self, root, onQButton, onAButton):

        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0, background="#DCDCDC")
        self.frame = tk.Frame(self.canvas, background="#DCDCDC")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.qButton = tk.Button(self.frame, text="Paste Question(F2)", command=onQButton)
        self.qLabel = tk.Label(self.frame)
        self.aButton = tk.Button(self.frame, text="Paste Answer(F3)", command=onAButton)
        self.aLabel = tk.Label(self.frame)

        self.qPic = tk.PhotoImage(file="1.png")
        self.aPic = tk.PhotoImage(file="1.png")
        
        self.populate()


    def updateQLabel(self, pic):
        self.qPic = pic
        self.qLabel.config(image=self.qPic)

        width = max(self.qPic.width(), self.aPic.width())
        height = self.qPic.height() + self.aPic.height() + 60
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
        height = self.qPic.height() + self.aPic.height() + 70
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
        # self.qEntry.pack(expand=True, fill='x')
        self.qButton.pack(expand=True, fill='x')
        self.qLabel.pack()
        # self.aEntry.pack(expand=True, fill='x')
        self.aButton.pack(expand=True, fill='x')
        self.aLabel.pack()
        tk.Frame.pack(self, side='top',fill="both", expand=True)
        self.canvas.config(height =130) # minimum height
        
if __name__ == "__main__":
    root=tk.Tk()
    entry = tk.Entry(root, text="terwrwe")
    global qPic
    qPic = tk.PhotoImage(file="qPic.png")
    frame = QAFrame(root, None, None)
    entry.pack()
    frame.pack()
    frame.updateQLabel(pic=qPic)
    frame.updateALabel(pic=qPic)
    root.mainloop()