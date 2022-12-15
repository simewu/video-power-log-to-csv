from PIL import Image
import os
import sys

print()
rotationAmount = int(input('How many degrees would you like to rotate the images?: '))

if rotationAmount <= 0 or rotationAmount >= 360:
	print('Invalid rotation amount.')
	sys.exit()

frames = os.listdir('frames/')
for frame in frames:
	filePath = 'frames/' + frame
	print('Rotating', filePath)
	img = Image.open(filePath)
	img.rotate(rotationAmount).save(filePath)
	img.close()