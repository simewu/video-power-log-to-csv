from PIL import Image
import cv2
import numpy as np
import os
import pytesseract
import shutil
import sys
import time

logIntermediateFrames = True

pathToTesseract = os.path.join('C:', os.sep, 'Program Files', 'Tesseract-OCR', 'tesseract.exe')
if os.path.exists(pathToTesseract):
	pytesseract.pytesseract.tesseract_cmd = pathToTesseract
else:
	print()
	print('ERROR: Cannot find Tesseract executable.')
	print('You may need to install Tesseract before it can be called using this python script.')
	print('Opening the installation website in 5 seconds...')
	time.sleep(5)
	import webbrowser
	webbrowser.open('https://github.com/UB-Mannheim/tesseract/wiki')
	time.sleep(5)
	print()
	print('Exiting. Please re-run the script when Tesseract is installed.')
	sys.exit()

# Take a sample every X frames
# Set it to 1 to log every frame
# ALSO UPDATE THIS VARIABLE IN step1_video_to_frames.py
everyXframes = 1

# if os.path.exists('old_readtext'):
# 	os.remove('old_readtext')
# if os.path.exists('readtext'):
# 	os.rename('readtext', 'old_readtext')
try:
	shutil.rmtree('readtext')
except: pass
os.mkdir('readtext')

if logIntermediateFrames:
	try:
		shutil.rmtree('intermediate_frames')
	except: pass
	os.mkdir('intermediate_frames')

frameCount = 0
path = os.path.join('frames', f'frame_{frameCount}.jpg')

while os.path.exists(path):
	print('Processing:', path)

	img = Image.open(path).convert('L')
	img = np.array(img)
	img = cv2.equalizeHist(img)
	ret, img = cv2.threshold(img, 175, 255, cv2.THRESH_TOZERO)
	#blur = cv2.GaussianBlur(np.array(img), (11, 11), 0)
	#img = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

	img = Image.fromarray(img.astype(np.uint8))
	if logIntermediateFrames:
		img.save('intermediate_' + path)
	config = '--psm 11 -c tessedit_char_whitelist="0123456789.VAW$ "'
	#config = '--psm 11 -c tessedit_char_whitelist="0123456789.VAW$ "'
	readData = pytesseract.image_to_string(img, config = config)

	outputPath = os.path.join('readtext',f'frame_{frameCount}.txt')
	file = open(outputPath, 'w')
	file.write(readData)
	file.close()

	print('    Wrote to:', outputPath, readData)

	frameCount += everyXframes
	path = os.path.join('frames',f'frame_{frameCount}.jpg')