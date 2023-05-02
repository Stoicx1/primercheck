import cv2
import numpy as np
import os
import time
import keyboard
import aspose.words as aw
import svgmodule

###########################################################
###	VARIABLES                                           ###
###########################################################
windowName = 'app'

pathCam1 = 'C:/Users/Pavol Hvolka/Documents/WEB/primercheck/camTest/cam1'
pathCam2 = 'C:/Users/Pavol Hvolka/Documents/WEB/primercheck/camTest/cam2'
pathCam3 = 'C:/Users/Pavol Hvolka/Documents/WEB/primercheck/camTest/cam3'

imgListCam1 = []
imgListCam2 = []
imgListCam3 = []

SNToFindCam1 = '13000027023041200001-W214-RR'
SNToFindCam2 = '13000027023042400139-A214780'
SNToFindCam3_1 = '1773245A;276010000884;030123'
SNToFindCam3_2 = '130000270230425000314;030123'
SNToFindCam3_3 = '130000270230425000254;030123'
SNToFindCam3_4 = '130000270230425000274;030123'

###########################################################
### FUNCTIONS                                           ###
###########################################################

def GetListOfImages(dirListCam, serialNubmer, numCam, pathCam):
	# prints all files
		dataDict = []
		imgList = []
		newestID = 0
		newestSN = ''

		for img in dirListCam:
			name = img
			if serialNubmer in name:
				tmpList = name.replace(".", "_").split("_")
				tmpList.append(name)
				dataDict.append({'CAM':numCam,'CYCLE':tmpList[2],'SN':tmpList[3],'RESULT':tmpList[4], 'ID':int(tmpList[5]), 'FORMAT':tmpList[6], 'PATH':tmpList[7]})
				temp = {'CAM':numCam,'CYCLE':tmpList[2],'SN':tmpList[3],'RESULT':tmpList[4], 'ID':int(tmpList[5]), 'FORMAT':tmpList[6], 'PATH':tmpList[7]}
				if temp['RESULT']=='NOK' and temp['FORMAT']=='svg':
					pathsvg = ('{0}/{1}'.format(pathCam, temp['PATH']))
					pathsvglength = len(pathsvg)-4
					pathpng = ('{0}/{1}'.format(pathCam, temp['PATH']))[:pathsvglength]+'.png'
					print(pathsvg)
					print(pathpng)
					if (os.path.exists(pathpng) == False):
						svgmodule.RemoveImage(pathsvg)
						# create a document
						doc = aw.Document()
						# create a document builder and initialize it with document object
						builder = aw.DocumentBuilder(doc)
						# insert SVG image to document
						shape = builder.insert_image(pathsvg)
						# OPTIONAL
						# Calculate the maximum width and height and update page settings 
						# to crop the document to fit the size of the pictures.
						pageSetup = builder.page_setup
						pageSetup.page_width = shape.width
						pageSetup.page_height = shape.height
						pageSetup.top_margin = 0
						pageSetup.left_margin = 0
						pageSetup.bottom_margin = 0
						pageSetup.right_margin = 0
						# save as PNG
						doc.save(pathpng)
						print(">>> Modified SVG succesfully saved as PNG")
					else:
						print(">>> PNG Exists")

				if len(dataDict)>0:
					old_array = dataDict
				else:
					pass

		if len(dataDict)>0:
			unique_cycles = {}
			for item in old_array:
				cycle = item['CYCLE']
				id = item['ID']
				format = item['FORMAT']
				if cycle not in unique_cycles:
					if item['FORMAT']=='bmp':
						unique_cycles[cycle] = id
				else:
					if id > unique_cycles[cycle]:
						unique_cycles[cycle] = id
			# Create a new array with the unique cycles and their maximum IDs
			new_array = []
			for cycle, id in unique_cycles.items():
				for item in old_array:
					if item['CYCLE'] == cycle and item['ID'] == id:
						new_array.append(item)
						break
		else:
			new_array = dataDict

		if len(new_array)>0:
			return new_array
		else:
			new_array = [{'CAM':numCam,'CYCLE':'X','SN':'N/A'}]
			return new_array

