# Main file for the Python implementation of the GA for ABM program
# Author: Megan Olsen

import os
import sys
#The first two lines for matplotlib are required for use on linux only
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Our imported files
import genetic_alg
import individual

VERBOSE = False  # for verbose output to be on or off


# Purpose: Write each file that will be used for running a version of the simulation
# Parameters: population array of individuals
# Return: common file name
def write_input_files(population):
    # name each file based on the number of the individual
    filename_common = "inputfile.txt"
    # for every individual, write a file with parameters and other relevant starting information for NetLogo
    # need index of population array to match the filename for later calculation of fitness
    for index in range(len(population)):
        filename = PREFIX + str(index) + filename_common
        individual.write_file_NetLogo(population[index], filename)
    return filename_common


# Purpose: Check that the arguments are valid
# Return: -1 on failure, 0 otherwise
def check_arguments():
    if len(sys.argv) < 15: #last one is optional!
        print("USAGE: ./run <number of individuals> <number of parameters> <mutation rate 0-100> <target fitness 0.5-1>", \
            "<max number of generations> <number of replications 1-12> <elitism count 0+> <tournament size 1+> <input text file> ", \
            "<max model steps 1+> <fitness function> <model name> <output file prefix> <input unvaried values> <optional fitness function data>")
        return -1
    #if len(sys.argv) > 16:
    #    print("Only the first 15 parameters will be used. The excess will be ignored.")

    returnvalue = 0
    # Error checking on the input values
    if not sys.argv[1].isdigit() or int(sys.argv[1]) < 1 or int(sys.argv[1]) > 100:
        print("Please ensure that the number of individuals is a positive number between 1 and 100")
        returnvalue = -1

    if not sys.argv[2].isdigit() or int(sys.argv[2]) < 0:
        print("Please ensure the number of parameters for each individual (lines in input text file) is >= 0")
        returnvalue = -1

    if not sys.argv[3].isdigit() or int(sys.argv[3]) < 0 or int(sys.argv[3]) > 100:
        print("Please ensure that the mutation rate is between 0 and 100")
        returnvalue = -1

    if float(sys.argv[4]) < 0.5 or float(sys.argv[4]) > 1:
        print("Please ensure that the target fitness rate is between 0.5 and 1")
        returnvalue = -1

    if not sys.argv[5].isdigit() or int(sys.argv[5]) < 0 or int(sys.argv[5]) > 2000:
        print("Please ensure that the max number of generations is between 0 and 2000")
        returnvalue = -1

    if not sys.argv[6].isdigit() or int(sys.argv[6]) < 1 or int(sys.argv[6]) > 12:
        print("Please ensure that the number of replications is between 1 and 12")
        returnvalue = -1

    if not sys.argv[7].isdigit() or int(sys.argv[7]) < 0 or int(sys.argv[7]) > int(sys.argv[1])-2 or int(sys.argv[7])%2!=0:
        print("Please ensure that the number of individuals to keep via elitism is even and between 0 and number of individuals minus 2")
        returnvalue = -1

    if not sys.argv[8].isdigit() or int(sys.argv[8]) < 1:
        print("Please ensure that the tournament size is >=1. Note that a size of 1 is equivalent to randomly choosing parents.")
        returnvalue = -1

    if not sys.argv[10].isdigit() or int(sys.argv[10]) < 1:
        print("Please ensure that the max number of steps the model can run is >=1.")
        returnvalue = -1

    if not sys.argv[11].isdigit() or int(sys.argv[11]) < 0 or int(sys.argv[11])>7:
        print("Please ensure that the fitness function is a valid option:")
        print("0: sheep are at exactly some value (parameters: desired sheep)")
        print("1: the number of time steps the simulation ran for")
        print("2: Maximize the number of sheep and wolves, with 0 of either species counting as fitness 0")
        print("5: average number of sheep over time (parameters: time)")
        print("6: minimizing standard deviation of number of sheep and wolves (parameters: time, desired sheep, desired wolves)")
        print("7: minimizing standard deviation of number of sheep (parameters: time)")
        returnvalue = -1
    
    return returnvalue


