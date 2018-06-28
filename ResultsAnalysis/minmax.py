# Purpose: To read through the results of the analysis of runs and put the min/max data into a useable format to copy/paste 
# into the CSV files. Need to average the three runs of the same parameters and find standard deviation of them.

import sys
import statistics

filename = sys.argv[1]

def deal_with_line(split, values):
	#print("processing ",split)
	if (split[0][0]=="f" and (len(split) == 5 or len(split) == 6)) or (split[0][0]=="t" and (len(split) == 7 or len(split) == 8)) : #valid data row
		#parameters = split[0].split("-")
		#for i in range(1,len(parameters)):
		#	print(parameters[i],end=",")
		smin = int(split[1])
		smax = int(split[2])
		wmin = int(split[3])
		wmax = int(split[4])
		values[0].append((smin+smax)/2)
		values[1].append((wmin+wmax)/2)
		if split[0][0]=="t":
			values[2].append(float(split[5])+float(split[6])/2)
	else:
		print("Surprise! Invalid row in middle of valid data: ",split)


def deal_with_line_swgonly(split, values):
	#print("processing ",split)
	if (split[0][0]=="f" and (len(split) == 5 or len(split) == 6)) or (split[0][0]=="t" and (len(split) == 7 or len(split) == 8)) : #valid data row
		if (split[0][0]=="f" and len(split) == 5) or (split[0][0]=="t" and len(split) == 7): #swg means there isn't a final column
			smin = int(split[1])
			smax = int(split[2])
			wmin = int(split[3])
			wmax = int(split[4])
			if smax < 9000 and wmax < 9000: #s10k and w10k weren't always calculated correctly
				values[0].append((smin+smax)/2)
				values[1].append((wmin+wmax)/2)
				if split[0][0]=="t":
					values[2].append(float(split[5])+float(split[6])/2)
	else:
		print("Surprise! Invalid row in middle of valid data: ",split)


def allrows():
	try:
		fd = open(filename,"r")
		line = fd.readline()
		while ".csv" in line or ".nlogo" in line or len(line)<2: #skip irrelevant rows
			#print("ignoring ",line.strip())
			line = fd.readline()

		#Now we are at the relevant lines, which are all together at tne end of the file
		while line != "":
			values = [[],[],[]]
			split = line.strip().split()
			parameters = split[0].strip()
			deal_with_line(split,values)

			#second line of same parameters
			line = fd.readline()
			split = line.strip().split()
			if split[0].strip()[:-2] != parameters[:-2]: #last two characters are run number, which will be different for each run
				print("ERROR! Second item is not same paramters as first in set: ",parameters,split[0])
				print("Ending, as can't recover.")
				sys.exit(-1)
			else:
				deal_with_line(split,values)

			#third line of same parameters
			line = fd.readline()
			split = line.strip().split()
			if split[0].strip()[:-2] != parameters[:-2]:
				print("ERROR! Third item is not same paramters as first in set: ",parameters,split[0])
				print("Ending, as can't recover.")
				sys.exit(-1)
			else:
				deal_with_line(split,values)

			print(split[0],end=",")
			if split[0][0] == "f":
				print("{:4.3f}".format(statistics.mean(values[0])),"{:4.3f}".format(statistics.pstdev(values[0])),"{:4.3f}".format(statistics.mean(values[1])),"{:4.3f}".format(statistics.pstdev(values[1])),sep=",")
			else:
				print("{:4.3f}".format(statistics.mean(values[0])),"{:4.3f}".format(statistics.pstdev(values[0])),"{:4.3f}".format(statistics.mean(values[1])),"{:4.3f}".format(statistics.pstdev(values[1])),"{:4.3f}".format(statistics.mean(values[2])),"{:4.3f}".format(statistics.pstdev(values[2])),sep=",")
			line = fd.readline()
	except IOError:
		print("Error processing file")


def swgrows():
	try:
		fd = open(filename,"r")
		line = fd.readline()
		while ".csv" in line or ".nlogo" in line or len(line)<2: #skip irrelevant rows
			#print("ignoring ",line.strip())
			line = fd.readline()

		#Now we are at the relevant lines, which are all together at tne end of the file
		while line != "":
			values = [[],[],[]]
			split = line.strip().split()
			parameters = split[0].strip()
			deal_with_line_swgonly(split,values)

			#second line of same parameters
			line = fd.readline()
			split = line.strip().split()
			if split[0].strip()[:-2] != parameters[:-2]: #last two characters are run number, which will be different for each run
				print("ERROR! Second item is not same paramters as first in set: ",parameters,split[0])
				print("Ending, as can't recover.")
				sys.exit(-1)
			else:
				deal_with_line_swgonly(split,values)

			#third line of same parameters
			line = fd.readline()
			split = line.strip().split()
			if split[0].strip()[:-2] != parameters[:-2]:
				print("ERROR! Third item is not same paramters as first in set: ",parameters,split[0])
				print("Ending, as can't recover.")
				sys.exit(-1)
			else:
				deal_with_line_swgonly(split,values)

			print(split[0],end=",")
			for value in values:
				if value == []:
					value.append(0)
			if split[0][0] == "f":
				print("{:4.3f}".format(statistics.mean(values[0])),"{:4.3f}".format(statistics.pstdev(values[0])),"{:4.3f}".format(statistics.mean(values[1])),"{:4.3f}".format(statistics.pstdev(values[1])),sep=",")
			else:
				print("{:4.3f}".format(statistics.mean(values[0])),"{:4.3f}".format(statistics.pstdev(values[0])),"{:4.3f}".format(statistics.mean(values[1])),"{:4.3f}".format(statistics.pstdev(values[1])),"{:4.3f}".format(statistics.mean(values[2])),"{:4.3f}".format(statistics.pstdev(values[2])),sep=",")
			line = fd.readline()
	except IOError:
		print("Error processing file")			


#allrows()
swgrows()
