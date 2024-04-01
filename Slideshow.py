import schedule
from Settings import background
from Slide import Slide
class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

class Slideshow:
    def __init__(self,root):
        self.root = root
        self.head = None
        self.tail = None
        self.ptr = self.head
        self.count=0
        self.size=0
        self.max=0
        self.timerOn = False
        self.scheduler=schedule.every(1).seconds.do(self.next)
    def restartScheduler(self):
        schedule.cancel_job(self.scheduler)
        # schedule.clear()
        self.scheduler=schedule.every(1).seconds.do(self.next)
    def resetSlideShow(self):
        self.ptr.prev.val.forgetP()
        self.head.val.packSlide()
        self.head.next.next.next= self.head
        self.tail = self.head.next.next
        self.tail.next = self.head
        self.head.prev = self.tail
        self.ptr=self.head
        self.size = 3

        # self.head.next= self.head
        # self.tail = self.head
        # self.tail.next = self.head
        # self.head.prev = self.tail
        # self.ptr=self.head
        # self.size = 1
    def setTimerOn(self,bool):
        self.timerOn=bool

    def add(self, val):
        self.size+=1
        if self.head == None:
            self.head = Node(val)
            self.tail = self.head
            self.tail.next = self.head
            self.head.prev = self.tail
            self.ptr=self.head
        else:
            newNode = Node(val)
            self.tail.next = newNode
            newNode.prev = self.tail
            newNode.next = self.head
            self.head.prev = newNode
            self.tail = self.tail.next
            newNode.val.time += newNode.prev.val.time
            self.max = self.tail.val.time
            self.count = self.max -1
        self.restartScheduler()
    def remove_tail(self):
        if not self.head:
            return

        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.ptr.prev.val.forgetP()
            self.head.val.packSlide()
            self.ptr=self.head
            self.tail = self.tail.prev
            remTime = self.max - self.tail.val.time
            self.tail.next = self.head
            self.head.prev = self.tail
            self.max -=remTime
        self.size -= 1

    def addAll(self,A):
        for x in A:
            self.add(x)
    def printAll(self):
        test = self.head
        for i in range(self.size):
            print(test.val.time,test.val.id)
            test = test.next
    def next(self):
        if not self.timerOn:
            if self.size > 1:
                self.count+=1
                if self.count == self.ptr.prev.val.time:
                    self.ptr.prev.val.forgetP()
                    self.ptr.val.packSlide()
                    # if self.ptr.val.announce:
                    #     self.root.config(bg='red')
                    # else:
                    #     self.root.config(bg=background)
                    self.ptr= self.ptr.next
                if self.count == self.max:
                    self.count = 0
            else:
                try:
                    self.head.val.packSlide()
                except:
                    pass
        else:
            self.ptr.prev.val.forgetP()
    def forceNext(self,event=None):
        if not self.timerOn:
            if self.size > 1:
                self.count=self.ptr.prev.val.time
                self.ptr.prev.val.forgetP()
                self.ptr.val.packSlide()
                # if self.ptr.val.announce:
                #     self.root.config(bg='red')
                # else:
                #     self.root.config(bg=background)
                self.ptr= self.ptr.next
                if self.count == self.max:
                    self.count = 0
            else:
                try:
                    self.head.val.packSlide()
                except:
                    pass
        else:
            self.ptr.prev.val.forgetP()
    def forcePrev(self,event=None):
        if not self.timerOn:
            if self.size > 1:
                self.ptr.prev.val.packSlide()
                self.count=self.ptr.prev.prev.val.time
                self.ptr.val.forgetP()
                # if self.ptr.val.announce:
                #     self.root.config(bg='red')
                # else:
                #     self.root.config(bg=background)
                self.ptr= self.ptr.prev
                if self.count == self.max:
                    self.count = 0
            else:
                try:
                    self.head.val.packSlide()
                except:
                    pass
        else:
            self.ptr.prev.val.forgetP()