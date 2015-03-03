#!/usr/bin/python
import cv2
from Tkinter import *
from ocr import *

#globals

class Webcam:
	startCrop = False		
	drawingCrop = False
	cropSelected=False
	pCrop0 = (0,0)
	pCrop1 = (0,0)

	def __init__(self):
		self.cap = cv2.VideoCapture(1)
		cv2.namedWindow("image")
		cv2.setMouseCallback("image",self.mouseCB,self)

	def mouseCB(self,event,x,y,flags,param):
		if event == cv2.EVENT_LBUTTONDOWN and self.startCrop == True:
			self.drawingCrop = True
			self.pCrop0 = (x,y)
		if  (event == cv2.EVENT_MOUSEMOVE and self.drawingCrop==True):
			self.pCrop1 = (x,y)
		if (event == cv2.EVENT_LBUTTONUP and self.drawingCrop == True):
			self.startCrop = False
			self.drawingCrop = False
			self.cropSelected=True
		
	def run(self):
		r,i = self.cap.read()

		if self.drawingCrop==True:
			cv2.rectangle(i,self.pCrop0,self.pCrop1,(0,255,0))

		if self.startCrop == False and self.cropSelected == True:
			x1 = self.pCrop0[0]
			y1 = self.pCrop0[1]
			x2 = self.pCrop1[0]
			y2 = self.pCrop1[1]
			i = i[y1:y2,x1:x2]

		cv2.imshow("image",i)
		
		key = cv2.waitKey(1)	
		#r 1048690
		#c 1048675
		if key == 1048690: #r
			self.cropSelected = False
		if key == 1048675: #c
			self.startCrop = True
		return i
		
	def crop(self):
		self.startCrop=True

		

class UI (Frame):
	def __init__(self,master=None):
		Frame.__init__(self,master)
		self.pack()
		self.createWidgets()
		self.cam = Webcam()
		self.cb = None
	def createWidgets(self):
		self.btnQuit = Button(self,{"text":"QUIT","command":self.quit})
		self.btnCrop = Button(self,{"text":"Crop","command":self.crop})
		self.btnStopCrop = Button(self,{"text":"StopCrop","command":self.resetCrop})
		self.btnQuit.pack({"side":'left'})
		self.btnCrop.pack({"side":'left'})
		self.btnStopCrop.pack({"side":'left'})


	'''
	call this to initiate cropping
	'''
	def crop(self):
		self.cam.crop()


	'''
	call this to stop the crop
	'''
	def resetCrop(self):
		self.cam.cropSelected = False

	'''
	this needs to be called at least once to start the main loop
	'''
	def loop(self):
		img = self.cam.run()
		if (self.cb is not None):
			self.cb(img)
		self.after(1,self.loop)


	'''
	cb takes one argument, which is the image it receives
	'''
	def registerImageCallback(self,cb):
		self.cb = cb
	

def checkDigit(im):
	try:
		img=cv2.cvtColor(im,cv2.cv.CV_BGR2GRAY)
		findDigits(img)
	except:
		print "couldnt find digit...."	



if __name__ == "__main__":
	cv2.namedWindow("OCR")
	root = Tk()
	app = UI(root)
	app.registerImageCallback(checkDigit)
	app.after(1,app.loop)
	app.mainloop()
	root.destroy()
