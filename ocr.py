#!/usr/bin/python
import cv2
import numpy as np

'''
should be an image of mostly just the digit with little margins, grayscale
'''
def interpretDigit(img):
	h,w = img.shape

	blur = cv2.GaussianBlur(img,(5,5),0)
	r,im = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	

	#get hist so we can auto-partition image
#	hist = cv2.calcHist([im],[0],None,[256],[0,256])
#	for i in xrange(256):
#		print hist[i]
	result = 0;

	'''
		1
	6		2
		7
	5		3
		4

	'''
	#partition image halfwise (horizontally) and in thirds (vertically) to detect segments
	#syntax im[y:y+h,x:x+w]
	sixTwoMask = np.zeros((h,w),np.uint8)
	sixTwoMask[int(h/4):int(h/3),0:w]=255
	sixTwo = sixTwoMask.copy()
	cv2.bitwise_and(im,sixTwoMask,sixTwo)
	

	fiveThreeMask = np.zeros((h,w),np.uint8)
	fiveThreeMask[int(2*h/3):int(3*h/4),0:w]=255
	fiveThree = fiveThreeMask.copy()
	cv2.bitwise_and(im,fiveThreeMask,fiveThree)


	oneSevenFourMask = np.zeros((h,w),np.uint8)
	oneSevenFourMask[0:h,int(w/3):int(2*w/3)]=255
	oneSevenFour = oneSevenFourMask.copy()
	cv2.bitwise_and(im,oneSevenFourMask,oneSevenFour)

	sixFiveMask = np.zeros((h,w),np.uint8)
	sixFiveMask[0:h,0:int(w/3)]=255
	sixFive = sixFiveMask.copy()
	cv2.bitwise_and(im,sixFiveMask,sixFive)

	twoThreeMask = np.zeros((h,w),np.uint8)
	twoThreeMask[0:h,int(2*w/3):w]=255
	twoThree = twoThreeMask.copy()
	cv2.bitwise_and(im,twoThreeMask,twoThree)


	#try to find 2
	two = im.copy()
	cv2.bitwise_and(twoThree,sixTwo,two)
	cv2.imshow('two',two)
	
#	cv2.imshow('sixTwo',sixTwo)
#	cv2.imshow('fiveThree',fiveThree)
#	cv2.imshow('oneSevenFour',oneSevenFour)
#	cv2.imshow('sixFive',sixFive)
#	cv2.imshow('twoThree',twoThree)
#
	#cv2.imshow('image',im)
	cv2.waitKey(0)
	
	
	

if __name__ == '__main__':
	#assume image is cropped already	
	im = cv2.imread('/home/trdenton/Pictures/0.jpg',0)
	interpretDigit(im)
#	try:
#		while True:
#			cv2.imshow('test',im)
#			cv2.waitKey(1)
#	except:
#		print "l8r"
	
