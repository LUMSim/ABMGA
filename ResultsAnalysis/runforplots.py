import sys, os
#The additional first two lines for matplotlib are required for use on linux only
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PREFIX = sys.argv[1]
INPUT_FILE = sys.argv[2]
VERBOSE=False
MODEL_NAME="WolfSheepPlot.nlogo"
MAX_STEPS=1000
NUM_RUNS=3
NUM_CONCURRENT = 3 #number of parameter sets to run concurrently. All runs of a parameter set alreays run concurrently.


######### Code for reading in parameter lists ##########
# purpose: read in values from input file
# parameter: name of file for parameters
# return: a list of range values
def read_parameters(filename):
    parameters = []

    try:
        filefd = open(filename, "r")

        names = filefd.readline()
        names = names.split()

        # populate ranges array
        for line in filefd:
            split = line.split()
            if len(split) == len(names):
                paramset = {}
                for i in range(len(names)):
                    paramset[names[i].strip()]=int(split[i].strip())
                parameters.append(paramset)
            else:
                print(split,"does not have the correct number of items to match",names)

        filefd.close()

    except Exception:
        print("Exception in file reading function")
        sys.exit(-1)

    return parameters

######### Code for setting up files for running NetLogo with correct parameters #########
# Purpose: Write each file that will be used for running a version of the simulation
# Parameters: population array of individuals
# Return: common file name
def write_input_files(parameters):
    # name each file based on the number of the individual
    filename_common = "inputfile.txt"
    # index = 0 #counting for applying to the filename
    # for every individual, write a file with paramters and other relevant starting information for NetLogo
    # need index of population array to match the filename for later calculation of fitness
    for index in range(len(parameters)):
        filename = PREFIX + str(index) + filename_common
        write_file_NetLogo(parameters[index], filename)
    return filename_common

# Purpose: write a file with all genes of this individual
# Parameters: data: dictionary with full parameter information; filename: name of output file
# Return: none
def write_file_NetLogo(data, filename):
    try:
        outfile = open(filename, "w")
        #set the booleans
        print("set show-energy? false",end="\n",file=outfile)
        if data["grass-regrowth-time"] == -1:
            print("set grass? false",sep=" ",end="\n",file=outfile)
        else:
            print("set grass? true",sep=" ",end="\n",file=outfile)

        for key in data.keys():
            if data[key] != -1:
                print("set", key, data[key], sep=" ", end="\n", file=outfile)
            else:
                print("set",key,"0",sep=" ",end="\n",file=outfile)
                    
        outfile.close()
    except IOError:
        print("Could not write file " + filename)


######### Code for Starting NetLogo Processes ##########
def child_process(instance,filename):
    # args has all arguments for executing the netlogo model run file, netlogo-mac-app.jar OR NetLogo.jar depending on OS
    args = ["java","-Xms3072m","-classpath", ".:../lib:../lib/netlogo-mac-app.jar:../API","RunNetLogoModel"]
    # model name, input file name, number of steps, report name
    args.append(MODEL_NAME)#"../WolfSheep/WolfSheep.nlogo")
    args.append(filename) #input file, which is the same for all seeds
    args.append(str(MAX_STEPS)) #everything sent to execvp must be a string
    args.append("outputplot "+str(instance)) #saves result of plot to a csv file
    #new_stdout = os.open(PREFIX+str(index)+"S"+str(seed)+"modelresults.txt", os.O_WRONLY|os.O_CREAT|os.O_TRUNC)
    #os.dup2(new_stdout, 1)
    os.execvp(args[0], args)

# Purpose: Run multiple versions of the same parameters
# Parameters: data: dictionary of parameters to send to child; filename: output filename common aspect
def run_children(data,filename):
    if VERBOSE:
        print("Parameters ",data,"beginning")
    pids = []
    # create all children with different random number seeds and have them run their process
    for i in range(NUM_RUNS):
        pids.append(os.fork())
        if pids[i] < 0:
            print("fork failed for RUN ", i)
            sys.exit(-1)
        # child process
        elif pids[i] == 0:
            if VERBOSE:
                print("Child ", i, " is now starting, ",filename)
            child_process(i, filename)
        else:
            if VERBOSE:
                print("continuing in main process...")
    return pids


