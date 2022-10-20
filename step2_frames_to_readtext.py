
import os
import cv2
from PIL import Image
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = os.path.join('C:', os.sep, 'Program Files', 'Tesseract-OCR', 'tesseract.exe')

if not os.path.exists('readtext'):
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

	frameCount += 1
	path = os.path.join('frames',f'frame_{frameCount}.jpg')