from datetime import datetime
from hijri_converter import Gregorian
from tkinter import Frame,Label
import schedule
from Settings import clockFont,dateFont, fontStyle,background,foreground
import os

class Footer:
    def __init__(self,root,timeOn,timeFg,timeBg,gDateOn,gDateFg,gDateBg,hDateOn,hDateFg,hDateBg):
        dates = getDates()
        width = root.winfo_screenwidth()
        self.frame = Frame(root,width=width)
        self.frame1 = Frame(self.frame,width=width,bg=foreground)
        gDateSide = 'left'
        hDateSide ='left'
        if not (gDateOn and hDateOn):
            gDateSide = None
            hDateSide=None
        if timeOn:
            self.createTime(width,timeBg,timeFg)
            self.repeater()
        if gDateOn:
            self.createGregorianDate(dates,gDateBg,gDateFg,gDateSide)
        if hDateOn:
            self.createHijriDate(dates,hDateBg,hDateFg,hDateSide)
        if hDateOn or gDateOn:
            self.frame1.pack(side="right",fill='x',expand=1)
        if hDateOn or gDateOn or timeOn:
            self.frame.pack(side="bottom",fill='x')
        
    def createTime(self,width,bg,fg):
        self.frame2 = Frame(self.frame,width=width,bg=bg)
        self.clock = Label(self.frame2,font=(fontStyle,clockFont,"bold"),bg=bg,fg=fg)
        self.time = datetime.now().strftime('%I:%M:%S %p')
        self.frame2.pack(side="left",fill='both',expand=1)
        self.frame2.tkraise()
        self.clock.pack(side='bottom')
    def createGregorianDate(self,dates,bg,fg,side):
        self.gDate = Label(self.frame1,text=dates[0],font=(fontStyle,dateFont,"bold"),bg=bg,fg=fg)
        self.gDate.pack(side='top',fill='both',ipadx=15,expand=1)
    def createHijriDate(self,dates,bg,fg,side):
        self.hDate = Label(self.frame1,text=dates[1],font=(fontStyle,dateFont-12,"bold"),bg=bg,fg=fg)
        self.hDate.pack(side='bottom',fill='both',ipadx=15,expand=1)
    def repeater(self):
        self.time = datetime.now().strftime('%I:%M:%S %p')
        self.clock.config(text=self.time)
        if self.time == "12:00:00 AM":
            os.system("sudo reboot")
        schedule.run_pending()
        self.clock.after(200,self.repeater)
    def packFooter(self):
        self.frame.pack(side='bottom',fill='x')
    def raiseFooter(self):
        self.frame.tkraise()
    def unpackFooter(self):
        self.frame.pack_forget()
def getDates():
    gregorianDate = datetime.now().strftime('%A, %d %B %Y')
    hijri = Gregorian(int(datetime.now().year), datetime.now().month, datetime.now().day).to_hijri()
    hijiriDate = str(hijri.day)+" "+hijri.month_name()+" "+str(hijri.year)+" "+hijri.notation()
    return (gregorianDate,hijiriDate)