########### RUNNING MULTIPLE MODELS FOR EACH PARAMETER SET, WAIT BETWEEN SETS ############
def child_process_different_seeds(index, filename,seed):
    # args has all arguments for executing the netlogo model run file, netlogo-mac-app.jar OR NetLogo.jar depending on OS
    args = ["java","-Xms3072m","-classpath", ".:../lib:../lib/netlogo-mac-app.jar:../API","RunNetLogoModelSeed"]
    # model name, input file name, number of steps, report name
    args.append(MODEL_NAME)#"../WolfSheep/WolfSheep.nlogo")
    args.append("../Python/"+PREFIX+str(index)+ filename) #input file, which is the same for all seeds
    args.append(str(MAX_STEPS)) #everything sent to execvp must be a string
    args.append(str(seed))
    for rep in REPORT:
        args.append(rep) #sheep or ticks
    new_stdout = os.open(PREFIX+str(index)+"S"+str(seed)+"modelresults.txt", os.O_WRONLY|os.O_CREAT|os.O_TRUNC)
    os.dup2(new_stdout, 1)

    os.execvp(args[0], args)


# Purpose: Run multiple versions of the same parameters but different random number seeds
# Parameters: id: which set of parameters to send to child; filename: output filename common aspect
def run_children_different_seeds(id,filename):
    pids = []
    # create all children with different random number seeds and have them run their process
    for i in range(NUM_SEEDS):
        pids.append(os.fork())
        if pids[i] < 0:
            print("fork failed for SEED ", i)
            sys.exit(-1)
        # child process
        elif pids[i] == 0:
            if VERBOSE:
                print("Child seed ", SEEDS[i], " is now starting")
            child_process_different_seeds(id, filename, SEEDS[i])
        else:
            if VERBOSE:
                print("continuing in main process...")

    # once all children have been created, wait for all to finish
    for i in range(NUM_SEEDS):
        if pids[i] > 0:  # if process was started, wait for it
            if VERBOSE:
                print("Waiting for pid ",pids[i])
            status = os.waitpid(pids[i], 0)
    if VERBOSE:
        print("All children have now finished")


#Purpose: Run all child processes, running NUM_SEEDS variations for each parameter set
#Parameters: filename: common aspect of output file names
def create_wait_children_different_seeds(filename):
    # create all children and have them run their process
    for i in range(NUM_INDIVIDUALS):
        run_children_different_seeds(i, filename)
        if VERBOSE:
            print("All",NUM_SEEDS,"instances for parameter set ",i,"have completed")
#####################################


################# Ploting and Output#############
# Plot the change over time
def plot_results(best,average):
    plt.plot(list(range(len(best))),best,'kx-',list(range(len(average))),average,'co--')
    plt.ylim(0, 1)
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.savefig(PREFIX+"plot.pdf")


def output_results(best,average,genes):
    try:
        fd = open(PREFIX+"end.txt","w")
        print("Total generations:",len(best),file=fd)
        print("Fitness over time:",file=fd)
        print("Gen\tBest\tAverage",file=fd)
        for i in range(len(best)):
            print(i+1,"\t",best[i],"\t",average[i],file=fd)
        print("Best Fitness:",max(best),file=fd)
        print("Best Genes:",file=fd)
        for key in genes.keys():
            print(key,"\t",genes[key],file=fd)
        fd.close()
    except:
        print("Error writing final results to output file")


def output_setup():
    print("GA Setup:")
    print("Number of individuals:",NUM_INDIVIDUALS)
    print("Number of replications:",NUM_SEEDS)
    print("Max generations:",NUM_GENERATIONS)
    print("Crossover: ",(NUM_INDIVIDUALS-NUM_KEEP)/NUM_INDIVIDUALS*100,"%",sep="")
    print("Pairs chosen: tournament size",TOURNAMENT_SIZE)
    print("Self pairing: allowed")
    print("Mutation: all possible values")
    print("Multiple runs combined via: mean")
    print("Ranges file: ",INPUT_FILE)
    print("Unvaried values file:", UNVARIED_INPUT)
    print("Maximum Steps:",MAX_STEPS)
    print("Fitness function:",FIT_FUNCTION)
    print("Report:",REPORT)
    print("Model:",MODEL_NAME)
    print("----------------------------------")
