from PIL import Image
import cv2
import numpy as np
import os
import pytesseract
import sys
import time

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
everyXframes = 15

if os.path.exists('old_readtext'):
	os.remove('old_readtext')

if os.path.exists('readtext'):
	os.rename('readtext', 'old_readtext')

os.mkdir('readtext')

frameCount = 0
path = os.path.join('frames',f'frame_{frameCount}.jpg')

while os.path.exists(path):
	print('Processing:', path)

	img = Image.open(path).convert('L')
	ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
	img = Image.fromarray(img.astype(np.uint8))
	config = '--psm 6 -c tessedit_char_whitelist="0123456789VAW$. "'
	readData = pytesseract.image_to_string(img, config = config)

	outputPath = os.path.join('readtext',f'frame_{frameCount}.txt')
	file = open(outputPath, 'w')
	file.write(readData)
	file.close()

	print('    Wrote to:', outputPath)

	frameCount += everyXframes
	path = os.path.join('frames',f'frame_{frameCount}.jpg')