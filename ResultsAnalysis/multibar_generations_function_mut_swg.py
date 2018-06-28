# This code assumes that the combine.py has been run to creation the generations function ind data for input

# libraries
#import numpy as np #only needed for example code
#from matplotlib import rc
#import pandas as pd # only needed  for example code
import sys
import multibar as mb

#which data to graph
TARGET = "95"
GRASS = "1"
IND = "10"
ELITE = "2"
RESULT = "swg"

#indices
D_AVG = 0
D_STD = 1
D_IND = {"10":0,"20":1,"30":2,"40":3,"50":4,"60":5,"70":6,"80":7} #whatever is in the bars is listed here to put bars in desired order

def read_data(filename):
	try:
		fd = open(filename, "r")
		data = {}
		headers = fd.readline().strip().split(",") #get the headers
		#find the index of each column we care about
		F_STD = headers.index("stdGen")
		F_AVG = headers.index("avgGen")
		F_IND = headers.index("individual")
		F_TGT = headers.index("target")
		F_GRASS = headers.index("grass")
		F_FUNCTION = headers.index("function")
		F_ELITE = headers.index("elitism")
		F_MUT = headers.index("mutation")
		F_RES = headers.index("result")

		ordering = []

		for line in fd:
			split = line.split(",")
			if split[F_TGT] == TARGET and split[F_GRASS].strip() == GRASS and split[F_IND] == IND and split[F_ELITE].strip() == ELITE and split[F_RES].strip() == RESULT: #and split[F_FUNCTION][:3] != "AVG":
				key = split[F_FUNCTION].strip()
				ind = split[F_MUT].strip()
				if not key in data:
					data[key] = [[0,0] for i in range(len(D_IND))] #[[0,0],[0,0],[0,0],[0,0]]
					ordering.append(key)
				data[key][D_IND[ind]][D_AVG] = (float(split[F_AVG].strip()))
				data[key][D_IND[ind]][D_STD] = (float(split[F_STD].strip()))

		fd.close()
		return data, ordering

	except IOError:
		print("Error reading and processing input data file. Aborting.")
		sys.exit(-1)


data, ordering = read_data("generationdata_by_GAparameters_result.csv")
#print(process_data)
#ordered = list(process_data.keys())
#ordered.sort()
legend = ["10","20","30","40","50","60","70","80"]

if len(data) == 0 or len(ordering) == 0:
	print("There is no data to plot")
else:
	#create file name for plot
	plotname = "multibar_generation_function_mutation_"+TARGET+"_"+GRASS+"_"+IND+"_"+ELITE+"_"+RESULT+".pdf"
	mb.plot_data(data,plotname,"Fitness Function","Generations",legend,ordering)