#Purpose: Run all child processes, running NUM_RUNS variations for each parameter set
#Parameters: filename: common aspect of output file names
def create_wait_children(filename, parameters):
    # create all children and have them run their process
    for i in range(0,len(parameters),NUM_CONCURRENT):
        pids=[]
        for k in range(NUM_CONCURRENT):
            if i+k < len(parameters):
                ifilename = PREFIX+str(i+k)+ filename
                pids.append(run_children(parameters[i+k], ifilename))
        # once all children have been created, wait for all to finish
        for m in range(len(pids)):
            for j in range(NUM_RUNS):
                if pids[m][j] > 0:  # if process was started, wait for it
                    if VERBOSE:
                        print("Waiting for pid ",pids[m][j])
                    status = os.waitpid(pids[m][j], 0)
            if VERBOSE:
                print("All children for parameter set",i+m," have now finished")
        if VERBOSE:
            print("All",NUM_RUNS,"instances for parameter set ",i,"have completed")


######### MAIN ##############
# Create filename for reading and for saving plot
# Filename is the common part of all runs from this parameter set. Will need run number appended later.
def create_filename(parameterset):
    if parameterset["grass-regrowth-time"]==-1:
        filename="false-"
    else:
        filename="true-"
    filename=filename+str(parameterset["initial-number-sheep"])+"-"+str(parameterset["initial-number-wolves"])+"-"+str(parameterset["sheep-reproduce"])
    filename=filename+"-"+str(parameterset["wolf-reproduce"])+"-"+str(parameterset["sheep-gain-from-food"])+"-"+str(parameterset["wolf-gain-from-food"])
    if parameterset["grass-regrowth-time"]==-1:
        filename=filename+"-"+"0"
    else:
        filename=filename+"-"+str(parameterset["grass-regrowth-time"])
    return filename

# Read in file for plotting
def read_plot_file(filename): 
    if filename.split("-")[0]=="true":
        isgrass = True
        data=[[],[],[]]
    else:
        data = [[],[]] 
        isgrass = False   
    filename = filename+".csv"

    try:
        fd = open(filename,"r")
        
        for i in range(19): # read the unnecessary starting lines of the file
            fd.readline()

        #read in the columns of data
        for line in fd:
            split = line.split(",")
            if len(split) >= 6:
                data[0].append(int(split[1].strip('\'').strip("\"")))
                data[1].append(int(split[5].strip('\'').strip("\"")))
                if isgrass:
                    data[2].append(float(split[9].strip('\'').strip("\"")))
        fd.close()
    except:
        print("Error reading plotting file")
        return -1
    return data

# Plot the change over time
# data: a row of sheep, a row of wolves, and a row of grass if relevant
# filename: the name to use for the plot file. Must add ".pdf"
def plot_results(data,filename):
    ymax = max(max(data[0]),max(data[1]))
    ymin=0
    xaxis = list(range(len(data[0])))
    plt.xlabel('Time Steps')
    plt.ylabel('Population')
    plt.ylim(ymin,ymax)
    
    matplotlib.rc('font', size=14)
    if len(data) == 2:
        plt.plot(xaxis,data[0],'k-',xaxis,data[1],'c--')
        plt.legend(["sheep","wolves"])
    else:
        plt.plot(xaxis,data[0],'k-',xaxis,data[1],'c--',xaxis,data[2],'g:')
        plt.legend(["sheep","wolves","grass/4"])
    plt.savefig(filename+"-plot.pdf")
    plt.clf()

def output_minmax(data,filename):
    print(filename,end=" ")
    
    if len(data[0]) > 1000:
        sheep = data[0][-1000:]
        wolf = data[1][-1000:]
        if len(data) == 3:
            grass = data[2][-1000:] 
    else:
        sheep = data[0]
        wolf = data[1]
        if len(data) == 3:
            grass = data[2]

    #output min/max of each
    print(min(sheep),max(sheep),sep=" ",end=" ")
    print(min(wolf),max(wolf),sep=" ",end=" ")
    if len(data) == 3:
        print(min(grass),max(grass),sep=" ",end=" ")

    #output result if it's one of the undesired scenarios
    if min(sheep) == 0:
        print("sdie/",end="")
    elif max(sheep) > 10000:
        print("s10k/",end="")
    if min(wolf) == 0:
        print("wdie/",end="")
    elif max(wolf) > 10000:
        print("w10k/",end="")

    print("") #line break

def main():
    # Read in file of parameters to create parameters list of dictionaries
    parameters = read_parameters(INPUT_FILE)
    # For each list of parameters, create an input file
    common = write_input_files(parameters)
    # For each list of parameters, run all such that they export a CSV of their plot, named for their parameters
    create_wait_children(common, parameters)
    # Create a plot from the CSV file
    for i in range(len(parameters)):
        plotfile = create_filename(parameters[i])
        for r in range(NUM_RUNS):
            iplotfile=plotfile+"-"+str(r)
            data = read_plot_file(iplotfile)
            if data != -1:
                plot_results(data,iplotfile)
                # Output to standard out the range of each agent type for a particular set of parameters
                output_minmax(data,iplotfile)

main()


