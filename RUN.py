# -*- coding: UTF-8 -*-
# Python
# from tkVideoPlayer import TkinterVideo
import subprocess
from math import ceil
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
# Other
from Settings import background,foreground,salahTitles,fontStyle,JummahTimes,BMA_logoLength,BMA_logoWidth,BMA_logoPositioningRelx,BMA_logoPositioningRely,x2,x1,x,y1,y,jummahXpos,jummahYpos,jummahTitleXpos,jummahTitleYpos,salahContainerFont,isRamadan
from datetime import datetime,date
from hijri_converter import Gregorian
import json
import schedule
# from VideoPlayer import *
# from tkVideoPlayer import TkinterVideo
file_path = 'changes.json'


# Check if the file exists
if not os.path.exists(file_path):
    # Create the JSON data
    data = {"changes": False}
    
    # Write the data to the file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)



def fixHex(colour):
    while(len(colour)!=7):
        colour=colour[0]+"0"+colour[1:]
    return colour
db = open('db.json')
data = json.load(db)
db.close()
dateAndTime = data["dateAndTime"]
time = dateAndTime['time']
gDate = dateAndTime['gregorianDate']
hDate = dateAndTime['hijriDate']
announcementsData = data['announcements']
countdown = data['countdown']
salahCountdown = countdown['salah']
root = Tk()
salahInfo= SalahInfo()
tmrroData = salahInfo.checkAnnouncemennts()
changes = tmrroData[1]
announcements = tmrroData[0]
slideshow =Slideshow(root)


# Schedule the polling task

f =Footer(root,time['on'],fixHex(time['textColour']),fixHex(time['backgroundColour']),gDate['on'],fixHex(gDate['textColour']),fixHex(gDate['backgroundColour']),hDate['on'],fixHex(hDate['textColour']),fixHex(hDate['backgroundColour']))
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
baitulMamurLogo = Image.open("logo.png")
logo_pic = baitulMamurLogo.resize((BMA_logoWidth,BMA_logoLength),Image.Resampling.LANCZOS)
new_logo = ImageTk.PhotoImage(logo_pic)
Label(salahContinerframe,image=new_logo).place(relx=BMA_logoPositioningRelx,rely=BMA_logoPositioningRely,anchor='center')

s1 = Slide(root,
content="",
frame=salahContinerframe,
time=10
)


hijri = Gregorian(int(datetime.now().year), datetime.now().month, datetime.now().day).to_hijri()

if hijri.month_name() =="Dhu al-Hijjah":
    if hijri.day <10 and hijri.day>3:
        eidJamaahSlide = Slide(root,title="EID JAMA'AH",content="1st Jama'ah: 7:00 AM\n\n2nd Jama'ah: 8:30 AM\n\n3rd Jama'ah: 10:00 AM",contentFont=100,bg='black')
if hijri.month_name() =="Ramadhan":
    ramadanDay = hijri.day
    ramadanDaySlide = Slide(root,title="Ramadan Day",content=ramadanDay,contentFont=450,titleFont=100)
    if ramadanDay >25:
        eidJamaahSlide = Slide(root,title="EID JAMA'AH",content="1st Jama'ah: 7:00 AM\n\n2nd Jama'ah: 8:30 AM\n\n3rd Jama'ah: 9:30 AM",contentFont=100,bg='black')
    if ramadanDay <= 12 and hijri.year == 1444:
        gatheringSlide = Slide(root, title="Iftaar gathering this monday",titleFont=100,content="On monday 3rd of April (12th Ramadan),\nBaitul Mamur Academy would like to invite you to an iftaar gathering,\nPlease come and bring your friends & family to this barakah filled event\nWe look forward to seeing you all\nInsha'Allah",contentFont=65)


