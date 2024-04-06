from datetime import datetime,timedelta
from tkinter import Frame,Label
from Settings import background, foreground
class Slide:
	def __init__(self,root, content,contentFont=35,title=None,titleFont=55,whatTime=None,time=7,howLong=5,frame=None,paddingCtop=10,fg=foreground,titleFg=foreground,bg=background,image=None,announce=False,wraplength=None,smallContent=None,smallContentFont=None,video=False):
		self.video = video
		if frame !=None:
			self.frame = frame
		else:
			self.createFrame(root,content,contentFont,title,titleFont,paddingCtop,fg,bg,image,wraplength,smallContent,smallContentFont,titleFg)
		if whatTime == None:
			self.time = time
		else:
			self.time = datetime.strptime(whatTime,"%I:%M %p")
			self.howLong = timedelta(minutes=howLong)
		self.announce = announce
		self.id = "Title: "+ str(title) +", Content: " +str(content)
		if video:
			self.id = "Video"
	def packSlide(self):
		if self.video:
			self.frame.play()
			# self.frame.toggle_pause_resume()
		self.frame.pack(side='top',fill="both",expand=1)
	def forgetP(self):
		if self.video:
			# self.frame.reset_video()
			self.frame.seek(sec=0)
			self.frame.pause()
		self.frame.pack_forget()
	def createFrame(self,root,content,contentFont,title,titleFont,paddingCtop,fg,bg,image,wraplength,smallContent,smallContentFont,titleFg):
		self.frame =Frame(root,bg=bg,width=root.winfo_screenwidth())
		self.inFrame = Frame(self.frame,bg=background)
		if image ==None:
			if wraplength == None:
				wraplength=root.winfo_screenwidth()-200
			self.content = Label(self.inFrame,text=content,font=('Arial',contentFont),fg=fg,bg=bg,wraplength=wraplength)
			self.content.pack(ipadx=1000,ipady=paddingCtop)
			if smallContent != None:
				self.smallContent = Label(self.inFrame,text=smallContent,font=('Arial',smallContentFont),fg=fg,bg=bg,wraplength=wraplength)
				self.smallContent.pack()
		elif content == None:
			self.imageLabel = Label(self.inFrame,image=image)
			self.imageLabel.pack()
		else:
			if wraplength == None:
				wraplength=root.winfo_screenwidth()-700
			self.content = Label(self.inFrame,text=content,font=('Arial',contentFont),fg=fg,bg=bg,wraplength=wraplength)
			self.imageLabel = Label(self.inFrame,image=image)
			self.imageLabel.pack(side='left')
			self.content.pack(side='right')
		if title != None and title != "":
			self.title = Label(self.frame,text=title,font=('Arial',titleFont,'underline','bold'),bg=bg,fg=titleFg)
			self.title.pack(side="top")
		self.inFrame.pack(side='top')
