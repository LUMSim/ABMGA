import sys
import csv
import statistics
import os.path

# indices of data read from the file. The last few will change based on the fitness function
IND = 0
GENES = 1
MUTATION = 2
TARGET = 3
MAXGEN = 4
REPLICATE = 5
ELITISM = 6
TOURNAMENT = 7
MAXTIME = 8
ACTUALGEN = 9
BESTFITNESS = 10
REALTIME_S = 11
USERTIME_S = 12
SYSTIME_S = 13
REALTIME_M = 14
USERTIME_M = 15
SYSTIME_M = 16
INITSHEEP = 17
INITWOLF = 18
SHEEPREP = 19
WOLFREP = 20
SHEEPGAIN = 21
WOLFGAIN = 22
GRASSGROW = 23
RESULTS = 25 #25 FOR GAS, STDSHP, STDAGT RUNS


#lists are mutable, so changes to fullllist are returned without a return statement
def add_to_list(fulllist,toaddlist,index):
	if len(toaddlist) > 0:
		fulllist[index].append(sum(toaddlist)/len(toaddlist))
		fulllist[index].append(statistics.pstdev(toaddlist))
	else:
		fulllist[index].append(0)
		fulllist[index].append(0)


def count_results(datalist,values,index):
	mydict = {}
	mydict["swg"] = 0
	mydict["sdie"] = 0
	mydict["wdie"] = 0
	mydict["s10k"] = 0
	mydict["w10k"] = 0
	for sublist in values:
		if len(sublist) == 1:
			mydict[sublist[0].lower().strip()]+=3
		elif len(sublist) == 2:
			mydict[sublist[0].lower().strip()]+=2
			mydict[sublist[1].lower().strip()]+=1
		elif len(sublist) == 3:
			mydict[sublist[0].lower().strip()]+=1
			mydict[sublist[1].lower().strip()]+=1
			mydict[sublist[2].lower().strip()]+=1
		else:
			print("Error in analyzing results. More than three results reported for a single run")
		#print(sublist)
		#print(mydict)
	datalist[index].append(mydict["swg"])
	datalist[index].append(mydict["sdie"])
	datalist[index].append(mydict["wdie"])
	datalist[index].append(mydict["s10k"])
	datalist[index].append(mydict["w10k"])



