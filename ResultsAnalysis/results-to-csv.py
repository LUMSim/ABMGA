# This program is created for analysis of the GA results of the WolfSheep NetLogo Model
# This program assumes a command line argument that is the name of a file of a specific format:
#   Last line of a list of timestamp, best fitness, average fitness
#   Best overall fitness
#   "Best Genes"
#   A list of genes and their best values, in no particular order (6 or 7, depending on setup)
# The name of the file gives the parameters used to create the results
# This program will read in this info, and info from associated files (found by modifying given filename), and
# outputting those results by appending to a results .csv file that can later be analyzed for info on all results

import sys


# Process the file with final statistics in it, and return the results (generations, fitness, parameters)
def read_endfile(filename):
    #Parameters to set from file
    results = {}
    results["parameters"]={}
    results["fitness"] = -1 #not every file will have fitness in it

    try:
        fd = open(filename,"r")

        #Get number of generations
        line = fd.readline()
        splitline = line.split() #split on whitespace: "Total", "generations:", [answer]
        results["generations"] = int(splitline[2])

        #In case there are table lines here, ignore them
        line = fd.readline()
        splitline = line.split()
        while splitline[0].isdigit():
            line = fd.readline()
            splitline = line.split()

        #Get fitness
        if len(splitline) == 3 and splitline[1].lower() == "fitness:":
            results["fitness"] = float(splitline[2]) #"Best", "fitness:", [answer]
            fd.readline() #skip the "Best Genes:" line

        #Get parameters
        line = fd.readline()
        while line:
            splitline = line.split()
            results["parameters"][splitline[0].strip()]=splitline[1]
            line = fd.readline()

        fd.close()

    except FileNotFoundError:
        print("File",filename," could not be opened for reading. Aborting.")
        sys.exit(-1)

    return results


# takes a time as created by linux time function and turns into seconds and minutes
# returns a list with the time in seconds and the time in minutes
def process_time(time):
    minutes = time.split("m")[0]
    seconds = time.split("m")[1][:-1]
    in_seconds = int(minutes) * 60 + float(seconds)
    in_minutes = in_seconds/60

    return [in_seconds,in_minutes]


def read_timefile(filename):
    times = {}
    try:
        fd = open(filename,"r")

        line = fd.readline() #skip empty line at start
        line = fd.readline() #get real time
        times["real"]=process_time(line.split()[1])

        line = fd.readline() #get user time
        times["user"]=process_time(line.split()[1])

        line = fd.readline() #get system time
        times["sys"]=process_time(line.split()[1])

        fd.close()

    except FileNotFoundError:
        print("File",filename," could not be opened for reading. Aborting.")
        sys.exit(-1)

    return times


# filename: the file name to be split apart, should be the common part only
# results: a dictionary storing results of analysis
def process_filename(filename,results):
    pieces = filename[:-1].split("-")
    #name="GAS100-${individuals}-${mutation}-${target}-${maxgen}-${replications}-${elitism}-${tournament}"
    results["function"]=pieces[0]
    results["individuals"]=pieces[1]
    results["mutation"]=pieces[2]
    results["target"]=pieces[3]
    results["maxgen"]=pieces[4]
    results["replications"]=pieces[5]
    index = 6
    #if len(pieces) >= 8: #no longer needed, as this was for results form before elitism and tournaments were used
    results["elitism"]=pieces[6]
    results["tournament"]=pieces[7]
    #    index = 8
    #else:
    #    results["elitism"] = 0
    #    results["tournament"] = 1
    results["maxsteps"]=pieces[8]
    results["fitfun"]=pieces[9]
    if len(pieces)>10:
        results["grass"]=1
    else:
        results["grass"]=0


# Write results to the end of the results_analysis file
def write_csv(results):

    try:
        fd = open(results["function"]+"_results_analysis.csv","a")

        print(results["individuals"], end=",",file=fd)
        print(len(results["parameters"]), end=",",file=fd)
        print(results["mutation"], end=",",file=fd)
        print(results["target"], end=",",file=fd)
        print(results["maxgen"], end=",",file=fd)
        print(results["replications"], end=",",file=fd)
        print(results["elitism"],end=",",file=fd)
        print(results["tournament"],end=",",file=fd)
        print(results["maxsteps"],end=",",file=fd) #was previously 500
        print(results["generations"], end=",",file=fd)
        print(results["fitness"], end=",",file=fd)
        print(results["real"][0], end=",",file=fd)
        print(results["user"][0], end=",",file=fd)
        print(results["sys"][0], end=",",file=fd)
        print(results["real"][1], end=",",file=fd)
        print(results["user"][1], end=",",file=fd)
        print(results["sys"][1], end=",",file=fd)
        print(results["parameters"]["initial-number-sheep"], end=",",file=fd)
        print(results["parameters"]["initial-number-wolves"], end=",",file=fd)
        print(results["parameters"]["sheep-reproduce"], end=",",file=fd)
        print(results["parameters"]["wolf-reproduce"], end=",",file=fd)
        print(results["parameters"]["sheep-gain-from-food"], end=",",file=fd)
        print(results["parameters"]["wolf-gain-from-food"], end=",", file=fd)
        if "grass-regrowth-time" in results["parameters"].keys():
            print(results["parameters"]["grass-regrowth-time"],file=fd)
        else:
            print(-1, file=fd)
        fd.close()
    except:
        print("Error writing results to the file")


def main():
    if len(sys.argv) != 2:
        print("This script requires a single command line argument with the name of a file.")
        sys.exit(-1)

    #Process final statistics
    filename = sys.argv[1]
    results = read_endfile(filename) #results is a dictionary

    #Process timing
    filecommon = filename[9:-12]
    timefile = filecommon+"error1.log"
    times = read_timefile(timefile)
    results["real"]=times["real"]
    results["user"]=times["user"]
    results["sys"]=times["sys"]

    #Process GA parameters by filename
    process_filename(filecommon,results)

    #Append results to the end of the results file
    write_csv(results)

main()