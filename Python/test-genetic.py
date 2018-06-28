# Testing functions for genetic_alg.py
# NOt sufficient to fully test.

import genetic_alg
import individual
import copy


def test_mutation_none():
    print("-------\nTesting mutation rate of zero")
    test_range = [] #"name minimum maximum increment"
    test_range.append(individual.ParamRange("a",0,100,10))
    test_range.append(individual.ParamRange("b", 5, 11, 3))
    test_range.append(individual.ParamRange("c", 1, 7, 1))
    test_range.append(individual.ParamRange("d", 50, 51, 1))

    isError = False
    population = individual.create_initial_population(10,test_range)
    #create a copy of the original genes for later comparison
    original_population = []
    for item in population:
        original_population.append(copy.deepcopy(item.genes))
    genetic_alg.mutate(population, test_range, 0)

    #compare every gene of every individual to ensure none have changed
    for i in range(len(population)):
        for param in test_range:
            if population[i].genes[param.name] != original_population[i][param.name]:
                isError = True
                print("Gene",param.name,"has been altered but should match:",population[i].genes[param.name],"vs",original_population[i][param.name])

    if not isError:
        print("Mutation rate of zero works correctly")

    return isError


#Does not yet test increment!
def test_mutation_range():
    print("-------\nTesting mutation ranges of 400 genes")
    test_range = []  # "name minimum maximum increment"
    test_range.append(individual.ParamRange("a", 0, 100, 10))
    test_range.append(individual.ParamRange("b", 5, 11, 3))
    test_range.append(individual.ParamRange("c", 1, 7, 1))
    test_range.append(individual.ParamRange("d", 50, 51, 1))

    isError = False
    population = individual.create_initial_population(100, test_range)
    genetic_alg.mutate(population, test_range, 100)

    # compare every gene of every individual to ensure all still in original range
    for ind in population:
        if not (0<=ind.genes["a"]<=100):
            print("gene a not in correct range")
            isError = True
        if not (5 <= ind.genes["b"] <= 11):
            print("gene b not in correct range")
            isError = True
        if not (1 <= ind.genes["c"] <= 7):
            print("gene c not in correct range")
            isError = True
        if not (50 <= ind.genes["d"] <= 51):
            print("gene d not in correct range")
            isError = True

    if not isError:
        print("Mutation correctly alters range of parameters")

    return isError


def test_choose_ind_random():
    print("-------\nTesting random pairing of individuals")
    test_range = []  # "name minimum maximum increment"
    test_range.append(individual.ParamRange("a", 0, 100, 10))
    test_range.append(individual.ParamRange("b", 5, 11, 3))
    test_range.append(individual.ParamRange("c", 1, 7, 1))
    test_range.append(individual.ParamRange("d", 50, 51, 1))

    isError = False
    num_individuals = 100
    population = individual.create_initial_population(num_individuals, test_range)

    pairs = genetic_alg.choose_individuals(population,"random")
    count_same = 0
    if len(pairs) != num_individuals/2:
        print("Does not create the correct number of pairs")
        isError=True
    for sublist in pairs:
        if len(sublist) != 2:
            print("Is not a pair: ",sublist)
            isError=True
        else: # these will fail if the above if is true
            if not (0<=sublist[0]<len(population) and 0<=sublist[1]<len(population)):
                print("Indices in pair list are invalid")
                isError=True
            if sublist[0]==sublist[1]:
                count_same+=1
    print("There are ",count_same,"pairs where both values are the same index")
    if not isError:
        print("Random pairing completed successfully")


def run_ga_crossover():
    print("-------\nRunning the GA crossover")
    print("To be able to fully tell if this works, need to print crossover points and individuals")
    test_range = []  # "name minimum maximum increment"
    test_range.append(individual.ParamRange("a", 0, 100, 10))
    test_range.append(individual.ParamRange("b", 5, 11, 3))
    test_range.append(individual.ParamRange("c", 1, 7, 1))
    test_range.append(individual.ParamRange("d", 50, 51, 1))

    isError = False
    num_individuals = 10
    population = individual.create_initial_population(num_individuals, test_range)
    print("Population before crossover:")
    individual.print_population(population)
    new_pop = genetic_alg.crossover(population,test_range)

    if len(new_pop) != len(population):
        print("Crossed over population is not correct length")
        isError=True
    print("Crossed over pairs:")
    individual.print_population(new_pop)


# RUN the tests
test_mutation_none()
test_mutation_range()
test_choose_ind_random()
run_ga_crossover()