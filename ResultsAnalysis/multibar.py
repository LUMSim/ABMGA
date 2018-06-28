import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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
# barorder gives legend name for data in the order they exist within the sublists
# xorder shows what order to access each main dictionary option (x-axis labels; they are keys to primary dictionary)
def plot_data(data,filename,xtitle,ytitle,barorder,xorder):
	legend_names = barorder
	r = np.arange(len(data))

	#ONE BAR PER LEGEND VALUE, first index is average
	bars = [[] for i in range(len(barorder))]
	errors = [[] for i in range(len(barorder))]
	for item in xorder:
		for i in range(len(barorder)):
			bars[i].append(data[item][i][0])
			errors[i].append(data[item][i][1])
	print("bars:",bars)
	print("errors:",errors)
	#create plot
	barWidth = 0.85/len(bars)
	fig,ax=plt.subplots()

	#store placement of each bar
	placement = []
	numBefore = int(len(bars)/2)
	v = list(range(1,numBefore+1))
	v.sort(reverse=True)
	for i in range(len(v)):
		placement.append(r-barWidth*v[i])
	for i in range(len(bars)-numBefore): #first one is zero, so right at r
		placement.append(r+barWidth*i)

	#hatch=['/','','\\','*','-']
	colors=["darkolivegreen","seagreen","deepskyblue","powderblue","goldenrod","gold","orangered","maroon"]
	#matplotlib.rc('font', size=14)
	axes = []
	axes.append(ax.bar(placement[0],bars[0],width=barWidth,yerr=errors[0],color=colors[0]))
	for i in range(1,len(bars)):
		axes.append(ax.bar(placement[i],bars[i],width=barWidth,yerr=errors[i],color=colors[i])) #,label=legend_names[i]

	fontsize = 12
	a = plt.gca()
	a.set_xticklabels(a.get_xticks(), {'size':fontsize})
	a.set_yticklabels(a.get_yticks(), {'size':fontsize})
	
	plt.xticks(r,xorder)
	plt.xticks(rotation=40)
	plt.setp(ax.xaxis.get_majorticklabels(), ha='right')
	plt.xlabel(xtitle,size=fontsize)
	plt.ylabel(ytitle,size=fontsize)
	ax.legend(axes,barorder,loc='upper left', bbox_to_anchor=(1,1), ncol=1)
	#ax.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
	plt.tight_layout(pad=7)
	ax.autoscale(tight=True)
	plt.savefig(filename)
	#plt.show()




