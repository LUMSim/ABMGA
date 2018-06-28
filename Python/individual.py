#
# individual.py
# authors: Megan Olsen, based on C code by Jessa Laspesa and Ned Taylor
# purpose: this file holds all the necessary data for an individual
# and also chooses random parameter values for testing
#

from collections import namedtuple
import random
import sys
import wolfsheep #fitness functions for wolfsheep model

VERBOSE = False
unvaried_values = {} #dictionary of parameters used in every run of the model

# Structures for organizing data together. NamedTuples are immutable.
Ind = namedtuple("Ind", "size genes fitness")  # number of genes, dictionary of genes, fitness value
# Population = namedtuple("Population","size population ranges") #number of individuals, individuals list, ranges list
ParamRange = namedtuple("ParamRange", "name minimum maximum increment type")  # name, minimum value, maximum value, increment, type (i or f)


# Purpose: write a file with all genes of this individual, so that model can be started with these values
# Parameters: Ind type namedtuple with full information, name of output file
# Return: none
def write_file_NetLogo(ind, filename):
    try:
        outfile = open(filename, "w")
        for key in ind.genes.keys():
            print("set", key, ind.genes[key], sep=" ", end="\n", file=outfile)
        if len(unvaried_values.keys()) > 0: #if there are unvaried values for the model
            for key in unvaried_values.keys():
                print("set",key,unvaried_values[key],sep=" ",end="\n",file=outfile)
        outfile.close()
    except IOError:
        print("Could not write file " + filename)


# purpose: read in ranges from input file
# parameter: name of file for ranges, name of file for unvaried values
# return: a list of range values
def read_ranges(ranges_filename, unvaried_filename=""):
    ranges = []

    try:
        filefd = open(ranges_filename, "r")

        # populate ranges array
        for line in filefd:
            split = line.split(",")
            if len(split) == 4: #range assumed to be integer
                ranges.append(ParamRange(split[0], int(split[1]), int(split[2]), split[3].strip(),"i"))
            elif len(split) == 5: #range includes type
                for index in range(1,3):
                    if split[index].isdigit():
                        split[index] = int(split[index])
                    else:
                        split[index] = float(split[index])

                ranges.append(ParamRange(split[0], split[1], split[2], split[3].strip(),split[4].strip()))
            else:
                if VERBOSE:
                    print("Skipping line in file with incorrect number of items")

        filefd.close()

        # Read in values that are the same for every instance of the model
        if unvaried_filename != "":
            filefd2 = open(unvaried_filename,"r")
            for line in filefd2:
                split = line.split()
                if len(split) == 2:
                    unvaried_values[split[0]] = split[1]
                else:
                    if VERBOSE:
                        print("Skipping line in unvaried values file with incorrect number of items")
            filefd2.close()

    except Exception:
        print("Exception in range reading function")
        sys.exit(-1)

    return ranges


# purpose: create a new population, load data from the input file 
#   into each individual in the population, populate the ranges array given
# parameters: num_individuals, the number of individuals; ranges, the range values for genes
# return: a new Population
def create_initial_population(num_individuals, ranges):
    new_pop = []

    # create individuals with values based on ranges
    for i in range(num_individuals):
        # add individual to population
        new_pop.append(Ind(size=len(ranges), genes={}, fitness=0))

        for value in ranges:
            # add values for each of its genes
            if value.type == "i":
                new_pop[i].genes[value.name] = random.randint(value.minimum, value.maximum)
            else:
                the_float = random.uniform(value.minimum, value.maximum)
                round_by = len(value.increment.split(".")[1])
                new_pop[i].genes[value.name] = round(the_float,round_by) 
    return new_pop


