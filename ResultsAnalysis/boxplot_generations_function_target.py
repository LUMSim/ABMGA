# This code assumes that the combine.py has been run to creation the generations function ind data for input

# libraries
#import numpy as np #only needed for example code
#from matplotlib import rc
#import pandas as pd # only needed  for example code
import sys
import boxplot as bp

#which data to graph
GRASS = "1"
IND = "10"

def read_data(filename):
	try:
		fd = open(filename, "r")
		data = {}
		headers = fd.readline().strip().split(",") #get the headers
		#find the index of each column we care about
		F_IND = headers.index("individual")
		F_TGT = headers.index("target")
		F_GRASS = headers.index("grass")
		F_FUNCTION = headers.index("function")
		F_VALUES = headers.index("values")

		ordering = []

		for line in fd:
			split = line.split(",")
			if split[F_GRASS].strip() == GRASS and split[F_IND]==IND and (split[F_FUNCTION] == "STDA" or split[F_FUNCTION] == "STDS" or split[F_FUNCTION] == "EXT100" or split[F_FUNCTION] == "AVG3000"):
				key = split[F_FUNCTION].strip()+"-"+str(int(split[F_TGT].strip())/100)
				if not key in data:
					data[key] = []
					ordering.append(key)
				for index in range(int(F_VALUES),len(split)):
					if split[index].isdigit():
						data[key].append(int(split[index]))

		fd.close()
		return data, ordering

	except:
		print("Error reading and processing input data file. Aborting.")
		sys.exit(-1)


data, ordering = read_data("generationdata_by_ind_target_boxplot.csv")
#print(process_data)
#ordered = list(process_data.keys())
#ordered.sort()
print(data)

#create file name for plot
plotname = "boxplot_generation_function_target_"+IND+"_"+GRASS+".pdf"
bp.plot_data(data,plotname,"Fitness Function","Generations",ordering)


