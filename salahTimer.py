from datetime import timedelta,datetime,date
from tkinter import Label
import schedule
from Settings import background,foreground,fontStyle,salahIn2Font,salahIn2PaddingTop,salahIn2SpaceBetween,announcementContentFont,salahIn2Bg,phonSwitchFont,isRamadan
from Slide import Slide
from audioplayer import AudioPlayer
from threading import Thread
from Slideshow import Slideshow
def toStrp(st):
    return datetime.strptime(st,"%I:%M:%S %p")
def play():
    AudioPlayer("sounds/SalahNoise.mp3").play(block=True)
def playAnnouncement(A):
    B = A[1].split(":")
    # AudioPlayer("sounds/announcements/salah/"+A[0]+".mp3").play(block=True)
    # AudioPlayer("sounds/announcements/hours/"+B[0]+".mp3").play(block=True)
    # AudioPlayer("sounds/announcements/minutes/"+B[1]+".mp3").play(block=True)


def playBeep():
    AudioPlayer("sounds/infoBeep.mp3").play(block=True)
    

announceMsg1 ="Insha'Allah\nFrom tomorrow "
announceMsg2 = " salah\nwill be at"
class Timer:
    def __init__(self,root,salahObj,Frames,changes,announcements,timesChanges,salahLabels,ramadan,keepMinutesAnnouncements,slideshowAnnouncement,staticSlide,salahCountBefore,salahDisplayText,salahKeepMinutes,salahCountdownOn) -> None:
        self.salahNames = ["Fajr","Zuhr","Asr","Maghrib","Isha"]
        self.keepMinutesAnnouncements = keepMinutesAnnouncements
        self.slideshowAnnouncement = slideshowAnnouncement
        self.staticSlide=staticSlide
        self.salahCountBefore=salahCountBefore
        self.salahDisplayText=salahDisplayText
        self.salahKeepMinutes=salahKeepMinutes
        self.salahCountdownOn=salahCountdownOn
        self.root = root
        self.salahObj= salahObj
        self.nextSalah = None
        self.timesChanges = timesChanges
        self.getNextSalah()
        self.countdown = Label(root,font=(fontStyle,salahIn2Font,"bold"),bg=salahIn2Bg,fg=foreground)
        self.counting = True
        self.phoneSwitch=Label(root,font=(fontStyle,phonSwitchFont,"bold"),text=salahIn2SpaceBetween+"Please switch off your mobile phones",bg=salahIn2Bg,fg=foreground)
        self.otherFrame = Frames
        self.changes = changes
        self.ramadan = ramadan
        self.announcements = announcements
        self.salahLabels = salahLabels
        self.timesChanged = False
        self.threadStarted = False
        self.bengaliStart = Label(root,font=(fontStyle,phonSwitchFont,"bold"),text="\n\nদয়া করে কাতার সোজা করেন",bg=salahIn2Bg,fg=foreground)
        self.announcementSet = False
        self.announcementMsg=Label(root,fg="white",bg="red",font=("Arial",100,"bold"))
        self.otherSalahs= Label(root,fg="White",bg="red",font=("Arial",60,"bold"))
        self.announcementVoiced= False
        self.zhikrSet = False
        if announcements !=[] and self.slideshowAnnouncement:
            self.sa = Slide(self.root,title="Announcements",content="",contentFont=announcementContentFont,fg="white",bg="red",paddingCtop=0,announce=True)
            self.otherFrame[1].add(self.sa)
            self.setAnnouncements()
        schedule.every(0.2).seconds.do(self.countingDown)
        self.cDownVar = ""
    def getNextSalah(self):
        arr = self.salahObj
        currentTime = toStrp(datetime.now().strftime("%I:%M:%S %p"))
        nextSalah = ""
        for j in range(len(arr)):
            if (not isinstance(arr[j][1],str)) and currentTime<arr[j][1]:
                if datetime.now().strftime("%A") == "Friday" and arr[j][0] == "Zuhr":
                    continue
                nextSalah=arr[j]
                break
        if not nextSalah:
            nextSalah=["Waiting to reboot\n\n\n\n\n\n\n\n\n",toStrp("11:59:00 PM")]
        self.nextSalah=nextSalah
    def countingDown(self):
        currentTime = datetime.now().strftime("%I:%M:%S %p")
        if self.nextSalah[1] <=toStrp(currentTime) and toStrp(currentTime)<=(self.nextSalah[1]+timedelta(minutes=self.salahCountBefore)):
            cDown = datetime.combine(date.min, (self.nextSalah[1]+timedelta(minutes=self.salahCountBefore)).time()) - datetime.combine(date.min, toStrp(currentTime).time())
            self.cDownVar = str(cDown).replace("0:0","")
            self.cDownVar = str(self.cDownVar).replace("0:","")
            if self.salahCountdownOn and not self.announcementSet and not self.zhikrSet:
                self.otherFrame[0].unpackFooter()
                self.otherFrame[1].setTimerOn(True)
                self.countdown.pack(ipady=salahIn2PaddingTop)
                self.root.config(bg=salahIn2Bg)
                self.phoneSwitch.pack()
            if self.counting:
                self.countdown.config(text=self.nextSalah[0]+" salah in\n"+self.cDownVar)
                if self.cDownVar == "2":
                    if not self.threadStarted:
                        Thread(target=play).start()
                        self.threadStarted=True
                if self.cDownVar == "0":
                    if not self.salahCountdownOn:
                        self.countdown.pack(ipady=salahIn2PaddingTop)
                        self.otherFrame[0].unpackFooter()
                        self.otherFrame[1].setTimerOn(True)
                        self.root.config(bg=salahIn2Bg)
                    self.counting =False
                    self.threadStarted = False
                    self.phoneSwitch.pack_forget()
                    self.countdown.config(text=self.salahDisplayText)
                    self.countdown.pack()
                    self.nextSalah[1] += timedelta(minutes=self.salahKeepMinutes)
            if self.cDownVar=="1" and not self.counting and not self.announcementSet:
                if self.nextSalah[0] == "Maghrib" and (datetime.now().strftime('%A')!="Sunday" and datetime.now().strftime('%A')!="Saturday" and datetime.now().strftime('%A')!="Friday"): 
                    self.nextSalah[1]+=timedelta(minutes=12)
                    self.phoneSwitch.pack_forget()
                    self.countdown.pack_forget()
                    self.otherSalahs.config(text="Assalamu alaykum\n\nPlease pray Sunnah prayer at home as Maktab is currently ongoing\n\n JazakAllah khair",font=('Arial',80),wraplength=1500,bg="green")
                    self.otherSalahs.pack(ipady=230)
                    self.root.config(bg="green")
                if self.announcements !=[] and self.staticSlide:
                    for i in range(len(self.announcements)):
                        if self.nextSalah[0] == self.salahNames[self.announcements[i][0]]:
                            self.announcementMsg.config(text=announceMsg1+self.nextSalah[0] + announceMsg2+" "+self.announcements[i][1])
                            self.nextSalah[1]+=timedelta(minutes=self.keepMinutesAnnouncements)
                            otherSalahs=""
                            for j in range(5):
                                if self.salahNames[j] == self.salahNames[self.announcements[i][0]]:
                                    continue
                                otherSalahs+=self.salahNames[j]+": "+self.salahLabels[j].label.cget("text")+"  "
                            self.phoneSwitch.pack_forget()
                            self.countdown.pack_forget()
                            self.otherSalahs.config(text=" "+otherSalahs,font=("Arial",60,"bold"),wraplength=None,bg="red")
                            self.announcementMsg.pack(ipady=200)
                            self.otherSalahs.pack(side="bottom",ipady=30)
                            self.root.config(bg="red")
                            break
                self.announcementSet=True
                # if not self.announcementSet and not self.zhikrSet:
                #     print("here234")
                #     englishSlide = Slide(self.root,title="English",content="some",contentFont=55,fg="white",bg="green",paddingCtop=0,time=5)
                #     bengaliSlide = Slide(self.root,title="Bengali",content="some contet",contentFont=55,fg="white",bg="green",paddingCtop=0,time=5)
                #     self.otherFrame[1].swapHeadZhikr([englishSlide,bengaliSlide])
                #     self.nextSalah[1]+=timedelta(minutes=1.2)
                #     self.zhikrSet = True
                #     self.otherFrame[1].redoTimes()
                #     self.otherFrame[1].setTimerOn(False)
                #     self.phoneSwitch.pack_forget()
                #     self.countdown.pack_forget()self
        elif toStrp(currentTime)>(self.nextSalah[1]+timedelta(minutes=self.salahCountBefore)):
                
            self.getNextSalah()
            self.threadStarted=False
            self.phoneSwitch.pack_forget()
            self.bengaliStart.pack_forget()
            self.countdown.pack_forget()
            self.otherFrame[0].packFooter()
            # self.otherFrame[1].swapHeadNormal()
            self.otherFrame[1].setTimerOn(False)
            self.counting=True
            self.timesChanged=False
            self.announcementMsg.pack_forget()
            self.otherSalahs.pack_forget()
            self.announcementVoiced=False
            self.announcementSet=False
            self.zhikr = False
            self.cDownVar=""
            self.root.config(bg=background)
        else:
            self.phoneSwitch.pack_forget()
            if not self.timesChanged:
                if(toStrp(currentTime) > toStrp(self.ramadan.RamadanTimes[0][1]+":00 AM")):
                    self.ramadan.setSuhoor()
                if(toStrp(currentTime) > toStrp(self.ramadan.RamadanTimes[0][2]+":00 PM")):
                    self.ramadan.setIftaar()
                for i in range(len(self.changes)):
                    if (not isinstance(self.changes[i][0],str))  and toStrp(currentTime) > self.changes[i][0]:
                        self.salahLabels[self.changes[i][2]].label.config(text=self.changes[i][1])
                        if (isRamadan and self.changes[i][2] ==0) | self.changes[i][2]==3:
                            continue
                        self.setAnnouncements(self.changes[i][2])
                self.timesChanged= True
                for i in range(5):
                        if (not isinstance(self.salahObj[i][1],str)) and toStrp(currentTime) > self.salahObj[i][1]:
                            if self.salahLabels[i].endTime != None:
                                self.salahLabels[i].startTime.config(text=self.timesChanges[i][0])
                                self.salahLabels[i].endTime.config(text=self.timesChanges[i][1])
                                continue
                            self.salahLabels[i].startTime.config(text=self.timesChanges[i])
            elif self.announcementSet and not self.announcementVoiced:
                A =  self.announcementMsg.cget("text").replace(announceMsg1,"")
                A = A.replace(announceMsg2,"").split(" ")
                cDown = datetime.combine(date.min, (self.nextSalah[1]+timedelta(minutes=self.salahCountBefore)).time()) - datetime.combine(date.min, toStrp(currentTime).time())
                self.cDownVar = str(cDown).replace("0:0","")
                self.cDownVar = str(self.cDownVar).replace("0:","")
                if (self.nextSalah[0] == "Zuhr" or self.nextSalah[0] == "Asr") and self.cDownVar == "5:00" and not self.announcementVoiced: 
                    self.announcementVoiced=True
                    Thread(target=playAnnouncement,args=(A,)).start()
                elif self.nextSalah[0] == "Isha"  and self.cDownVar == "2:00" and not self.announcementVoiced:
                    self.announcementVoiced=True
                    Thread(target=playAnnouncement,args=(A,)).start()
                elif self.nextSalah[0]=="Fajr" and self.cDownVar == "1:00" and not self.announcementVoiced:
                    self.announcementVoiced=True
                    Thread(target=playAnnouncement,args=(A,)).start()
                # elif self.nextSalah[0] == "Maghrib" and self.cDownVar == "5:00" and not self.announcementVoiced:
                #     self.announcementVoiced=True
                #     Thread(target=playAnnouncement,args=(A,)).start()
    def setAnnouncements(self,whichSalah=-1):
        
        if self.announcements != [] and self.slideshowAnnouncement:
            announcementscontent = "Insha'Allah\n"
            for i in range(len(self.announcements)):
                if self.announcements[i][0] <= whichSalah:
                    announcementscontent+=self.salahNames[self.announcements[i][0]]+" is now at "+self.announcements[i][1]+"\n"
                else:
                    announcementscontent+=self.salahNames[self.announcements[i][0]]+" salah will be changing to "+self.announcements[i][1]+" tommorow\n"
            self.sa.content.config(text=announcementscontent)
