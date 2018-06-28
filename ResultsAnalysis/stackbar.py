import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

#set up dictionary of values indices of lists stored at each key (Function name is key)
D_SWG = 0 #this is the only one to hold the total, as it's the same for all
D_S10K = 1
D_SDIE = 2
D_WDIE = 3
D_W10K = 4

# assumes data has gone through processing so that it only holds percentages
# orders the functions from largest swg percentage to smallest, for graph ordering
def order_functions(data):
	order = []

	for key in data.keys(): #keys are function names
		order.append([data[key][D_SWG],key])

	order.sort(reverse=True)
	#print(order)
	return [d[1] for d in order] 


# Data is a dictionary with function name as key, and values in indices following global index variables
# Ordering is a list of function names in the order they should display across the x-axis
def plot_data(data, ordering,filename,xtitle):
	legend_names = ["swg","s10k","wdie","sdie","w10k"]
	r = list(range(len(ordering)))
	plt.figure(figsize=(7, 5)) #4.5,5.5; set width, height http://mple.m-artwork.eu/tutorial

	#each bar is data[key][<result>], in legend order, ONE BAR PER LEGEND VALUE
	bars = [[] for i in range(5)]
	for item in ordering:
		bars[0].append(data[item][D_SWG])
		bars[1].append(data[item][D_S10K])
		bars[2].append(data[item][D_WDIE])
		bars[3].append(data[item][D_SDIE])
		bars[4].append(data[item][D_W10K])

	#create plot
	barWidth = 0.9
	hatch=['/','','\\','*','-']
	colors=["seagreen","deepskyblue","goldenrod","orangered","maroon"]
	#matplotlib.rc('font', size=14)
	plt.bar(r,bars[0],width=barWidth,label=legend_names[0],hatch=hatch[0],color=colors[0])
	bottom = [0 for i in range(len(ordering))]
	for i in range(1,len(bars)):
		bottom = [x + y for x, y in zip(bottom, bars[i-1])]
		plt.bar(r,bars[i],bottom=bottom,width=barWidth,label=legend_names[i],hatch=hatch[i],color=colors[i])

	a = plt.gca()
	a.set_xticklabels(a.get_xticks(), {'size':14})
	a.set_yticklabels(a.get_yticks(), {'size':14})
	plt.xticks(r,ordering)
	plt.xticks(rotation=40)
	plt.xticks(ha='right')
	plt.xlabel(xtitle,size=14)
	plt.ylabel("Percent Achieving\n Result",size=14)
	plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
	
	plt.tight_layout(pad=7)
	plt.savefig(filename)
	#plt.show()



#data is a dictionary using global indices above. SWG has the total number of runs included for each.
#this function will calculate the percentage each result is for the given function
def process_data_for_plotting(data):
	for key in data.keys():
		denominator = data[key][D_SWG][1]*3
		data[key][D_SDIE] = data[key][D_SDIE]/denominator
		data[key][D_S10K] = data[key][D_S10K]/denominator
		data[key][D_WDIE] = data[key][D_WDIE]/denominator
		data[key][D_W10K] = data[key][D_W10K]/denominator
		data[key][D_SWG] = data[key][D_SWG][0]/denominator

	return data 


def original_plot_code(): 
	# Data
	r = [0,1,2,3,4]
	raw_data = {'greenBars': [20, 1.5, 7, 10, 5], 'orangeBars': [5, 15, 5, 10, 15],'blueBars': [2, 15, 18, 5, 10]}
	df = pd.DataFrame(raw_data)
	 
	# From raw value to percentage
	#each Bar list is for one colored bar across all x-axis categories
	totals = [i+j+k for i,j,k in zip(df['greenBars'], df['orangeBars'], df['blueBars'])]
	greenBars = [i / j * 100 for i,j in zip(df['greenBars'], totals)]
	orangeBars = [i / j * 100 for i,j in zip(df['orangeBars'], totals)]
	blueBars = [i / j * 100 for i,j in zip(df['blueBars'], totals)]

	 
	# plot
	barWidth = 0.85
	names = ('A','B','C','D','E') #x-axis categories
	# Create green Bars
	plt.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth)
	# Create orange Bars, bottom is the top of each green bar's value
	plt.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth)
	# Create blue Bars, bottom sit he top of green +orange bar's values
	plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color='#a3acff', edgecolor='white', width=barWidth)

	print([i+j for i,j in zip(greenBars, orangeBars)])
	 
	# Custom x axis
	plt.xticks(r, names)
	plt.xlabel("group")
	 
	# Show graphic
	plt.show()

