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

	cv2.imshow("OCR",im)
	cv2.waitKey(1)	

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

	resultMap = { 	63:'0',
			6: '1',
			91: '2',
			79: '3',
			102: '4',
			109: '5',
			125: '6',
			7: '7',
			39: '7',
			127: '8',
			103: '9',
			111: '9',
			}

	#partition image halfwise (horizontally) and in thirds (vertically) to detect segments
	#syntax im[y:y+h,x:x+w]
	sixTwoMask = np.zeros((h,w),np.uint8)
	sixTwoMask[int(h/4):int(h/3),0:w]=255
	sixTwo = cv2.bitwise_and(im,sixTwoMask)
	

	fiveThreeMask = np.zeros((h,w),np.uint8)
	fiveThreeMask[int(2*h/3):int(3*h/4),0:w]=255
	fiveThree = cv2.bitwise_and(im,fiveThreeMask)


	oneSevenFourMask = np.zeros((h,w),np.uint8)
	oneSevenFourMask[0:h,int(2*w/5):int(3*w/5)]=255
	oneSevenFour = cv2.bitwise_and(im,oneSevenFourMask)

	sixFiveMask = np.zeros((h,w),np.uint8)
	sixFiveMask[0:h,0:int(w/3)]=255
	sixFive = cv2.bitwise_and(im,sixFiveMask)

	twoThreeMask = np.zeros((h,w),np.uint8)
	twoThreeMask[0:h,int(2*w/3):w]=255
	twoThree = cv2.bitwise_and(im,twoThreeMask)

	#need horizontal slices for one, seven, for
	topMask = np.zeros((h,w),np.uint8)
	topMask[0:int(h/5),0:w]=255
	top = cv2.bitwise_and(im,topMask)

	
	midMask = np.zeros((h,w),np.uint8)
	midMask[int(2*h/5):int(3*h/5),0:w]=255
	mid = cv2.bitwise_and(im,midMask)

	
	bottomMask = np.zeros((h,w),np.uint8)
	bottomMask[int(4*h/5):h,0:w]=255
	bottom = cv2.bitwise_and(im,bottomMask)

	one = cv2.bitwise_and(oneSevenFour,topMask)
	if (one.any()):
		result |= 1<<0
		#print "found one"

	four = cv2.bitwise_and(oneSevenFour,bottomMask)
	if (four.any()):
		result |= 1<<3
		#print "found four"
	
	seven = cv2.bitwise_and(oneSevenFour,midMask)
	if (seven.any()):
		result |= 1<<6
		#print "found seven"

	two = cv2.bitwise_and(twoThree,sixTwo)
	if (two.any()):
		result |= 1<<1
		#print "found two"

	six = cv2.bitwise_and(sixTwo,sixFive)
	if (six.any()):
		result |= 1<<5
		#print "found six"

	five = cv2.bitwise_and(fiveThree,sixFive)
	if (five.any()):
		result |= 1<<4
		#print "found five"

	three = cv2.bitwise_and(fiveThree,twoThree)
	if (three.any()):
		result |= 1<<2
		#print "found three"

	return resultMap[result]
	
	
	

if __name__ == '__main__':
	#assume image is cropped already	
	test()


def test():
	for i in xrange(10):
		try: 
			im = cv2.imread("/home/trdenton/Pictures/%d.jpg"%i,0)
			print interpretDigit(im)
		except:
			print "%d sucks!" % i
#	try:
#		while True:
#			cv2.imshow('test',im)
#			cv2.waitKey(1)
#	except:
#		print "l8r"
	
