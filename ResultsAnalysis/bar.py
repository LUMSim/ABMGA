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
def plot_data(data,filename,xtitle,ytitle,xorder):

	r = np.arange(len(data))
	bars = []
	errors = []
	for item in xorder:
		bars.append(data[item][0])
		errors.append(data[item][1])
	print("bars:",bars)
	print("errors:",errors)

	plt.bar(r,bars,yerr=errors,align="center")

	a = plt.gca()
	a.set_xticklabels(a.get_xticks(), {'size':14})
	a.set_yticklabels(a.get_yticks(), {'size':14})
	
	plt.xticks(r,xorder)
	plt.xticks(rotation=40)
	plt.xlabel(xtitle,size=14)
	plt.ylabel(ytitle,size=14)
	#plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
	#ax.legend(axes,barorder)
	plt.tight_layout(pad=7)
	#ax.autoscale(tight=True)
	plt.savefig(filename)
	#plt.show()




