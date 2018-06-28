# libraries
#import numpy as np #only needed for example code
#from matplotlib import rc
#import pandas as pd # only needed  for example code
import sys
import stackbar as sb

#which data to graph
TARGET = "95"
GRASS = "1"
IND = "10"


def read_data(filename):
	try:
		fd = open(filename, "r")
		data = {}
		headers = fd.readline().strip().split(",") #get the headers
		#find the index of each column we care about
		F_SWG = headers.index("swg")
		F_S10K = headers.index("s10k")
		F_SDIE = headers.index("sdie")
		F_WDIE = headers.index("wdie")
		F_W10K = headers.index("w10k")
		F_TOTAL = headers.index("numValues")
		F_FUNCTION = headers.index("function")
		F_TGT = headers.index("target")
		F_GRASS = headers.index("grass")
		F_IND = headers.index("individual")

		for line in fd:
			split = line.split(",")
			function = split[F_FUNCTION].strip()
			if split[F_TGT] == TARGET and split[F_GRASS].strip() == GRASS and split[F_IND].strip() == IND: #and split[F_FUNCTION] != "EXT500":
				if function in data:
					data[function][sb.D_SWG][0] += int(split[F_SWG].strip())
					data[function][sb.D_SWG][1] += int(split[F_TOTAL].strip())
					data[function][sb.D_S10K] += int(split[F_S10K].strip())
					data[function][sb.D_SDIE] += int(split[F_SDIE].strip())
					data[function][sb.D_W10K] += int(split[F_W10K].strip())
					data[function][sb.D_WDIE] += int(split[F_WDIE].strip())
				else:
					data[function] = [[] for i in range(5)]
					data[function][sb.D_SWG] = []
					data[function][sb.D_SWG].append(int(split[F_SWG].strip()))
					data[function][sb.D_SWG].append(int(split[F_TOTAL].strip()))
					data[function][sb.D_S10K] = int(split[F_S10K].strip())
					data[function][sb.D_SDIE] = int(split[F_SDIE].strip())
					data[function][sb.D_W10K] = int(split[F_W10K].strip())
					data[function][sb.D_WDIE] = int(split[F_WDIE].strip())

		fd.close()
		return data

	except IOError:
		print("Error reading and processing input data file. Aborting.")
		sys.exit(-1)



data = read_data("alldata_averages.csv")
process_data = sb.process_data_for_plotting(data)
#print(process_data)
ordered = sb.order_functions(process_data)
#ordered = ["EXT1000","NTK","AVG3000"]
#create file name for plot
print(process_data)
plotname = "stackbar_quality_"+TARGET+"_"+IND+"_"+GRASS+".pdf"
sb.plot_data(process_data,ordered,plotname,"Fitness Function")