# Purpose: compute fitness when multiple seeds were used with same parameter set. Update individual's fitness and return.
# Parameters: individual whose fitness will be updated, file prefix, file suffix, number of models run,
#   fitness function to run, the max steps for calculating fitness function (ignored if not applicable),
#   parameters for hte fitness function
# Return: an individual with updated fitness calculation 
def compute_fitness_seeds(ind,filename1,filename2,num_seeds,seeds,function,maxsteps,fit_parameters):
    fitness=0
    
    for i in range(num_seeds):
        name = filename1+"S"+str(seeds[i])+filename2
        #print(filename1,filename2,seeds[i])
        if function == 0:
            fitness+=wolfsheep.simple_fitness_sheep100(name,fit_parameters)
        elif function == 1:
            fitness+=wolfsheep.simple_fitness_longestTimeStep(name,maxsteps)
        elif function == 2:
            fitness+=wolfsheep.simple_fitness_sheepwolfmax(name)
        elif function == 5:
            fitness+=wolfsheep.average_agents_over_time(name,fit_parameters)
        elif function == 6:
            fitness+=wolfsheep.stdev_agents_over_time(name,fit_parameters)
        elif function == 7:
            fitness+=wolfsheep.stdev_sheep_over_time(name,fit_parameters)
        else:
            print("ERROR. Fitness function ",function,"not defined")
    #print(fitness,num_seeds,fitness/num_seeds)
    fitness = fitness/num_seeds
    ind = Ind(size=ind.size,genes=ind.genes,fitness = fitness)
    return ind


# purpose: compute the fitness score for a certain individual, when only one instance of parameters are run
# parameters: the individual, the name of the file to read in results from, the fitness function to use
# return: the original individual with updated fitness value
def compute_fitness_single(ind, filename, function):
    ind = Ind(size=ind.size,genes=ind.genes,fitness = wolfsheep.simple_fitness_sheep100(filename))
    if function == 0:
        ind = Ind(size=ind.size,genes=ind.genes,fitness = wolfsheep.simple_fitness_sheep100(name,fit_parameters))
    elif function == 1:
        ind = Ind(size=ind.size,genes=ind.genes,fitness = wolfsheep.simple_fitness_longestTimeStep(name,maxsteps))
    elif function == 2:
        ind = Ind(size=ind.size,genes=ind.genes,fitness = wolfsheep.simple_fitness_sheepwolfmax(name))
    elif function == 5:
        ind = Ind(size=ind.size,genes=ind.genes,fitness = wolfsheep.average_agents_over_time(name,fit_parameters))
    elif function == 6:
        ind = Ind(size=ind.size,genes=ind.genes,fitness = wolfsheep.stdev_agents_over_time(name,fit_parameters))
    elif function == 7:
        ind = Ind(size=ind.size,genes=ind.genes,fitness = wolfsheep.stdev_sheep_over_time(name,fit_parameters))
    else:
        print("ERROR. Fitness function ",function,"not defined")
    return ind

# purpose: cross over the two individuals given, adding the new individuals to the provided list
# parameters: two old individuals, the new population list, the ranges list, the cross over point
# return: none. New population is updated in place.
def crossover(individual_1, individual_2, ret_pop, ranges, cross_point):
    ret_pop_index = len(ret_pop)  # first index of new items is current length of list

    # create new individuals with crossed values at the crossover point
    ret_pop.append(Ind(size=len(ranges), genes={}, fitness=0))
    ret_pop.append(Ind(size=len(ranges), genes={}, fitness=0))

    for j in range(cross_point):  # for everything before cross point, don't swap
        ret_pop[ret_pop_index].genes[ranges[j].name] = individual_1.genes[ranges[j].name]
        ret_pop[ret_pop_index + 1].genes[ranges[j].name] = individual_2.genes[ranges[j].name]
    for j in range(cross_point, len(ranges)):  # for everything after and including cross point, swap
        ret_pop[ret_pop_index].genes[ranges[j].name] = individual_2.genes[ranges[j].name]
        ret_pop[ret_pop_index + 1].genes[ranges[j].name] = individual_1.genes[ranges[j].name]


# purpose: print an individual to standard out. Helper function to print_population, but can be used for debugging.
# parameters: the individual to be printed
# return: none
def print_individual(individual):
    print("Genes: ",end="")
    for key in individual.genes.keys():
        print(individual.genes[key], end=" ")
    print("\nFitness: ",individual.fitness)


# purpose: print a population to standard out, giving all genes and fitness
# input: the population to be printed
# return: none
def print_population(pop):
    print("-------------Population--------------")
    if len(pop) > 0:
        print("Gene Order:",pop[0].genes.keys())
        for index in range(len(pop)):
            print("Individual ", index)
            print_individual(pop[index])
    print("-------------------------------------")


# Purpose: calculate the average fitness of a population
# Parameter: population
# Return: average fitness
def average_fitness(pop):
    sum=0
    for ind in pop:
        sum += ind.fitness
    return sum/len(pop)