s1.packSlide()
slideshow.add(s1)
normalSlides = []
imageSlides = []
photoImageRefs = []  # List to store references to PhotoImage objects
def img():
    normalSlides.clear()
    imageSlides.clear()
    photoImageRefs.clear()
    db = open('db.json')
    data = json.load(db)
    db.close()
    try:
        slides = data['slides']
        basicSlides = slides['basic']
        nSlides = basicSlides['normalSlide']
        iSlides = basicSlides['imageSlide']
        if(not (isinstance(nSlides,str))):
            for i in range(len(nSlides)):
                normalSlides.append([Slide(root,
            title=nSlides[i]['title'],
            titleFont=45+(nSlides[i]['font']['textFactor']*5),
            content=nSlides[i]['text'],
            contentFont=35+(nSlides[i]['font']['textFactor']*5),
            bg=fixHex(nSlides[i]['colour']['slide']),
            time=nSlides[i]['displayTime'],
            fg=fixHex(nSlides[i]['colour']['text']),
            titleFg=fixHex(nSlides[i]['colour']['title']),
            ),nSlides[i]['order']])
        if(not (isinstance(iSlides,str))):
            maxImgWidth=1900
            for i in range(len(iSlides)):
                maxImgHeight = 870 if iSlides[i]['title'] == "" else 780
                try:
                    openedImage = Image.open("images/downloadedImages/" + iSlides[i]['imageName'])
                except FileNotFoundError:
                    openedImage = Image.open("images/noImgFound.png")
                
                width, height = openedImage.size
                imgWidth = min(round((width / height) * maxImgHeight), maxImgWidth)
                imgHeight = min(maxImgHeight, round((height / width) * maxImgWidth))
                
                # Create ImageTk.PhotoImage object and store a reference
                photoImage = ImageTk.PhotoImage(openedImage.resize((imgWidth, imgHeight), Image.LANCZOS))
                photoImageRefs.append(photoImage)
                
                imageSlides.append([Slide(root, None,
                                        image=photoImage,
                                        title=iSlides[i]['title'],
                                        bg=fixHex(iSlides[i]['colour']['slide']),
                                        time=iSlides[i]['displayTime'],
                                        titleFont=45 + (iSlides[i]['font']['titleFactor'] * 5),
                                        titleFg=fixHex(iSlides[i]['colour']['title'])),
                                    iSlides[i]['order']])
    except Exception as e:
        print("error",e)
        pass
    allSlides = [None for _ in range(len(normalSlides)+len(imageSlides))]
    for i in range(len(normalSlides)):
        allSlides[normalSlides[i][1]] = normalSlides[i][0]
    for i in range(len(imageSlides)):
        allSlides[imageSlides[i][1]] = imageSlides[i][0]
    slideshow.addAll(allSlides)

def poll_json():
    # Load the JSON file
    with open('changes.json') as f:
        data = json.load(f)
    
    # Check if the value of 'changes' is True
    if data['changes']:
        print("Changes detected! Setting 'changes' to False.")
        # Set 'changes' to False
        data['changes'] = False
        for i in range(len(normalSlides)+len(imageSlides)):
            slideshow.remove_tail()
        img()
        # Write the updated data back to the JSON file
        with open('changes.json', 'w') as f:
            json.dump(data, f, indent=4)

# Define the polling interval (e.g., every 5 seconds)
POLL_INTERVAL_SECONDS = 5


try:
    slideshow.add(gatheringSlide)
except:
    pass
try:
    slideshow.add(ramadanDaySlide)
except:
    pass
try:
    slideshow.add(eidJamaahSlide)
except:
    pass
try:
    slideshow.add(eidMubarakSlide)
except:
    pass

# def createVideoSlide(video_path):
#     app = VideoPlayerFrame(root,"videos/" +video_path)
#     app.toggle_pause_resume()
#     ta =app.get_video_duration()

#     vidSlide= Slide(frame=app,root=root,content="",time=ta,video=True)
#     slideshow.add(vidSlide)
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return ceil(float(result.stdout))
# def createVideoSlide(filename):
#     videoplayer = TkinterVideo(master=root, scaled=True)
#     videoplayer.load("videos/"+filename)
#     vidSlide= Slide(frame=videoplayer,root=root,content="",time=get_length("videos/"+filename),video=True)
#     slideshow.add(vidSlide)

r=Ramadan(slideshow,root)
# for video in data['slides']['basic']['videoSlide']:
#     createVideoSlide(video['videoName'])
# createVideoSlide("eid-video.mp4")
t = Timer(root,salahInfo.salahTimesObj,[f,slideshow],changes,announcements,timeChanges,salahLabels,r,announcementsData['minutes'],announcementsData['slideshow'],announcementsData['staticSlide'],salahCountdown['countBefore'],salahCountdown['displayText'],salahCountdown['keepMinutes'],salahCountdown['on'])
img()


schedule.every(POLL_INTERVAL_SECONDS).seconds.do(poll_json)



root.bind('<space>',slideshow.forceNext)
root.bind('<Right>',slideshow.forceNext)
root.bind('<Left>',slideshow.forcePrev)

root.config(bg=background)
root.attributes('-fullscreen',True)
root.mainloop()
