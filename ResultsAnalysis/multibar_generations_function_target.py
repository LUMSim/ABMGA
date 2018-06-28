# This code assumes that the combine.py has been run to creation the generations function ind data for input

# libraries
#import numpy as np #only needed for example code
#from matplotlib import rc
#import pandas as pd # only needed  for example code
import sys
import multibar as mb

#which data to graph
GRASS = "1"
IND = "10"

#indices
D_AVG = 0
D_STD = 1
D_IND = {"95":0,"99":1,"100":2}

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

		ordering = []

		for line in fd:
			split = line.split(",")
			if split[F_GRASS].strip() == GRASS and split[F_IND]==IND:
				key = split[F_FUNCTION].strip()
				ind = split[F_TGT].strip()
				if not key in data:
					data[key] = [[0,0],[0,0],[0,0]]
					ordering.append(key)
				data[key][D_IND[ind]][D_AVG] = (float(split[F_AVG].strip()))
				data[key][D_IND[ind]][D_STD] = (float(split[F_STD].strip()))

		fd.close()
		return data, ordering

	except:
		print("Error reading and processing input data file. Aborting.")
		sys.exit(-1)


data, ordering = read_data("generationdata_by_ind_target.csv")
#print(process_data)
#ordered = list(process_data.keys())
#ordered.sort()
print(data)

#create file name for plot
plotname = "multibar_generation_function_target_"+IND+"_"+GRASS+".pdf"
mb.plot_data(data,plotname,"Fitness Function","Generations",["95","99","100"],ordering)


