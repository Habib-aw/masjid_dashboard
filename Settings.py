from datetime import datetime,timedelta
from hijri_converter import Gregorian
import json
#-------------------------------All-------------------------------

fontStyle =  "Arial"
background = '#000037' #'#000023'
foreground = 'white' #'#e8d0bc'
isRamadan = Gregorian(int(datetime.now().year), datetime.now().month, datetime.now().day).to_hijri() == "Ramadhan"

#-------------------------------SalahContainer class-------------------------------
salahContainerFont = 93
salahTitles = 55
c= 125
salahContainerFrameW = 262+c
salahContainerFrameH =324+c
salahContainerCanvasW=262+c
salahContainerCanvasH=272+c
salahContainerCircleRadius = 175
circleXpos = 190
circleYpos = 176
salahTitlesYpos = 0.1 
salahTitlesXpos =0.5
canvasXpos=0.5
canvasYpos=0.65
salahTimeXpos=0.5
salahTimeYpos =0.45

#-------------------------------Footer class-------------------------------
clockFont = 70
dateFont =55
#-------------------------------SalahTimer class-------------------------------
salahIn2Font = 65
announcementContentFont = 64
salahIn2PaddingTop=300
salahIn2SpaceBetween=""
salahIn2Bg= 'black'
salahIn2Font = 100
salahIn2SwitchFont = 60
salahIn2Bg= 'black'
phonSwitchFont = 75
minsBeforeSalah=1
# -------------------------------Run class-------------------------------
l = -0.028
jTimes = json.load(open("times.json"))['jummahTimes']
def last_day(d, day_name):
    days = ['sunday','monday','tuesday','wednesday',
                        'thursday','friday','saturday']
    target_day = days.index(day_name.lower())
    delta_day = target_day - d.isoweekday()
    if delta_day >= 0: delta_day -= 7 # go back 7 days
    return d + timedelta(days=delta_day)
marchLastSunday = last_day(datetime(datetime.now().year,4,1),'sunday')
octoberLastSunday = last_day(datetime(datetime.now().year,11,1),'sunday')
JummahTimes = jTimes['winter'][0]+" | "+jTimes['winter'][1]

if datetime.now() >= marchLastSunday and datetime.now()<octoberLastSunday: # summer time jummah times go here
    JummahTimes = jTimes['summer'][0]+" | "+jTimes['summer'][1]

jummahXpos=0.5
jummahYpos=0.9+l

jummahTitleXpos=0.5
jummahTitleYpos=0.77+l
x= -0.1
y=-0.24
x1=0
y1=-0.07
x1=0.052
x2=0.004

BMA_logoWidth = 400
BMA_logoLength = 140
BMA_logoPositioningRelx = 0.5
BMA_logoPositioningRely = 0.64+l

# -------------------------------Ramadan class-------------------------------
DailyMessageImgWidth = 1700
DailyMessageImgLength = 770
SuhoorIftaarTimeFont = 120
SuhoorIftaarPaddingTop =25
SuhoorIftaarSpaceBetween="\n\n"