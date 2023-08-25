# -*- coding: UTF-8 -*-
# Python
from tkinter import Tk,Label
from ramadan import Ramadan
from PIL import ImageTk,Image
# Classes
from SalahContainer import *
from Slide import *
from SalahInfo import *
# from Bot import *
from Footer import *
from Slideshow import *
from salahTimer import Timer
from hijri_converter import Gregorian
# Other
from Settings import background,foreground,salahTitles,fontStyle,JummahTimes,logoPositioningRelx,logoPositioningRely,x2,x1,x,y1,y,jummahXpos,jummahYpos,jummahTitleXpos,jummahTitleYpos,salahContainerFont,isRamadan


root = Tk()
salahInfo= SalahInfo() ### updates times and receives time from file ###
tmrroData = salahInfo.checkAnnouncemennts()
changes = tmrroData[1]
announcements = tmrroData[0]
slideshow =Slideshow(root)
f =Footer(root)
sTimes = salahInfo.startTimes
timeChanges = salahInfo.tmrroStartTimes()
salahContinerframe =Frame(root,bg=background,height=root.winfo_screenheight()-150,width=root.winfo_screenwidth())
fajr = SalahContainer(salahContinerframe,"Fajr",salahInfo.get(0),sTimes[0],xpos=(x+0.1)-x2,ypos=y+0.70)
zuhr = SalahContainer(salahContinerframe,"Zuhr",salahInfo.get(1),sTimes[1],xpos=x+0.35-x1,ypos=y+0.5+y1)
asr = SalahContainer(salahContinerframe,"Asr",salahInfo.get(2),sTimes[2],xpos=x+0.5,ypos=y+0.25)
maghrib = SalahContainer(salahContinerframe,"Maghrib",salahInfo.get(3),sTimes[3],xpos=x+0.65+x1,ypos=y+0.5+y1)
isha = SalahContainer(salahContinerframe,"Isha",salahInfo.get(4),sTimes[4],xpos=(x+0.9)+x2,ypos=y+0.70)
salahLabels = [fajr,zuhr,asr,maghrib,isha]
Label(salahContinerframe,text="Jummah",font=(fontStyle,salahTitles),bg=background,fg=foreground).place(relx=jummahTitleXpos,rely=jummahTitleYpos,anchor='center')
Label(salahContinerframe,text=JummahTimes,font=(fontStyle,salahContainerFont),bg=background,fg=foreground).place(relx=jummahXpos,rely=jummahYpos,anchor='center')

s1 = Slide(root,
content="",
frame=salahContinerframe,
time=10
)

hijri = Gregorian(int(datetime.now().year), datetime.now().month, datetime.now().day).to_hijri()

if hijri.month_name() =="Ramadhan":
    ramadanDay = hijri.day
    if ramadanDay >25:
        eidJamaahSlide = Slide(root,title="EID JAMA'AH",content="1st Jama'ah: 8:30 AM\n\n2nd Jama'ah: 9:30 AM\n\n3rd Jama'ah: 10:30 AM",contentFont=100,bg='black')

if isRamadan:
    r = Ramadan(slideshow,root)

s1.packSlide()
slideshow.addAll([s1])
try:
    slideshow.add(eidJamaahSlide)
except:
    pass
try:
    t = Timer(root,salahInfo.salahTimesObj,[f,slideshow],changes,announcements,timeChanges,salahLabels,r)
except:
    t = Timer(root,salahInfo.salahTimesObj,[f,slideshow],changes,announcements,timeChanges,salahLabels,None)
slideshow.redoTimes()
root.config(bg=background)
root.attributes('-fullscreen',True)
root.mainloop()
