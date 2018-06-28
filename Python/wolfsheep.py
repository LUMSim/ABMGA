# wolfsheep.py
# Fitness functions for predator prey Wolf Sheep Predation model.
# These functions could be used for other predator prey models.
# Each function assumes specific NetLogo reports were run to create the files that are read from for calculating fitness.
# Author: Megan Olsen


import statistics 

# This fitness function expects that the "sheep" report is run
# This fitness function can be run whether or not the NetLogo model ends when one species dies out
# However, if run without the check for die out, it may run very long and slowly
# fit_parameters should contain a single number that is the desired number of sheep
# FITNESS FUNCTION 0
def simple_fitness_sheep100(filename, fit_parameters):
    DESIRED_SHEEP = int(fit_parameters[0])
    try:
        # Read file to determine number of sheep in the model
        fd = open(filename, "r")
        fd.readline()
        fd.readline()
        fd.readline()
        line = fd.readline()  # we only care about line 4
        fd.close()

        # Percentage of desired number of sheep that was attained
        splitline = line.split()
        num_sheep = int(splitline[2])  # third item when split by whitespace is the count
        if num_sheep > 10000: #models ends if sheep cross 10000 threshold; for calculation purposes, use 10000 in this case
            num_sheep = 10000
        if num_sheep > DESIRED_SHEEP:
            return 1-abs(DESIRED_SHEEP-num_sheep)/(10000-DESIRED_SHEEP)
        else:
            return num_sheep / DESIRED_SHEEP
    except IOError:
        print("Error reading file. No fitness calculated.",filename)
        return 0


# This fitness function is intended to be run with the version of the NetLogo model 
# that ends when there are no more of at least one of the species
# Needs the "ticks" report to be run from netLogo
# FITNESS FUNCTION 1
def simple_fitness_longestTimeStep(filename,maxsteps):
    try:
        # Read file to determine how long it lasted
        fd = open(filename, "r")
        fd.readline()
        line = fd.readline()  # we only care about line 2
        fd.close()

        time = float(line.strip())  # third item when split by whitespace is the count
        return time / maxsteps # percentage of maxsteps attained
    except IOError:
        print("Error reading file. No fitness calculated.",filename)
        return 0


# This fitness function expects that the "sheep" report and the then the "wolf" report is run
# This fitness function can be run wether or not the NetLogo model ends when one species dies out
# However, if run without the check for die out, it may run very long and slowly
# FITNESS FUNCTION 2
def simple_fitness_sheepwolfmax(filename):
    try:
        important_lines = []
        # Read file to find the count of sheep and the count of wolves
        fd = open(filename, "r")
        for line in fd: #...... count(): 170
            split = line.split()
            if len(split)==3 and split[1].strip()=="count():":
                important_lines.append(split[2].strip())
                if len(important_lines) == 2:
                    break
        fd.close()

        # If data is missing, cannot continue
        if len(important_lines) != 2:
            print("Results cannot be analyzed!",filename," Missing reporting data! Return fitness of -1")
            return -1

        # save data for correct calculation
        num_sheep = important_lines[0]
        num_wolves = important_lines[1]

        # fitness is 0 if either dies out, otherwise calculate fitness
        if int(num_sheep) == 0 or int(num_wolves) == 0:
            return 0
        return 1-(1/(int(num_wolves)+int(num_sheep)))

    except IOError:
        print("Error reading file. No fitness calculated.",filename)
        return 0


