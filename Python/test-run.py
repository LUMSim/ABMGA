# To test any part of the main code, replace main in run.py with the contents of one of the following functions:
import individual

def test_file_write():
    print("-------\nTesting writing to file of 3 population members")
    population = []
    population.append(individual.Ind(size=5, genes={"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}, fitness=0))
    population.append(individual.Ind(size=5, genes={"a": 6, "b": 7, "c": 8, "d": 9, "e": 10}, fitness=0))
    population.append(individual.Ind(size=5, genes={"a": 1, "b": 3, "c": 5, "d": 7, "e": 9}, fitness=0))
    filename = run.write_input_files(population)
    print("Check for 3 files that start with the name",filename)
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
    NUM_INDIVIDUALS = 2
    ind = individual.Ind(size=5,
                         genes={"initial-number-sheep": 100, "initial-number-wolves": 25, "sheep-gain-from-food": 5,
                                "sheep-reproduce": 10, "wolf-reproduce": 20}, fitness=0)
    individual.write_file_NetLogo(ind, "0test.txt")
    ind = individual.Ind(size=5,
                         genes={"initial-number-sheep": 50, "initial-number-wolves": 5, "sheep-gain-from-food": 5,
                                "sheep-reproduce": 10, "wolf-reproduce": 20}, fitness=0)
    individual.write_file_NetLogo(ind, "1test.txt")

    create_wait_children("test.txt")
    print("Experiments complete.",NUM_INDIVIDUALS,"modelresults files should exist.")


def test_main():
    NUM_INDIVIDUALS = 2
    NUM_GENERATIONS = 1
    main()