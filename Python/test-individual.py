import individual

def test_input_reading():
    print("--------\nTesting file reading of ranges...")
    ranges = individual.read_ranges("../WolfSheep/ranges.txt")
    print(ranges)
    print("CHECK if the above ranges match the input file")

# Tests if:
# correct number of individuals are created
# gene values of individuals are within given ranges
# gene values of individuals match increment
# fitness has been set to zero for each individual
def test_create_initial_population(num_individuals):
    print("--------\nTesting creation of population...")
    test_range = [] #"name minimum maximum increment"
    test_range.append(individual.ParamRange("a",0,100,10))
    test_range.append(individual.ParamRange("b", 5, 11, 3))
    test_range.append(individual.ParamRange("c", 1, 7, 1))
    test_range.append(individual.ParamRange("d", 50, 51, 1))

    countOf50d = 0
    isError = False
    population = individual.create_initial_population(num_individuals,test_range)
    assert(len(population)==num_individuals), "incorrect number of individuals created"
    for ind in population:
        if not(ind.fitness == 0):
            print("Fitness not set to zero!")
            isError = True
        if ind.size != 4:
            print("Size not correctly set!")
            isError = True
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
        if(ind.genes["a"]%10!=0):
            print("increment for gene a not correctly used")
            isError = True
        if(ind.genes["b"]%3!=0):
            print("increment for gene b not correctly used")
            isError = True
        if ind.genes["d"] == 50:
            countOf50d+=1
    if(countOf50d == num_individuals):
        print("all of type d individuals have value 50")
        isError = True
    elif (countOf50d == 0):
        print("all of type d individuals have value 51")
        isError = True
    if not isError:
        print("Test of population creation complete with no errors")

# Tests if:
# Crossover correctly crosses individuals at each possible crossover point.
# Crossover point is defined as the index and which swapping starts
def test_crossover():
    #use these 2 individuals for all sub tests
    individual_1 = individual.Ind(size=5, genes={"a":1,"b":2,"c":3,"d":4,"e":5}, fitness=0)
    individual_2 = individual.Ind(size=5, genes={"a": 6, "b": 7, "c": 8, "d": 9, "e": 10}, fitness=0)
    ranges=[individual.ParamRange("a",0,10,1),individual.ParamRange("b",0,10,1),individual.ParamRange("c",0,10,1),
            individual.ParamRange("d",0,10,1),individual.ParamRange("e",0,10,1)]
    isError = False
    print("--------\nTesting crossover for individuals",individual_1.genes,"and",individual_2.genes)
    for cross_point in range(1,4):
        print("Testing crossover point ",cross_point,"...")
        ret_pop = [] #restart each time through
        individual.crossover(individual_1, individual_2, ret_pop, ranges, cross_point)

        #Test that the individuals are correct
        print(ret_pop[0],ret_pop[1])
        for i in range(cross_point): #check up to cross point in each individual in ret_pop for no change
            if (ret_pop[0].genes[ranges[i].name]!=individual_1.genes[ranges[i].name]) or \
                (ret_pop[1].genes[ranges[i].name] != individual_2.genes[ranges[i].name]):
                isError = True
                print("Error at gene ",ranges[i].name," using crossover point ",cross_point)
        for i in range(cross_point,len(ranges)):
            if (ret_pop[0].genes[ranges[i].name] != individual_2.genes[ranges[i].name]) or \
                (ret_pop[1].genes[ranges[i].name] != individual_1.genes[ranges[i].name]):
                isError = True
                print("Error at gene ",ranges[i].name," using crossover point ",cross_point)

    if not isError:
        print("Crossover test complete with no errors")


#assumes that all input is integers
def test_file_write():
    print("--------\nTesting writing to file for model input...")
    individual_1 = individual.Ind(size=5, genes={"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}, fitness=0)
    individual.write_file_NetLogo(individual_1,"test_file_output.txt")

    fd = open("test_file_output.txt","r")
    file_genes = {}
    for line in fd:
        split = line.split()
        if split[0] != "set":
            print("ERROR: set is missing at start of line")
        file_genes[split[1]]=int(split[2])
    fd.close()
    if len(individual_1.genes.keys()) != len(file_genes.keys()):
        print("number of variables from individual do not match number of variables in file")
    elif not("a" in file_genes.keys() and "b" in file_genes.keys() and "c" in file_genes.keys() and "d" in file_genes.keys()
         and "e" in file_genes.keys()):
        print("one or more variables is missing in the file")
        print("variables in individual: ",individual_1.genes.keys())
        print("variables in file: ",file_genes.keys())
    elif individual_1.genes["a"] != file_genes["a"] or individual_1.genes["b"] != file_genes["b"] \
        or individual_1.genes["c"] != file_genes["c"] or individual_1.genes["d"] != file_genes["d"] \
        or individual_1.genes["e"] != file_genes["e"]:
        print("values in the file do not match values from individual")
        print("values in individual: ", individual_1.genes)
        print("values in file: ",file_genes)
    else:
        print("File writing is correct")
    #print("End of testing output file writing")

def test_fitness_calculation():
    print("--------\nTesting fitness calculation...")
    print("Not yet implemented.")

test_file_write()
test_fitness_calculation()
test_create_initial_population(10)
test_crossover()
test_input_reading()