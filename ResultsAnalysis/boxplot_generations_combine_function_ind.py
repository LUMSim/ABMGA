# This code assumes that the combine.py has been run to creation the generations function ind data for input

# libraries
#import numpy as np #only needed for example code
#from matplotlib import rc
#import pandas as pd # only needed  for example code
import sys
import boxplot as bp

#which data to graph
TARGET = "95"
GRASS = "1"

def read_data(filename):
	try:
		fd = open(filename, "r")
		data = {}
		headers = fd.readline().strip().split(",") #get the headers
		#find the index of each column we care about
		F_VALUES = headers.index("values")
		F_TGT = headers.index("target")
		F_GRASS = headers.index("grass")
		F_FUNCTION = headers.index("function")
		F_IND = headers.index("individual")

		ordering = []

		for line in fd:
			split = line.split(",")
			if split[F_TGT] == TARGET and split[F_GRASS].strip() == GRASS and split[F_FUNCTION][:3]!="AVG":
				key = split[F_FUNCTION].strip()+"-"+split[F_IND].strip()
				if not key in data:
					data[key] = []
					ordering.append(key)
				for index in range(int(F_VALUES),len(split)):
					if split[index].isdigit():
						data[key].append(int(split[index]))


		fd.close()
		return data, ordering

	except IOError:
		print("Error reading and processing input data file. Aborting.")
		sys.exit(-1)


data, ordering = read_data("generationdata_by_ind_target_boxplot_only61020.csv")
#print(process_data)
#ordered = list(process_data.keys())
#ordered.sort()
print(data)

#create file name for plot
plotname = "box_generation_combineIND"+TARGET+"_"+GRASS+"BOXnoAVG.pdf"
bp.plot_data(data,plotname,"Fitness Function","Generations",ordering)


