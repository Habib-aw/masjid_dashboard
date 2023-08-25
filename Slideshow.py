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
        # self.setZhikrSlide()
        schedule.every(1).seconds.do(self.next)
    def setTimerOn(self,bool):
        self.timerOn=bool
    # def setZhikrSlide(self):
    #     englishSlide = Slide(self.root,title="English",content="some",contentFont=55,fg="white",bg="green",paddingCtop=0)
    #     bengaliSlide = Slide(self.root,title="Bengali",content="some contet",contentFont=55,fg="white",bg="green",paddingCtop=0)
    #     self.secondHead = Node(englishSlide)
    #     self.secondHead.next = Node(bengaliSlide)
    #     self.secondHead.prev=self.secondHead.next
    #     self.secondHead.next.next = self.secondHead
    #     self.secondHead.next.prev = self.secondHead
        # english
        # bengali bengali
    def swapHeadZhikr(self,A):
        self.secondHead = self.head
        self.head = None
        self.addAll(A)
    def swapHeadNormal(self):
        self.head = self.secondHead
    def redoTimes(self):
        count = 0
        if self.size<=1:
            return
        ptr = self.head.next
        while count < self.size-1:
            ptr.val.time +=ptr.prev.val.time
            ptr = ptr.next
            count+=1
        self.max = self.tail.val.time
        self.count = self.max -1
    def add(self, val):
        self.size+=1
        if self.head == None:
            self.head = Node(val)
            self.tail = self.head
            self.tail.next = self.head
            self.head.prev = self.tail
            self.ptr=self.head
        else:
            a = Node(val)
            self.tail.next = a
            a.prev = self.tail
            a.next = self.head
            self.head.prev = a
            self.tail = self.tail.next
    def addAll(self,A):
        for x in A:
            self.add(x)
    def next(self):
        if not self.timerOn:
            if self.size > 1:
                self.count+=1
                if self.count == self.ptr.prev.val.time:
                    self.ptr.prev.val.forgetP()
                    self.ptr.val.packSlide()
                    if self.ptr.val.announce:
                        self.root.config(bg='red')
                    else:
                        self.root.config(bg=background)
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