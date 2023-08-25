from datetime import datetime
from hijri_converter import Gregorian
from tkinter import Frame,Label
import schedule
from Settings import clockFont,dateFont, fontStyle,background,foreground
import os
import subprocess

def connectedToInternet():
    import requests
    url = "https://www.google.com/"
    try:
        requests.get(url, timeout=10)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


def gitPull():
    if connectedToInternet():
        cmd = [ 'git', 'pull']
        output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
        if "Already up-to-date." in str(output):
            pass
        elif "Error" in str(output):
            pass
        elif "Updating" in str(output):
            os.system("sudo reboot")
class Footer:
    def __init__(self,root):
        dates = getDates()
        self.frame = Frame(root,width=root.winfo_screenwidth(),bg=foreground)
        self.frame1 = Frame(self.frame,width=root.winfo_screenwidth(),bg=foreground)
        self.frame2 = Frame(self.frame,width=root.winfo_screenwidth(),bg=background)
        self.clock = Label(self.frame2,font=(fontStyle,clockFont,"bold"),bg=background,fg=foreground)
        self.time = datetime.now().strftime('%I:%M:%S %p')
        self.gDate = Label(self.frame1,text=dates[0],font=(fontStyle,dateFont,"bold"),bg=foreground,fg=background)
        self.hDate = Label(self.frame1,text=dates[1],font=(fontStyle,dateFont-12,"bold"),bg=foreground,fg=background)
        self.split = Label(self.frame1,text=" | ",font=(fontStyle,dateFont,"bold"),bg=foreground,fg=background)
        self.packFooter()
        # schedule.every(30).seconds.do(gitPull)
        self.repeater()
        self.check = True
    def repeater(self):
        self.time = datetime.now().strftime('%I:%M:%S %p')
        self.clock.config(text=self.time)
        if self.time == "12:00:00 AM":
            os.system("sudo reboot")
        schedule.run_pending()
        self.clock.after(200,self.repeater)
    def updateDate(self):
        dates = getDates()
        self.gDate.config(text=dates[0])
        self.hDate.config(text=dates[1])
    def packFooter(self):
        self.frame.pack(side="bottom")
        self.frame1.pack(side="bottom")
        self.frame2.pack(side="top")
        self.frame2.tkraise()
        self.gDate.pack(side="left")
        self.split.pack(side="left")
        self.clock.pack(ipadx=1000)
        self.hDate.pack(side="left")
    def raiseFooter(self):
        self.frame.tkraise()
    def unpackFooter(self):
        self.frame.pack_forget()
def getDates():
    gregorianDate = datetime.now().strftime('%A, %d %B %Y')
    hijri = Gregorian(int(datetime.now().year), datetime.now().month, datetime.now().day).to_hijri()
    hijiriDate = str(hijri.day)+" "+hijri.month_name()+" "+str(hijri.year)+" "+hijri.notation()
    return (gregorianDate,hijiriDate)
