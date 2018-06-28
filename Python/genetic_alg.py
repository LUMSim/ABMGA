# genetic_alg.py
# authors: Megan Olsen, based on C code by Jessa Laspesa and Ned Taylor
# purpose: all functions necessary for running the genetic algorithm.

import individual
import random
import sys


# purpose: mutate genes in each individual based on mutation rate, uniformally at random
# parameters: the population list (modified by this function), the list of range values, 
#   the mutation rate, the number at the end to not mutate
# return: none
def mutate(pop, ranges, mutate_rate, num_ignore):
    #count = 0 #for testing purposes
    # go through each individual in the population, but not those chosen via elitism (last num_ignore number of individuals)
    for i in range(len(pop)-num_ignore):
        for param in ranges:
            r = random.randrange(0, 100) #need randrange to ensure 100 isn't included in numbers
            # only mutate if the random value is less than the given rate
            if r < mutate_rate:
                # make sure new random value isn't outside the allowed range
                min = param.minimum
                max = param.maximum
                #count+=1
                if param.type == "i":
                    pop[i].genes[param.name] = random.randint(min, max)
                else:
                    the_float = random.uniform(min, max)
                    round_by = len(value.increment.split(".")[1])
                    pop[i].genes[param.name] = round(the_float,round_by) 
    #print(count,"genes were mutated")


# Purpose: Save keep number of individuals with highest fitnesses to new population
# Parameters: the old population list, the new (mutable) population list, and the number of individuals to keep
# Return: none. Assumes ret_pop is mutable, and modifies it.
def elitism(pop, ret_pop, keep):
    # Check that anything can be done
    if keep <= 0 or len(pop)==0:
        return

    sorted_list = []  # each item is fitness followed by the index of that individual in pop
    for index in range(len(pop)):
        sorted_list.append([pop[index].fitness, index])
    sorted_list.sort(reverse=True) #sort to descending order

    #add the first keep number of items to the returned population
    for i in range(keep):
        ret_pop.append(pop[sorted_list[i][1]]) #only care about saving index from original list


# purpose: goes through the current population, selects two random individuals,
#   and crosses over their values at a certain point in the genes list
# parameters: the old population, the ranges list, the number of top inviduals to keep from the prior generation, 
#   number of individuals to compare against in choosing each parent
# return: the new population
def crossover(pop, ranges, keep, tournament_size):
    
    # Choose the parent pairs
    ret_pop = [] # this will hold the new population
    number_of_pairs = int((len(pop) - keep)/2)
    pairs_for_crossover = choose_individuals(pop, "tournament", number_of_pairs, tournament_size)  # holds indices of individuals as a list of pairs

    # ensures choose_individuals can't break this function
    if len(pairs_for_crossover) != int(number_of_pairs):
        print("Error. Incorrect number of pairs for crossover chosen:",len(pairs_for_crossover),number_of_pairs)
        sys.exit(-1)

    # crosses over two individuals at a time from the pair list
    for i in range(len(pairs_for_crossover)):
        # random point to cross over
        cross_point = random.randint(1, len(ranges) - 1)  # forces crosspoint to not be before or after end
        #print("Crossoverpoint:", cross_point)
        # get the random individuals
        individual_1 = pop[pairs_for_crossover[i][0]]
        individual_2 = pop[pairs_for_crossover[i][1]]

        #print(individual_1,individual_2)
        # send over individuals and crossover point. ret_pop will be modified to hold two new individuals
        individual.crossover(individual_1, individual_2, ret_pop, ranges, cross_point)

    #add elitism individuals to the new population
    elitism(pop,ret_pop,keep)

    assert (len(pop) == len(ret_pop)), "new population is not the correct size!"

    return ret_pop


# Purpose: Run a tournament to determine the parent for crossover
# Parameters: pop, the population; size, the number of individuals to have in the tournament
# Return: the index of the chosen individual who should be a parent
def tournament(pop,size):
    best_fitness = -1
    best_index = -1
    # Choose size number of individuals, keeping and returning the top one only
    for i in range(size):
        random_index = random.randrange(len(pop))
        if pop[random_index].fitness > best_fitness:
            best_fitness = pop[random_index].fitness
            best_index = random_index
    return best_index


# Purpose: Select individuals for crossover
# Parameters: pop, the population;
# type, the type of individual choice (random,tournament);
# paircount, the number of pairs to create;
# tournament_size, the number of individuals to run within a tournament
# Return: two indices of individuals
def choose_individuals(pop, type, paircount, tournament_size):
    pairs = []  # a list of lists, each sublist has 2 indices in it to act as parents

    # allows an individual to be paired with itself
    for i in range(paircount):
        if type == "random":  #note: same as tournament of size 1
            index_1 = random.randrange(len(pop))
            index_2 = random.randrange(len(pop))
        elif type == "tournament":
            index_1 = tournament(pop,tournament_size)
            index_2 = tournament(pop,tournament_size)
        else:
            print("Invalid choice for approach to choosing parents. Aborting.")
            sys.exit(-1)
        pairs.append([index_1, index_2])

    return pairs


# Purpose: Compute fitness for all individuals, write them to a file, and return the highest value
# Parameters: the current population as a list (mutable), prefix of names, common part of what the files are named
# Return: the highest fitness value of the current individuals in the population
def compute_all_fitness(new_pop, prefix,common_filename):
    best = -1
    for i in range(len(new_pop)):
        new_pop[i] = individual.compute_fitness(new_pop[i], prefix+str(i)+common_filename)
        if new_pop[i].fitness > best:
            best = new_pop[i].fitness
    return best


# Purpose: Compute fitness for all individuals, write them to a file, and return the highest value
# Parameters: the current population as a list (mutable), prefix of names, common part of what the files are named, 
#   number of instances of each individual, the seeds used, the fitness function to use, the max steps for fitness
#   function to use in its calculation, and other fitness function parameters
# Return: the highest fitness value of the current individuals in the population
def compute_all_fitness_seeded(new_pop, prefix,common_filename, num_seeds, seeds,function,maxsteps,fit_parameters):
    best = -1
    best_genes = {}
    # Calculate fitness for each individual, and determine the best one
    for i in range(len(new_pop)):
        new_pop[i] = individual.compute_fitness_seeds(new_pop[i], prefix+str(i),common_filename,num_seeds,seeds,function,maxsteps,fit_parameters)
        if new_pop[i].fitness > best:
            best = new_pop[i].fitness
            for key in new_pop[i].genes:
                best_genes[key] = new_pop[i].genes[key]
    return best,best_genes