def printImgListCam(imgListCam, numCam):
	for row in imgListCam:
		print(row)

def SetImgText(img, imgData):

	colorText = (0, 255, 0) if imgData['RESULT']=='OK' else (0, 0, 255)
	font                   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (40,300)
	fontScale              = 5
	fontColor              = colorText
	thickness              = 15
	lineType               = 3

	cv2.putText(img, 
		imgData['RESULT'], 
	    bottomLeftCornerOfText, 
	    font, 
	    fontScale,
	    fontColor,
	    thickness,
	    lineType)

	colorText = (0, 255, 0) if imgData['RESULT']=='OK' else (0, 0, 255)
	font                   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (55,120)
	fontScale              = 2.2
	fontColor              = (255,255,255)
	thickness              = 5
	lineType               = 4

	cv2.putText(img, 
		imgData['PATH'], 
	    bottomLeftCornerOfText, 
	    font, 
	    fontScale,
	    fontColor,
	    thickness,
	    lineType)

	colorFrame = (0, 255, 0) if imgData['RESULT']=='OK' else (0, 0, 255) 
	w,h = 2448,2048
	thickness = 20
	thicknessOff = 30
	# Create background rectangle with color
	#cv2.rectangle(imgCam1Cycle1, (x,x), (x + w, y + h), (0,255,0), -1)
	cv2.line(img, (thicknessOff		, thicknessOff), 		(w-thicknessOff,	thicknessOff), 		colorFrame, thickness)
	cv2.line(img, (w-thicknessOff	, thicknessOff), 		(w-thicknessOff,	h-thicknessOff), 	colorFrame, thickness)
	cv2.line(img, (w-thicknessOff	,	h-thicknessOff), 	(thicknessOff,		h-thicknessOff), 	colorFrame, thickness)
	cv2.line(img, (thicknessOff		,	h-thicknessOff), 	(thicknessOff,		thicknessOff), 		colorFrame, thickness)

def SetImgTextInfo(img):
	font                   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (130,1000)
	fontScale              = 5
	fontColor              = (222,222,222)
	thickness              = 15
	lineType               = 3

	cv2.putText(img, 
		time.ctime(time.time()), 
	    bottomLeftCornerOfText, 
	    font, 
	    fontScale,
	    fontColor,
	    thickness,
	    lineType)