##################################

# Main function for running the program
def main_seeds():
    #Output basic setup
    output_setup()

    # read in starting values and create first population
    ranges = individual.read_ranges(INPUT_FILE,UNVARIED_INPUT)
    pop = individual.create_initial_population(NUM_INDIVIDUALS, ranges)
    run_count = 1
    average_fitnesses = []
    best_fitnesses = []
    best_fitness_overall = 0
    best_genes = {}

    # run for a specific number of times or until target fitness is achieved
    while run_count <= NUM_GENERATIONS and best_fitness_overall < TARGET_FITNESS:
        print("run number ", run_count)
        
        write_input_files(pop)  # write files to be used for starting models
        create_wait_children_different_seeds("inputfile.txt")  # create children and wait for them to finish
        best_fitness_round,best_genes_round = genetic_alg.compute_all_fitness_seeded(pop,PREFIX,"modelresults.txt",NUM_SEEDS,SEEDS,FIT_FUNCTION,MAX_STEPS,FIT_PARAM)  # calculate fitness of each individual
        best_fitnesses.append(best_fitness_round)
        average_fitnesses.append(individual.average_fitness(pop))

        #set overall best fitness if it is improved
        if best_fitness_round > best_fitness_overall:
            best_fitness_overall = best_fitness_round
            best_genes = best_genes_round

        #After running but before crossover, what are the genes and their fitness?
        individual.print_population(pop)
        print("Best fitness this generation:", best_fitness_round)
        print("Average fitness this generation:",average_fitnesses[run_count-1])
        print("Best fitness thus far:",best_fitness_overall)

        # cross over the individuals if we do not have a best fit and will run again
        if best_fitness_round < TARGET_FITNESS and run_count < NUM_GENERATIONS:
            pop = genetic_alg.crossover(pop,ranges,NUM_KEEP, TOURNAMENT_SIZE)
            genetic_alg.mutate(pop, ranges, MUTATION_RATE, NUM_KEEP)

        run_count += 1
        
    # done with a single generation

    #end of program output
    plot_results(best_fitnesses,average_fitnesses)
    output_results(best_fitnesses,average_fitnesses,best_genes)
    

#############################################################

#### Before running main, check that command line arguments are OK and store in global "constants"
if check_arguments() == -1:
    print("Program Ending. Parameters incorrect.")
    sys.exit(-1)

# Make it easier to interact with arguments in the rest of the code
NUM_INDIVIDUALS = int(sys.argv[1])
PARAMETER_COUNT = int(sys.argv[2])
MUTATION_RATE = int(sys.argv[3])
TARGET_FITNESS = float(sys.argv[4])
NUM_GENERATIONS = int(sys.argv[5])
NUM_SEEDS = int(sys.argv[6])
NUM_KEEP = int(sys.argv[7])
TOURNAMENT_SIZE = int(sys.argv[8])
INPUT_FILE = sys.argv[9]
MAX_STEPS = int(sys.argv[10])

#Values that are needed for a fitness function, varies by function
FIT_PARAM = []
if len(sys.argv) > 15:
    number = len(sys.argv)-15
    for i in range(number):
        FIT_PARAM.append(sys.argv[15+i])

FIT_FUNCTION = int(sys.argv[11])
if FIT_FUNCTION == 0:
    REPORT=["sheep"]
    if len(FIT_PARAM)<1:
        print("ERROR: fitness function requires a fitness parameter (desired sheep)")
        sys.exit(-1)
elif FIT_FUNCTION == 1:
    REPORT=["ticks"]
elif FIT_FUNCTION == 2:
    REPORT=["sheep","wolves"]
elif FIT_FUNCTION == 3:
    REPORT=["EatingAverage"]