def alldata_averagesameparams(fulldata,grass):
	#get only data with grass on (could also check number of genes instead)
	if grass:
		data = [d for d in fulldata if d[GRASSGROW] != "-1" and d[REPLICATE]=="10"]
	else:
		data = [d for d in fulldata if d[GRASSGROW] == "-1" and d[REPLICATE]=="10"]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	#each row lists target, individual, mut, elite, then list of all generation numbers that match that
	generations = [["function","grass","target","individual","mutation","elitism","GenA","GenS","realA","realS","sysuserA","sysuserS","bestA","bestS","numValues","swg","sdie","wdie","s10k","w10k"]]
	index = 1
	for target in ["95","99","100"]:
		for individual in ["6","10","20"]:
			for mut in ["10","20","30","40","50","60","70","80"]:		
				for elite in ["0","2"]:
					#first two lines can be removed and then a row of zeros will be added instead if it doesn't exist in ths dataset
					values = [d for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
					if len(values) > 0:
						generations.append([target])
						generations[index].append(individual)
						generations[index].append(mut)
						generations[index].append(elite)
						values = [int(d[ACTUALGEN]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
						add_to_list(generations,values,index)
						values = [float(d[REALTIME_M]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target and d[REALTIME_M]!=""]
						add_to_list(generations,values,index) 
						values = [float(d[SYSTIME_M])+float(d[USERTIME_M]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target and d[SYSTIME_M]!="" and d[USERTIME_M]!=""]
						add_to_list(generations,values,index)
						values = [float(d[BESTFITNESS]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
						add_to_list(generations,values,index)
						generations[index].append(len(values))
						values = [d[RESULTS].split("/") for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
						count_results(generations,values,index)
						index += 1
				if individual == "20": #elite value of 4 is only valid if there are 20 individuals
					elite = "4"
					#first two lines can be removed and then a row of zeros will be added instead if it doesn't exist in ths dataset
					values = [d for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
					if len(values) > 0:
						generations.append([target])
						generations[index].append(individual)
						generations[index].append(mut)
						generations[index].append(elite)
						values = [int(d[ACTUALGEN]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
						add_to_list(generations,values,index)
						values = [float(d[REALTIME_M]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target and d[REALTIME_M]!=""]
						add_to_list(generations,values,index) 
						values = [float(d[SYSTIME_M])+float(d[USERTIME_M]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target  and d[SYSTIME_M]!="" and d[USERTIME_M]!=""]
						add_to_list(generations,values,index)
						values = [float(d[BESTFITNESS]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
						add_to_list(generations,values,index)
						generations[index].append(len(values))
						values = [d[RESULTS].split("/") for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
						count_results(generations,values,index)
						index +=1

	return generations


def generations_by_target(fulldata,grass):
	#get only data with grass on (could also check number of genes instead)
	if grass:
		data = [d for d in fulldata if d[GRASSGROW] != "-1"]
	else:
		data = [d for d in fulldata if d[GRASSGROW] == "-1"]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	#each row lists target, individual, mut, elite, then list of all generation numbers that match that
	generations = [["function","grass","target","avgGen","stdGen","totalGen","totalNum"]]
	index = 1
	for target in ["95","99","100"]:
		values = []
		for individual in ["6","10","20"]:
			for mut in ["10","20","30","40","50","60","70","80"]:		
				for elite in ["0","2"]:
					values.extend([int(d[ACTUALGEN]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target])
				if individual == "20": #elite value of 4 is only valid if there are 20 individuals
					elite = "4"
					values.extend([int(d[ACTUALGEN]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target])
		if len(values) > 0:
			generations.append([target])
			generations[index].append(sum(values)/len(values))
			generations[index].append(statistics.pstdev(values))
			generations[index].append(sum(values))
			generations[index].append(len(values))

			index +=1

	return generations


def generations_by_ind_target(fulldata,grass):
	#get only data with grass on (could also check number of genes instead)
	if grass:
		data = [d for d in fulldata if d[GRASSGROW] != "-1"]
	else:
		data = [d for d in fulldata if d[GRASSGROW] == "-1"]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	#each row lists target, individual, mut, elite, then list of all generation numbers that match that
	generations = [["function","grass","target","individual","avgGen","stdGen","totalGen","totalNum"]]
	index = 1
	for target in ["95","99","100"]:
		for individual in ["6","10","20"]:
			values = []
			for mut in ["10","20","30","40","50","60","70","80"]:		
				for elite in ["0","2"]:
					values.extend([int(d[ACTUALGEN]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target])
				if individual == "20": #elite value of 4 is only valid if there are 20 individuals
					elite = "4"
					values.extend([int(d[ACTUALGEN]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target])
			if len(values) > 0:
				generations.append([target])
				generations[index].append(individual)
				generations[index].append(sum(values)/len(values))
				generations[index].append(statistics.pstdev(values))
				generations[index].append(sum(values))
				generations[index].append(len(values))

				index +=1

	return generations


def generations_by_ind_target_boxplot(fulldata,grass):
	#get only data with grass on (could also check number of genes instead)
	if grass:
		data = [d for d in fulldata if d[GRASSGROW] != "-1"]
	else:
		data = [d for d in fulldata if d[GRASSGROW] == "-1"]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	#each row lists target, individual, mut, elite, then list of all generation numbers that match that
	generations = [["function","grass","target","individual","values"]]
	index = 1
	for target in ["95","99","100"]:
		for individual in ["6","10","20"]:
			values = []
			for mut in ["10","20","30","40","50","60","70","80"]:		
				for elite in ["0","2","4"]:
					values.extend([int(d[ACTUALGEN]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target])
			if len(values) > 0:
				generations.append([target])
				generations[index].append(individual)
				generations[index].extend(values)
				index +=1

	return generations


# grass should be a boolean denoting whether we are calculating for grass runs (true) or non-grass runs(false)
# returns a list that has one column for each GA parameter, followed by average then standard deviation of generations
def generations_by_allparameters(fulldata,grass):
	#get only data with grass on (could also check number of genes instead)
	if grass:
		data = [d for d in fulldata if d[GRASSGROW] != "-1"]
	else:
		data = [d for d in fulldata if d[GRASSGROW] == "-1"]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	#each row lists target, individual, mut, elite, then list of all generation numbers that match that
	generations = [["function","grass","target","individual","mutation","elitism","avgGen","stdGen"]]
	index = 1
	for target in ["95","100"]:
		for individual in ["6","10","20"]:
			for mut in ["10","20","30","40","50","60","70","80"]:		
				for elite in ["0","2","4"]:
					values = [int(d[ACTUALGEN]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
					if len(values) > 0:
						generations.append([target])
						generations[index].append(individual)
						generations[index].append(mut)
						generations[index].append(elite)
						generations[index].append(sum(values)/len(values))
						if len(values) > 1:
							generations[index].append(statistics.pstdev(values))
						else:
							generations[index].append(0)
						index += 1

	return generations


# grass should be a boolean denoting whether we are calculating for grass runs (true) or non-grass runs(false)
# returns a list that has one column for each GA parameter, followed by average then standard deviation of generations
def generations_by_allparameters_boxplot(fulldata,grass):
	#get only data with grass on (could also check number of genes instead)
	if grass:
		data = [d for d in fulldata if d[GRASSGROW] != "-1"]
	else:
		data = [d for d in fulldata if d[GRASSGROW] == "-1"]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	#each row lists target, individual, mut, elite, then list of all generation numbers that match that
	generations = [["function","grass","target","individual","mutation","elitism","values"]]
	index = 1
	for target in ["95","100"]:
		for individual in ["6","10","20"]:
			for mut in ["10","20","30","40","50","60","70","80"]:		
				for elite in ["0","2","4"]:
					values = [int(d[ACTUALGEN]) for d in data if d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
					if len(values) > 0:
						generations.append([target])
						generations[index].append(individual)
						generations[index].append(mut)
						generations[index].append(elite)
						generations[index].extend(values)
						index += 1

	return generations


# grass should be a boolean denoting whether we are calculating for grass runs (true) or non-grass runs(false)
# returns a list that has one column for each GA parameter, followed by average then standard deviation of generations
def generations_by_allparameters_withresult(fulldata,grass):
	#get only data with grass on (could also check number of genes instead)
	if grass:
		data = [d for d in fulldata if d[GRASSGROW] != "-1"]
	else:
		data = [d for d in fulldata if d[GRASSGROW] == "-1"]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	#each row lists target, individual, mut, elite, then list of all generation numbers that match that
	generations = [["function","grass","target","individual","mutation","elitism","result","avgGen","stdGen"]]
	index = 1
	for target in ["95","100"]:
		for individual in ["6","10","20"]:
			for mut in ["10","20","30","40","50","60","70","80"]:		
				for elite in ["0","2","4"]:
					for res in ["swg","s10k","sdie","wdie","w10k"]: #IGNORES anything with multiple possible results
						values = [int(d[ACTUALGEN]) for d in data if d[RESULTS].strip()==res and d[MUTATION]==mut and d[IND]==individual and d[ELITISM] == elite and d[TARGET] == target]
						if len(values) > 0:
							generations.append([target]) #create the new list at index, then append each item to it
							generations[index].append(individual)
							generations[index].append(mut)
							generations[index].append(elite)
							generations[index].append(res)
							generations[index].append(sum(values)/len(values))
							#can't find standard deviation of one value:
							if len(values) > 1:
								generations[index].append(statistics.pstdev(values))
							else:
								generations[index].append(0)
							index += 1

	return generations


# Helper function for alltime_by_target_ind_gens, to be called for each list
def helper_addavgstdev(generations, index, values):
	if len(values) > 0:
		generations[index].append(sum(values))
		generations[index].append(len(values))
		generations[index].append(sum(values)/len(values))
		#can't find standard deviation of one value:
		if len(values) > 1:
			generations[index].append(statistics.pstdev(values))
		else:
			generations[index].append(0)
	else:
		generations.extend([0,0])


# grass should be a boolean denoting whether we are calculating for grass runs (true) or non-grass runs(false)
# returns a list that has one column for each GA parameter combo, followed by average then standard deviation of each time amount
def alltime_by_target_ind_gens(fulldata,grass):
	#get only data with grass on (could also check number of genes instead)
	if grass:
		data = [d for d in fulldata if d[GRASSGROW] != "-1"]
	else:
		data = [d for d in fulldata if d[GRASSGROW] == "-1"]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	#each row lists target, individual, mut, elite, then list of all generation numbers that match that
	generations = [["function","grass","target","individual","finished?","sumRealM","lenRealM","avgRealM","stdRealM","sumUserM","lenUserM","avgUserM","stdUserM","sumSysM","lenSysM","avgSysM","stdSysM"]]
	index = 1
	for target in ["95","99","100"]:
		for individual in ["6","10","20"]:
			for finished in ["y","n"]:
				if finished == "y":		
					values_R = [float(d[REALTIME_M]) for d in data if d[REALTIME_M] != "" and d[IND]==individual and d[TARGET] == target and d[ACTUALGEN] != "1000"]
					values_U = [float(d[USERTIME_M]) for d in data if d[USERTIME_M] != "" and d[IND]==individual and d[TARGET] == target and d[ACTUALGEN] != "1000"]
					values_S = [float(d[SYSTIME_M]) for d in data if d[SYSTIME_M] != "" and d[IND]==individual and d[TARGET] == target and d[ACTUALGEN] != "1000"]
				else:
					values_R = [float(d[REALTIME_M]) for d in data if d[REALTIME_M] != "" and d[IND]==individual and d[TARGET] == target and d[ACTUALGEN] == "1000"]
					values_U = [float(d[USERTIME_M]) for d in data if d[USERTIME_M] != "" and d[IND]==individual and d[TARGET] == target and d[ACTUALGEN] == "1000"]
					values_S = [float(d[SYSTIME_M]) for d in data if d[SYSTIME_M] != "" and d[IND]==individual and d[TARGET] == target and d[ACTUALGEN] == "1000"]
				if len(values_R) > 0 or len(values_S) > 0 or len(values_U) > 0:
					generations.append([target]) #create the new list at index, then append each item to it
					generations[index].append(individual)
					generations[index].append(finished)
					helper_addavgstdev(generations,index,values_R)
					helper_addavgstdev(generations,index,values_U)
					helper_addavgstdev(generations,index,values_S)
					index += 1

	return generations


# grass should be a boolean denoting whether we are calculating for grass runs (true) or non-grass runs(false)
# returns a list that has one column for each GA parameter combo, followed by average then standard deviation of each time amount
def timepergeneration_by_target_ind_result(fulldata,grass):
	#get only data with grass on (could also check number of genes instead)
	if grass:
		data = [d for d in fulldata if d[GRASSGROW] != "-1"]
	else:
		data = [d for d in fulldata if d[GRASSGROW] == "-1"]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	#each row lists target, individual, mut, elite, then list of all generation numbers that match that
	generations = [["function","grass","target","individual","result","realTimeByGeneration"]]
	index = 1
	for target in ["95","99","100"]:
		for individual in ["6","10","20"]:	
			for result in ["swg","wdie","sdie","s10k","w10k"]:
				values_R = [float(d[REALTIME_M])/float(d[ACTUALGEN]) for d in data if d[REALTIME_M] != "" and d[IND]==individual and d[TARGET] == target and d[RESULTS] == result]
				if len(values_R) > 0:
					for value in values_R:
						generations.append([target]) #create the new list at index, then append each item to it
						generations[index].append(individual)
						generations[index].append(result)
						generations[index].append(value)
						index += 1

	return generations


#for now, only process grass data
#need one row with columns for each mutation rate and individual combo's average and stddev
def grass_time_by_mutation_individuals(fulldata,target):
	#get only data with grass on (could also check number of genes instead)
	grassdata = [d for d in fulldata if d[GRASSGROW] != "-1" and d[TARGET]==target]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	realtime = [[] for i in range(12)]
	index = 0
	for individual in ["6","10","20"]:
		for mut in ["10","20","30","40","50","60","70","80"]:
			realtime[index] = [float(d[REALTIME_M]) for d in grassdata if d[MUTATION]==mut and d[IND]==individual]
			index +=1

	finaldata = [[] for i in range(12*2+1)] #for each set in realtime, need average and stddev
	finaldata[0] = ["function","target","i6m10avg","i6m10std","i6m20avg","i6m20std","i6m30avg","i6m30std","i6m40avg","i6m40std",\
		"i10m10avg","i10m10std","i10m20avg","i10m20std","i10m30avg","i10m30std","i10m40avg","i10m40std",\
		"i20m10avg","i20m10std","i20m20avg","i20m20std","i20m30avg","i20m30std","i20m40avg","i20m40std",]
	final_i = 1
	for i in range(len(realtime)):
		#if there is no data, average and stddev are 0
		if len(realtime[i]) == 0:
			finaldata[final_i] = 0
			finaldata[final_i+1] = 0
		#if there is data, save average then standard deviation into finaldata
		else:
			finaldata[final_i] = sum(realtime[i])/len(realtime[i])
			finaldata[final_i+1] = statistics.pstdev(realtime[i])
		final_i += 2 #skip ahead to next index for finaldata list
	return finaldata

#for now, only process grass data
#need one row with columns for each mutation rate and individual combo's average and stddev
def grass_nonparallel_time_by_mutation_individuals(fulldata,target):
	#get only data with grass on (could also check number of genes instead)
	grassdata = [d for d in fulldata if d[GRASSGROW] != "-1" and d[TARGET]==target]

	#store real time per mutation rate and individuals
	#all data for 6 individuals, then for 10, then for 20. Mutation rates in order.
	realtime = [[] for i in range(12)]
	index = 0
	for individual in ["6","10","20"]:
		for mut in ["10","20","30","40","50","60","70","80"]:
			realtime[index] = [float(d[SYSTIME_M])+float(d[USERTIME_M]) for d in grassdata if d[MUTATION]==mut and d[IND]==individual]
			index +=1

	finaldata = [[] for i in range(12*2+1)] #for each set in realtime, need average and stddev
	finaldata[0] = ["function","target","i6m10avg","i6m10std","i6m20avg","i6m20std","i6m30avg","i6m30std","i6m40avg","i6m40std",\
		"i10m10avg","i10m10std","i10m20avg","i10m20std","i10m30avg","i10m30std","i10m40avg","i10m40std",\
		"i20m10avg","i20m10std","i20m20avg","i20m20std","i20m30avg","i20m30std","i20m40avg","i20m40std",]
	final_i = 1
	for i in range(len(realtime)):
		#if there is no data, average and stddev are 0
		if len(realtime[i]) == 0:
			finaldata[final_i] = 0
			finaldata[final_i+1] = 0
		#if there is data, save average then standard deviation into finaldata
		else:
			finaldata[final_i] = sum(realtime[i])/len(realtime[i])
			finaldata[final_i+1] = statistics.pstdev(realtime[i])
		final_i += 2 #skip ahead to next index for finaldata list
	return finaldata



def readfile(filename):
	data = []

	try:
		fd = open(filename,"r")
		fd.readline() #GET RID OF TITLE LINE
		reader = csv.reader(fd)

		#can reference each column by the name that was in the first row
		for line in reader:
			if line[REPLICATE] == "10": #ignore lines with different number of replcations
				data.append(line)
		fd.close()
	except:
		print("Exception")
		return -1

	return data


#for debugging output only
def print_list(thelist):
	for i in range(len(thelist)):
		print(thelist[i])


def print_header(thelist,filename):
	try:
		if not os.path.exists(filename):
			fd = open(filename,"w")
			for item in thelist[0]:
				print(item,end=",",file=fd)
			print("",file=fd)
			fd.close()
	except:
		print("Error in writing the header to the file")


#append data to the file
#if file doesn't exist, first print out the headers
def append_to_file(thelist,function,initvalues,filename):
	#if the file doesn't already exist, add the header information
	print_header(thelist,filename)

	#append the data from the list to a row of the file
	try:
		fd = open(filename,"a")
		print(function,end=",",file=fd)
		for value in initvalues:
			print(value,end=",",file=fd)
		for index in range(1,len(thelist)-1): #skip first row, as header row, and last row
			print(thelist[index],end=",",file=fd)
		print(thelist[-1],file=fd) #print last row with line break instead of comma
		fd.close()
	except:
		print("Error in writing data to the file")


#append data to the file
#if file doesn't exist, first print out the headers
def append_to_file_lists(thelist,function,initvalues,filename):
	#if the file doesn't already exist, add the header information
	print_header(thelist,filename)

	#append the data from the list to a row of the file
	try:
		fd = open(filename,"a")
		for row in range(1,len(thelist)): 
			print(function,end=",",file=fd)
			for value in initvalues:
				print(value,end=",",file=fd)
			for index in range(len(thelist[row])-1):
				print(thelist[row][index],end=",",file=fd)
			print(thelist[row][-1],file=fd) #print last row with line break instead of comma
		fd.close()
	except:
		print("Error in writing data to the file")


def main():
	filename = sys.argv[1]
	function = sys.argv[2]
	global RESULTS
	if function.strip() == "NTK": #NTICKS
		RESULTS = 24
	if function.strip()[:3] == "AVG": #OVRTME
		RESULTS = 27
	data = readfile(filename)
	print("Processing: ",function, len(data))

	#calculate real time data by target, individual number, and mutation rate
	# timedata95 = grass_time_by_mutation_individuals(data,"95")
	# timedata100 = grass_time_by_mutation_individuals(data,"100")
	# append_to_file(timedata95,function,[95],"grass_realtime_by_ind_mut.csv")
	# append_to_file(timedata100,function,[100],"grass_realtime_by_ind_mut.csv")

	#calculate user time plus system time by target, individual number, and mutation rate
	# partime95 = grass_nonparallel_time_by_mutation_individuals(data,"95")
	# partime100 = grass_nonparallel_time_by_mutation_individuals(data,"100")
	# append_to_file(partime95,function,[95],"grass_nonparalleltime_by_ind_mut.csv")
	# append_to_file(partime100,function,[100],"grass_nonparalleltime_by_ind_mut.csv")

	#number of generations broken up by all GA parameters
	# gendatatrue = generations_by_allparameters(data,True)
	# gendatafalse = generations_by_allparameters(data,False)
	# append_to_file_lists(gendatatrue,function,[1],"generationdata_by_GAparameters.csv")
	# append_to_file_lists(gendatafalse,function,[0],"generationdata_by_GAparameters.csv")

	#number of generations broken up by all GA parameters
	# gendatatrue = generations_by_allparameters_boxplot(data,True)
	# gendatafalse = generations_by_allparameters_boxplot(data,False)
	# append_to_file_lists(gendatatrue,function,[1],"generationdata_by_GAparameters_boxplot.csv")
	# append_to_file_lists(gendatafalse,function,[0],"generationdata_by_GAparameters_boxplot.csv")

	#number of generations broken up by all GA parameters
	# gendatatrue = generations_by_allparameters_withresult(data,True)
	# gendatafalse = generations_by_allparameters_withresult(data,False)
	# append_to_file_lists(gendatatrue,function,[1],"generationdata_by_GAparameters_result.csv")
	# append_to_file_lists(gendatafalse,function,[0],"generationdata_by_GAparameters_result.csv")

	#number of generations only caring about target and individual combo differences
	# indgendatatrue = generations_by_ind_target(data,True)
	# indgendatafalse = generations_by_ind_target(data,False)
	# append_to_file_lists(indgendatatrue,function,[1],"generationdata_by_ind_target.csv")
	# append_to_file_lists(indgendatafalse,function,[0],"generationdata_by_ind_target.csv")

	#number of generations only caring about target and individual combo differences
	# indgendatatrue = generations_by_ind_target_boxplot(data,True)
	# indgendatafalse = generations_by_ind_target_boxplot(data,False)
	# append_to_file_lists(indgendatatrue,function,[1],"generationdata_by_ind_target_boxplot.csv")
	# append_to_file_lists(indgendatafalse,function,[0],"generationdata_by_ind_target_boxplot.csv")

	#number of generations broken up by target
	# gendatatrue = generations_by_target(data,True)
	# gendatafalse = generations_by_target(data,False)
	# append_to_file_lists(gendatatrue,function,[1],"generationdata_by_target.csv")
	# append_to_file_lists(gendatafalse,function,[0],"generationdata_by_target.csv")

	#get all data averaged on identical GA parameters
	# alldataT = alldata_averagesameparams(data,True)
	# alldataF = alldata_averagesameparams(data,False)
	# append_to_file_lists(alldataT,function,[1],"alldata_averages.csv")
	# append_to_file_lists(alldataF,function,[0],"alldata_averages.csv")

	#find average R/U/S time for each target, grass, and indiividual number
	# alltimeT = alltime_by_target_ind_gens(data,True)
	# alltimeF = alltime_by_target_ind_gens(data,False)
	# append_to_file_lists(alltimeT,function,[1],"alltime_target_ind_averages.csv")
	# append_to_file_lists(alltimeF,function,[0],"alltime_target_ind_averages.csv")

	#find realtime/generation, for each target, grass, individual, and result
	gentimeT = timepergeneration_by_target_ind_result(data,True)
	gentimeF = timepergeneration_by_target_ind_result(data,False)
	append_to_file_lists(gentimeT,function,[1],"gentime_target_ind_result.csv")
	append_to_file_lists(gentimeF,function,[0],"gentime_target_ind_result.csv")

	

main()
			
