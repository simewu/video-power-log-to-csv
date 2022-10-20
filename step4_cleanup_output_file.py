import csv
import numpy as np
import os
import re
import scipy.stats
import sys
import time

percentileAmount = 10
columnsToInclude = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

# Return the +- value after a set of data
def percentile(data, p=95):
	a = 1.0 * np.array(data)
	return np.percentile(a, p)

fileName = 'output.csv'
outputfileName = 'finalOutput.csv'

readerFile = open(fileName, 'r')
reader = csv.reader(x.replace('\0', '') for x in readerFile)

header = next(reader)

data = []

for row in reader:
	for i, cell in enumerate(row):
		if len(data) <= i:
			data.append([])
		
		if columnsToInclude[i] == 1:
			num = float(cell)
			data[i].append(num)

readerFile.close()

percentileMin = []
percentileMax = []
for i, array in enumerate(data):
	pmin = 0
	pmax = 100
	if columnsToInclude[i] == 1:
		pmin = percentile(array, percentileAmount)
		pmax = percentile(array, 100 - percentileAmount)
	percentileMin.append(pmin)
	percentileMax.append(pmax)


outputFile = open(outputfileName, 'w', newline='')
outputWriter = csv.writer(outputFile)

readerFile = open(fileName, 'r')
reader = csv.reader(x.replace('\0', '') for x in readerFile)

header = next(reader)
outputWriter.writerow(header)

removedRows = 0
totalRows = 0

minValues = [None] * len(percentileMax)
maxValues = [None] * len(percentileMax)

for row in reader:
	totalRows += 1

	validData = True
	for j, cell in enumerate(row):
		if columnsToInclude[j] == 0: continue
		num = float(cell)
		if num < percentileMin[j] or num > percentileMax[j]:
			validData = False
			break # Short circuit

		if minValues[j] == None or num < minValues[j]: minValues[j] = num
		if maxValues[j] == None or num > maxValues[j]: maxValues[j] = num

	if not validData:
		removedRows += 1
		continue

	outputWriter.writerow(row)

readerFile.close()
outputFile.close()
print()
print(f'Removed the top and bottom {percentileAmount}% of data.')
print(f'    {removedRows} out of {totalRows} rows were removed.')
print('Current minimums:', minValues)
print('Current maximums:', maxValues)
print()
print(f'Saved to {outputfileName}')