def CreateImage(path, numCycle, imgListCam):
	validResult = 0
	for data in imgListCam:
		if data['CYCLE']==str(numCycle):
			print('---> {0}'.format(data))
			validResult = numCycle
			img = cv2.imread(path + '/' + data['PATH'], cv2.IMREAD_COLOR)
			SetImgText(img, data)

			pathimg = ('{0}/{1}'.format(path, data['PATH']))
			pathimglength = len(pathimg)-4
			pathpng = ('{0}/{1}'.format(path, data['PATH']))[:pathimglength]+'.png'
			if (os.path.exists(pathpng) == True):
				image_bgr = cv2.imread(pathpng, cv2.IMREAD_COLOR)

				h, w, c = image_bgr.shape
				# append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
				image_bgra = np.concatenate([image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
				# create a mask where white pixels ([255, 255, 255]) are True
				white = np.all(image_bgr == [255, 255, 255], axis=-1)
				# change the values of Alpha to 0 for all the white pixels
				image_bgra[white, -1] = 0
				img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)
				dst = cv2.resize(image_bgra, (2448, 2048))
				added_image = cv2.addWeighted(img,0.4,dst,0.6,0)
				return added_image
			else:
				return img
			
	if validResult==0:
		img = np.zeros((2048, 2448, 3), dtype=np.uint8)
		return img

###########################################################
### MAIN                                                ###
###########################################################

while True:

	time.sleep(3)

	dirListCam1 = os.listdir(pathCam1)
	dirListCam2 = os.listdir(pathCam2)
	dirListCam3 = os.listdir(pathCam3)

	imgListCam1 = []
	imgListCam2 = []
	imgListCam3 = []

	print()
	print('#####################################################################')

	if keyboard.is_pressed('ctrl'):
		break
	
	print()
	print('CAMERA1')
	imgListCam1 = GetListOfImages(dirListCam1, SNToFindCam1, 1, pathCam1)
	printImgListCam(imgListCam1, 'CAMERA1')

	print()
	print('CAMERA2')
	imgListCam2 = GetListOfImages(dirListCam2, SNToFindCam2, 2, pathCam2)
	printImgListCam(imgListCam2, 'CAMERA2')

	print()
	print('CAMERA3')
	imgListCam3.append(GetListOfImages(dirListCam3, SNToFindCam3_1, 3, pathCam3)[0]) 
	imgListCam3.append(GetListOfImages(dirListCam3, SNToFindCam3_2, 3, pathCam3)[0])
	imgListCam3.append(GetListOfImages(dirListCam3, SNToFindCam3_3, 3, pathCam3)[0])
	imgListCam3.append(GetListOfImages(dirListCam3, SNToFindCam3_4, 3, pathCam3)[0])
	printImgListCam(imgListCam3, 'CAMERA3')
	print()

	imgCam1Cycle1 = CreateImage(pathCam1, 1, imgListCam1)
	imgCam1Cycle2 = CreateImage(pathCam1, 2, imgListCam1)
	imgCam1Cycle3 = CreateImage(pathCam1, 3, imgListCam1)	
	imgCam1Cycle4 = CreateImage(pathCam1, 4, imgListCam1)

	imgCam2Cycle1 = CreateImage(pathCam2, 1, imgListCam2)
	imgCam2Cycle2 = CreateImage(pathCam2, 2, imgListCam2)
	imgCam2Cycle3 = CreateImage(pathCam2, 3, imgListCam2)	
	imgCam2Cycle4 = CreateImage(pathCam2, 4, imgListCam2)
	imgCam2Cycle5 = CreateImage(pathCam2, 5, imgListCam2)
	imgCam2Cycle6 = CreateImage(pathCam2, 6, imgListCam2)

	imgCam3Cycle1 = CreateImage(pathCam3, 1, imgListCam3)
	imgCam3Cycle2 = CreateImage(pathCam3, 2, imgListCam3)
	imgCam3Cycle3 = CreateImage(pathCam3, 3, imgListCam3)	
	imgCam3Cycle4 = CreateImage(pathCam3, 4, imgListCam3)

	imgInfo1 = np.zeros((2048, 2448, 3), dtype=np.uint8)
	imgInfo2 = np.zeros((2048, 2448, 3), dtype=np.uint8)

	
	SetImgTextInfo(imgInfo1)

	try:
		cv2.namedWindow("ph-industry primercheck evaluation", cv2.WINDOW_KEEPRATIO)
		cv2.setWindowProperty("ph-industry primercheck evaluation", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
		# Create a 4x4 grid of images
		x1th_row = np.hstack((imgCam1Cycle4, imgCam2Cycle5, imgCam2Cycle6, 	imgCam3Cycle4))
		x2th_row = np.hstack((imgCam1Cycle3, imgCam2Cycle4, imgInfo1, 			imgCam3Cycle3))
		x3th_row = np.hstack((imgCam1Cycle2, imgCam2Cycle3, imgInfo2, 			imgCam3Cycle2))
		x4th_row = np.hstack((imgCam1Cycle1, imgCam2Cycle1, imgCam2Cycle2, 	imgCam3Cycle1))
		grid = np.vstack((x1th_row, x2th_row, x3th_row, x4th_row))
		cv2.imshow("ph-industry primercheck evaluation", grid)
		#1 ms for painting
		cv2.waitKey(10)
		#Block for 0.01 seconds
		time.sleep(0.01)
		#Wait 1 seconds for button press
		cv2.waitKey(1)
	except:
		print('ERROR: Create CV2.Image')
	
	
cv2.destroyAllWindows()
