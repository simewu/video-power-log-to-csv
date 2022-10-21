import os
import re
import sys
import csv

# Take a sample every X frames
# Set it to 1 to log every frame
# ALSO UPDATE THIS VARIABLE IN step2_frames_to_readtext.py
everyXframes = 15

outputFile = open('output.csv', 'w')
header = ''
header += 'Frame,'
header += 'Timestamp (s),'
header += 'Voltage (V),'
header += 'Current (A),'
header += 'Power (W),'
header += 'Power Factor (%),'
header += 'Total (kWh),'
header += 'Oneshot (kWh),'
header += 'Total ($),'
header += 'Oneshot ($),'
outputFile.write(header + '\n')

timestampMapFile = open(os.path.join('frames', 'timestamp_map.csv'), 'r')
timestampMapReader = csv.reader(x.replace('\0', '') for x in timestampMapFile)
header = next(timestampMapReader)

frameCount = 0
path = os.path.join('readtext',f'frame_{frameCount}.txt')
numberOfErrors = 0

while os.path.exists(path):
	print('Processing:', path)
	file = open(path, 'r')
	contents = file.read()
	file.close()

	matches = re.findall(r'([0-9]+\.?[0-9]+)\.*[^0-9\.]+\.*([0-9]+\.?[0-9]+)', contents)
	values = []
	for match in matches:
		if len(values) == 0: # First two numbers
			num1 = float(match[0])
			num2 = float(match[1])
			values.append(num1)
			values.append(num2)
			continue

		if len(values) == 2:
			num1 = float(match[0])
			num2 = float(match[1])
			values.append(num1)
			values.append(num2)
			continue

		if len(values) == 4:
			num1 = float(match[0])
			num2 = float(match[1])
			values.append(num1)
			values.append(num2)
			continue

		if len(values) == 6:
			num1 = float(match[0])
			num2 = float(match[1])
			values.append(num1)
			values.append(num2)
			break

	if len(values) == 8:
		timestamp = next(timestampMapReader)
		line = ''
		line += str(int(timestamp[0])) + ','
		line += str(float(timestamp[1]) / 1000) + ','
		line += str(values[0]) + ','
		line += str(values[1]) + ','
		line += str(values[2]) + ','
		line += str(values[3]) + ','
		line += str(values[4]) + ','
		line += str(values[5]) + ','
		line += str(values[6]) + ','
		line += str(values[7]) + ','
		outputFile.write(line + '\n')
	else:
		print('!!! ERROR READING', path)
		# print('[contents start]')
		# print(contents)
		# print('[contents end]')
		numberOfErrors += 1

	frameCount += everyXframes
	path = os.path.join('readtext',f'frame_{frameCount}.txt')

print('Total number of errors:', numberOfErrors, 'out of', frameCount)