# This fitness function expects that the "report-allsheep" and then the "report-allwolves" report is run
# This fitness function can be run whether or not the NetLogo model ends when one species dies out
# However, if run without the check for die out, it may run very long and slowly
# Time denotes how many timesteps from the END the fitness function uses in the average
# fit_parameters should contain: number of steps to go back in time, desired num sheep, desired num wolves
# FITNESS FUNCTION 5
def average_agents_over_time(filename, fit_parameters):
    # Ensure parameters are integers
    time = int(fit_parameters[0])
    DESIRED_SHEEP = int(fit_parameters[1])
    DESIRED_WOLF = int(fit_parameters[2])

    try:
        # Read in data
        data = []
        fd = open(filename, "r")
        fd.readline() #skip line stating the model the data came from
        sheepline = fd.readline().strip() #line of sheep list
        wolfline = fd.readline().strip() #line of wolf list
        fd.close()
      
    except IOError:
        print("Error reading file. No fitness calculated.",filename)
        return 0

    #Process data from the file if the reading didn't fail
    sheepline = sheepline.strip("[").strip("]")
    wolfline = wolfline.strip("[").strip("]")
    sheeplist = sheepline.split(",")
    wolflist=wolfline.split(",")
    sheeplist = [float(x) for x in sheeplist]
    wolflist = [float(x) for x in wolflist]

    # if a species died out, fitness is zero
    if wolflist[-1] < 1 or sheeplist[-1] < 1:
        return 0 #not good if one species dies out

    # otherwise, find average over last "time" number of steps
    if len(sheeplist) > time:
        sheeplist = sheeplist[len(sheeplist)-time:]
    if len(wolflist) > time:
        wolflist = wolflist[len(wolflist)-time:]
    s_average = sum(sheeplist)/len(sheeplist)
    w_average = sum(wolflist)/len(wolflist)

    # Model is ended if count > 10000. For calculation purposes, in this case replace the count with 10000.
    if s_average > 10000:
        s_average = 10000
    if w_average > 10000:
        w_average = 10000

    #use averages to determine fitness
    s_fit = 0
    w_fit = 0
    if s_average <= DESIRED_SHEEP:
        s_fit = s_average/DESIRED_SHEEP
    else:
        s_fit = 1-abs(DESIRED_SHEEP-s_average)/(10000-DESIRED_SHEEP)
    if w_average <= DESIRED_WOLF:
        w_fit = w_average/DESIRED_WOLF
    else:
        w_fit = 1-abs(DESIRED_WOLF-w_average)/(10000-DESIRED_WOLF)

    return (s_fit + w_fit)/2 #average of the two averages


# This fitness function expects that the "report-allsheep" and then the "report-allwolves" report is run
# This fitness function can be run wether or not the NetLogo model ends when one species dies out
# However, if run without the check for die out, it may run very long and slowly
# Time denotes how many timesteps from the END the fitness function uses in the average
# fit_parameters should include time
# FITNESS FUNCTION 6
def stdev_agents_over_time(filename, fit_parameters):
    time = int(fit_parameters[0])
    try:
        # Read in data
        data = []
        fd = open(filename, "r")
        fd.readline() #skip line stating the model the data came from
        sheepline = fd.readline().strip() #line of sheep list
        wolfline = fd.readline().strip() #line of wolf list
        fd.close()
      
    except IOError:
        print("Error reading file. No fitness calculated.",filename)
        return 0

    #Process data from the file if the reading didn't fail
    sheepline = sheepline.strip("[").strip("]")
    wolfline = wolfline.strip("[").strip("]")
    sheeplist = sheepline.split(",")
    wolflist=wolfline.split(",")
    sheeplist = [float(x) for x in sheeplist]
    wolflist = [float(x) for x in wolflist]

    if wolflist[-1] < 1 or sheeplist[-1] < 1:
        return 0 #not good if one species dies out

    #otherwise, find standard deviation over last "time" number of steps
    if len(sheeplist) > time:
        sheeplist = sheeplist[len(sheeplist)-time:]
    if len(wolflist) > time:
        wolflist = wolflist[len(wolflist)-time:]
    s_dev = statistics.pstdev(sheeplist)
    w_dev = statistics.pstdev(wolflist)

    #want to minimize the two standard deviations
    fitness = 1-(s_dev/10000+w_dev/10000)/2

    return fitness


# This fitness function expects that the "report-allsheep" and then the "report-allwolves" report is run
# This fitness function can be run wether or not the NetLogo model ends when one species dies out
# However, if run without the check for die out, it may run very long and slowly
# Time denotes how many timesteps from the END the fitness function uses in the average
# FITNESS FUNCTION 7
def stdev_sheep_over_time(filename, fit_parameters):
    time = int(fit_parameters[0])
    try:
        # Read in data
        data = []
        fd = open(filename, "r")
        fd.readline() #skip line stating the model the data came from
        sheepline = fd.readline().strip() #line of sheep list
        wolfline = fd.readline().strip() #line of wolf list
        fd.close()
      
    except IOError:
        print("Error reading file. No fitness calculated.",filename)
        return 0

    #Process data from the file if the reading didn't fail
    sheepline = sheepline.strip("[").strip("]")
    wolfline = wolfline.strip("[").strip("]")
    sheeplist = sheepline.split(",")
    wolflist=wolfline.split(",")
    sheeplist = [float(x) for x in sheeplist]
    wolflist = [float(x) for x in wolflist]

    if wolflist[-1] < 1 or sheeplist[-1] < 1:
        return 0 #not good if one species dies out

    #otherwise, find standard deviation over last "time" number of steps
    if len(sheeplist) > time:
        sheeplist = sheeplist[len(sheeplist)-time:]
    s_dev = statistics.pstdev(sheeplist)

    #want to minimize the standard deviation
    fitness = 1-s_dev/10000

    return fitness









