#boxplot portion based on beginning of http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


# Data is a dictionary with function name as key, and values in indices following global index variables
# barorder gives legend name for data in the order they exist within the sublists
# xorder shows what order to access each main dictionary option (x-axis labels; they are keys to primary dictionary)
def plot_data(data,filename,xtitle,ytitle,xorder):

	bars = []
	for item in xorder:
		bars.append(data[item])
	#print("bars:",bars)

	# Create a figure instance
	fig = plt.figure(1, figsize=(5, 6)) #8,6 or 5,6

	# Create an axes instance
	ax = fig.add_subplot(111)

	# Create the boxplot
	bp = ax.boxplot(bars,notch=False,patch_artist=False) #patch artist activates facecolor

	#stylize the boxplot
	for box in bp['boxes']:
		box.set(linewidth=2)
		#box.set(facecolor='#b3fff4') #fill color

	for w in bp['whiskers']:
		w.set(linewidth=2)

	for c in bp['caps']:
		c.set(linewidth=2)

	for med in bp['medians']:
		med.set(color="#006400", linewidth=2)

	#for fl in bp['fliers']:
	#	fl.set(color="#0000ff",alpha=0.5) #marker='o'
		
	# Save the figure
	#fig.savefig('fig1.png', bbox_inches='tight')

	a = plt.gca()
	a.set_xticklabels(a.get_xticks(), {'size':18})
	a.set_yticklabels(a.get_yticks(), {'size':18})
	plt.setp(ax.xaxis.get_majorticklabels(), ha='right')
	ax.set_xticklabels(xorder)
	#plt.xticks(r,xorder)
	plt.xticks(rotation=40)
	plt.xlabel(xtitle,size=18)
	plt.ylabel(ytitle,size=18)
	# #plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
	# #ax.legend(axes,barorder)
	plt.tight_layout(pad=7)
	# #ax.autoscale(tight=True)
	plt.savefig(filename)
	#plt.show()