elif FIT_FUNCTION == 4:
    REPORT=["isFullAverage"]
elif FIT_FUNCTION == 5:
    REPORT=["report-allsheep","report-allwolves"]
    if len(FIT_PARAM)<3:
        print("ERROR: fitness function requires 3 fitness parameters (time, desired sheep, desired wolves)")
        sys.exit(-1)
elif FIT_FUNCTION == 5 or FIT_FUNCTION == 6 or FIT_FUNCTION == 7:
    REPORT=["report-allsheep","report-allwolves"]
    if len(FIT_PARAM)<1:
        print("ERROR: fitness function requires a fitness parameter (time)")
        sys.exit(-1)

MODEL_NAME = sys.argv[12]
PREFIX = sys.argv[13]
#if len(sys.argv) >= 15: #everything after this number is ignored, as this should be the last parameter
UNVARIED_INPUT = sys.argv[14]
#else:
#    UNVARIED_INPUT = ""


SEEDS = [500,1024,3,89043,25323,44,567,99933,6789,10919,87878,2522]

main_seeds()

#######################TESTS########################################
# these need to be updated with some recent code changes
def test_file_write():
    print("-------\nTesting writing to file of 3 population members")
    population = []
    population.append(individual.Ind(size=5, genes={"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}, fitness=0))
    population.append(individual.Ind(size=5, genes={"a": 6, "b": 7, "c": 8, "d": 9, "e": 10}, fitness=0))
    population.append(individual.Ind(size=5, genes={"a": 1, "b": 3, "c": 5, "d": 7, "e": 9}, fitness=0))
    filename = write_input_files(population)
    print("Check for 3 files that start with the name", filename)
    print("They should have set statements that match the following:")
    print(population[0].genes)
    print(population[1].genes)
    print(population[2].genes)


def test_NetLogo_Run():
    ind = individual.Ind(size=5, genes={"initial-number-sheep":100,"initial-number-wolves":25,"sheep-gain-from-food":5,
                                        "sheep-reproduce":10,"wolf-reproduce":20}, fitness=0)
    individual.write_file_NetLogo(ind, "0test.txt")
    child_process(0,"test.txt")


def test_fitness_calculation():
    ind = individual.Ind(size=5,
                         genes={"initial-number-sheep": 100, "initial-number-wolves": 25, "sheep-gain-from-food": 5,
                                "sheep-reproduce": 10, "wolf-reproduce": 20}, fitness=0)
    individual.write_file_NetLogo(ind, "0test.txt")
    #Fork and run the process
    pid=os.fork()
    if pid < 0:
        print("fork failed for process ", i)
        sys.exit(-1)
    # child process
    elif pid == 0:
        print("Child process is now starting")
        child_process(0, "test.txt")

    else:  # if process was started, wait for it
        status = os.waitpid(pid, 0)
        print("status: ",status)

    #calculate fitness
    ind = individual.compute_fitness(ind, "modelresults.txt")
    print("Calculated fitness is ",ind.fitness)


def test_create_wait_children():
    #TO RUN, MUST SEND 2 IN FOR THE NUM_INDIVIDUALS PARAMETER. NO OTHER PARAMETER MATTERS.
    ind = individual.Ind(size=5,
                         genes={"initial-number-sheep": 100, "initial-number-wolves": 25, "sheep-gain-from-food": 5,
                                "sheep-reproduce": 10, "wolf-reproduce": 20}, fitness=0)
    individual.write_file_NetLogo(ind, "0test.txt")
    ind = individual.Ind(size=5,
                         genes={"initial-number-sheep": 50, "initial-number-wolves": 5, "sheep-gain-from-food": 5,
                                "sheep-reproduce": 10, "wolf-reproduce": 20}, fitness=0)
    individual.write_file_NetLogo(ind, "1test.txt")

    create_wait_children("test.txt")
    print("Experiments complete.", NUM_INDIVIDUALS, "modelresults files should exist.")


#test_file_write()
#test_NetLogo_Run()
#test_fitness_calculation()
#test_create_wait_children()




