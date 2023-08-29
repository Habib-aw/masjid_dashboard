from datetime import datetime,timedelta
from Settings import minsBeforeSalah,isRamadan
import json
def toStrpDate(st):
    return datetime.strptime(st,"%d-%b-%y")

class SalahInfo:
	def __init__(self):
		self.allTimes = json.load(open("times.json"))
		self.startI=0
		self.salahI=0
		# self.getI()
		self.salahTimes = None
		self.salahTimesObj = None
		self.startTimes = None
		# self.getSalahs()
		self.setJamaahStartTimes()
		print(self.salahTimes)
	def setJamaahStartTimes(self):
		today = datetime.today()
		if today.date() != datetime.now().date().replace(month=12, day=31):
			tommorrow = today + timedelta(days=1)
			self.tmrroTimes = self.allTimes[tommorrow.month-1][tommorrow.day-1]
		self.todayTimes = self.allTimes[today.month-1][today.day-1]
		self.getSalahs()
	# create salah times object 
	# returns salah in an array form
	# returns start in an array form
	def getSalahs(self):
		self.salahTimes = self.returnTimes(True)
		self.salahTimesObj = objTime(self.salahTimes,subtractMin=minsBeforeSalah)
		self.startTimes =self.returnTimes(False)
    #creates an array with [fajrTime,zuhrTime,..]
	def returnTimes(self,salah):
		if(salah):
			return [self.todayTimes['Fajr_jamaah'],
				self.todayTimes['Zuhr_jamaah'],
				self.todayTimes['Asr_jamaah'],
				self.todayTimes['Maghrib_jamaah'],
				self.todayTimes['Isha_jamaah']]
		return [['STRT: '+self.todayTimes['Fajr_start'],'END: '+self.todayTimes['Sunrise']],
            'STRT: '+self.todayTimes['Zuhr_start'],
            'STRT: '+self.todayTimes['Asr_start1'],
            'STRT: '+self.todayTimes['Maghrib_start'],
            'STRT: '+self.todayTimes['Isha_start']]
	# returns salah time object at index i
	def getO(self,i):
		return self.salahTimesObj[i][1].strftime("%I:%M:%S %p")
	# returns salah time at index i
	def get(self,i):
		return self.salahTimes[i]
	# 
	def checkAnnouncemennts(self):
		announcements = []
		changes = []
		if datetime.today().date() != datetime.now().date().replace(month=12, day=31):
			tmrroSalahs = self.tmrroJamaahTimes()
			for i in range(5):
				if self.salahTimes[i] !=tmrroSalahs[i]:
					changes.append([self.salahTimesObj[i][1],tmrroSalahs[i],i])
				if  i!=3:
					if self.salahTimes[i] !=tmrroSalahs[i]:
						announcements.append([i,tmrroSalahs[i]])
		return [announcements,changes]
	def tmrroJamaahTimes(self):
		return [self.tmrroTimes['Fajr_jamaah'],
				self.tmrroTimes['Zuhr_jamaah'],
				self.tmrroTimes['Asr_jamaah'],
				self.tmrroTimes['Maghrib_jamaah'],
				self.tmrroTimes['Isha_jamaah']]
	def tmrroStartTimes(self):
		return [['STRT: '+self.tmrroTimes['Fajr_start'],'END: '+self.tmrroTimes['Sunrise']],
            'STRT: '+self.tmrroTimes['Zuhr_start'],
            'STRT: '+self.tmrroTimes['Asr_start1'],
            'STRT: '+self.tmrroTimes['Maghrib_start'],
            'STRT: '+self.tmrroTimes['Isha_start']]
def objTime(arr,addMin=0,subtractMin=0):
	salahNames = ["Fajr","Zuhr","Asr","Maghrib","Isha"]
	newArr = arr.copy()
	newArr[0] += " AM"
	for i in range(1,len(arr)):
		newArr[i]+= " PM"
	for i in range(len(newArr)):
		if "-" in newArr[i]:
			continue
		newArr[i] = datetime.strptime(newArr[i],"%I:%M %p")+timedelta(minutes=addMin)-timedelta(minutes=subtractMin)
	for i in range(len(arr)):
		newArr[i] = [salahNames[i],newArr[i]]
	return newArr