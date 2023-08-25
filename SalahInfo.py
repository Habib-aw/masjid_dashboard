from datetime import datetime,timedelta
import re
from Settings import minsBeforeSalah,isRamadan
def toStrpDate(st):
    return datetime.strptime(st,"%d-%b-%y")
class SalahInfo:
	def __init__(self):
		self.lines = open("times.txt", "r").readlines()
		self.startTimesLines = open("start-times.txt","r").readlines()
		self.startI=0
		self.salahI=0
		self.getI()
		self.salahTimes = None
		self.salahTimesObj = None
		self.startTimes = None
		self.getSalahs()
	def getI(self):
		if len(self.lines) != 0:
			while self.lines[self.salahI][:9] != datetime.now().strftime("%d-%b-%y"):
				self.salahI+=1
		if len(self.startTimesLines)!=0:
			while self.startTimesLines[self.startI][:9] != datetime.now().strftime("%d-%b-%y"):
				self.startI+=1
	def getSalahs(self):
		salahNames = ["Fajr","Zuhr","Asr","Maghrib","Isha"]
		if len(self.lines) != 0:
			self.salahTimes = self.returnSalahTimes()
#    re.findall("\d+:[0-9][0-9]", self.lines[self.salahI])
			self.salahTimesObj = objTime(self.salahTimes,subtractMin=minsBeforeSalah)
			for i in range(len(self.salahTimes)):
				self.salahTimes[i] = [salahNames[i],self.salahTimes[i]]
				self.salahTimesObj[i] = [salahNames[i],self.salahTimesObj[i]]
		if len(self.lines) != 0:
			self.startTimes = self.startTimesLines[self.startI].split(",")
			self.startTimes = self.startTimes[1:]
			for i in range(len(self.startTimes)):
				if "|" in self.startTimes[i]:
					self.startTimes[i]=self.startTimes[i].split("|")
	def returnSalahTimes(self,index=0):
		x = self.lines[self.salahI+index].split(",")
		x = x[1:]
		for i in range(len(x)):
			x[i]=x[i].split(" ")[1]
		x[len(x)-1]=x[len(x)-1].replace("\n","")
		return x
	def getO(self,i):
		return self.salahTimesObj[i][1].strftime("%I:%M:%S %p")
	def get(self,i):
		return self.salahTimes[i][1]
	def checkAnnouncemennts(self):
		announcements = []
		changes = []
		if (len(self.lines)-1-self.salahI)>=2:
			tmrroSalahs = self.returnSalahTimes(1)
   #re.findall("\d+:[0-9][0-9]", self.lines[self.salahI+1])
			for i in range(5):
				if self.salahTimes[i][1] !=tmrroSalahs[i]:
					changes.append([self.salahTimesObj[i][1],tmrroSalahs[i],i])
				if i == 0 and isRamadan:
					continue
				if  i!=3:
					if self.salahTimes[i][1] !=tmrroSalahs[i]:
						announcements.append([i,tmrroSalahs[i]])
		return [announcements,changes]
	def tmrroStartTimes(self):
		changes= []
		if (len(self.lines)-1-self.salahI)>=2:
			changes = self.startTimesLines[self.startI+1].split(",")
			changes = changes[1:]
			for i in range(len(changes)):
				if "|" in changes[i]:
					changes[i]=changes[i].split("|")
		return changes
def checkRamadan():
	rmd = open("ramadan.txt", "r").readlines()
	if rmd !=[]:
		RamadanTimes = [rmd[0].replace("\n","").split("|")]
		if toStrpDate(RamadanTimes[0][0])  <= toStrpDate(datetime.now().strftime("%d-%b-%y")) and toStrpDate(RamadanTimes[len(RamadanTimes)-1][0])>=toStrpDate(datetime.now().strftime("%d-%b-%y")):
			return True
	return False
def objTime(arr,addMin=0,subtractMin=0):
	newArr = arr.copy()
	newArr[0] += " AM"
	for i in range(1,len(arr)):
		newArr[i]+= " PM"
	for i in range(len(newArr)):
		if "-" in newArr[i]:
			continue
		newArr[i] = datetime.strptime(newArr[i],"%I:%M %p")+timedelta(minutes=addMin)-timedelta(minutes=subtractMin)
	return newArr
