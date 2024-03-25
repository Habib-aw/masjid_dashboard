from Slide import Slide
from datetime import datetime
from Settings import SuhoorIftaarPaddingTop,SuhoorIftaarSpaceBetween,SuhoorIftaarTimeFont,DailyMessageImgLength,DailyMessageImgWidth

def toStrpDate(st):
    return datetime.strptime(st,"%d-%b-%y")

class Ramadan:
    def __init__(self,slideshow,root) -> None:
        self.filename = "ramadan.txt"
        self.lines = open(self.filename, "r",encoding="utf-8").readlines()
        self.i=0
        self.getCorrectDate()
        self.RamadanTimes = [self.lines[i].replace("\n","").split("|") for i in range(self.i,len(self.lines))]
        self.suhoor = "\nSuhoor Ends: "+self.RamadanTimes[0][1]
        self.iftaar = "Iftaar Starts: "+self.RamadanTimes[0][2]
        self.fastTimes = self.fastTimes = self.suhoor + SuhoorIftaarSpaceBetween + self.iftaar
        self.nextDayFasts = [None for _ in range(len(self.RamadanTimes)-1)];self.setNextDayFasts()
        # Holds reference to other objects 
        self.slideshow = slideshow
        self.root = root
        self.fastTimesSlide = Slide(self.root,self.fastTimes,contentFont=SuhoorIftaarTimeFont,paddingCtop=SuhoorIftaarPaddingTop)
        self.slideshow.add(self.fastTimesSlide)
    def setFastTimes(self):
        self.fastTimes = self.suhoor + SuhoorIftaarSpaceBetween + self.iftaar
        self.fastTimesSlide.content.config(text=self.fastTimes)



    def setNextDayFasts(self):
        if len(self.RamadanTimes) > 1:
            self.nextDayFasts = self.RamadanTimes[1][1:]
    def setSuhoor(self):
        if self.nextDayFasts[0] !=None:
            self.suhoor = "\nSuhoor Ends: "+self.nextDayFasts[0] 
            self.setFastTimes()
    def setIftaar(self):
        if self.nextDayFasts[1] !=None:
            self.iftaar = "Iftaar Starts: "+self.nextDayFasts[1] 
            self.setFastTimes()
    def getCorrectDate(self):
        if len(self.lines) != 0:
            while self.lines[self.i][:9] != datetime.now().strftime("%d-%b-%y"):
                self.i+=1
    def isRamadan(self):
        if self.lines == []:
            return False
        return toStrpDate(self.RamadanTimes[0][0])  <= toStrpDate(datetime.now().strftime("%d-%b-%y"))
