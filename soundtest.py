#!/usr/bin/python
import cv2

#globals
startCrop = False		
drawingCrop = False
cropSelected=False
pCrop0 = (0,0)
pCrop1 = (0,0)

def mouseFunc(event,x,y,flags,param):
	global startCrop,pCrop0,pCrop1,cropSelected,drawingCrop
	if event == cv2.EVENT_LBUTTONDOWN and startCrop == True:
		drawingCrop = True
		pCrop0 = (x,y)
	if  (event == cv2.EVENT_MOUSEMOVE and drawingCrop==True):
		pCrop1 = (x,y)
	if (event == cv2.EVENT_LBUTTONUP and drawingCrop == True):
		startCrop = False
		drawingCrop = False
		cropSelected=True
		
		


	

cap = cv2.VideoCapture(0)

cv2.namedWindow("test")
v = cv2.setMouseCallback("test",mouseFunc)

try:
	while True:
		r,i = cap.read()

		#if we are drawing the crop box add that here
		if drawingCrop==True:
			cv2.rectangle(i,pCrop0,pCrop1,(0,255,0))

		if startCrop == False and cropSelected == True:
			x1 = pCrop0[0]
			y1 = pCrop0[1]
			x2 = pCrop1[0]
			y2 = pCrop1[1]
			i = i[y1:y2,x1:x2]

		cv2.imshow("test",i)
		
		key = cv2.waitKey(1)	
#q 1048689
#r 1048690
#c 1048675

		if key == 1048689: #q
			break
		if key == 1048690: #r
			cropSelected = False
		if key == 1048675: #c
			startCrop = True
		
except:
	print "exiting!"
