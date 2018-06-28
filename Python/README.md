# Python

## Files

The files in this folder are the GA tool itself. They rely on the other files in the repository to be able to run.

* genetic_alg.py: functions specific to the genetic algorithm. These functions are model agnostic.
* individual.py: all functions related to an individual in the GA, i.e. a set of model parameters and its associated fitness. The named tuples in this file are the types used to store this information. The compute_fitness functions are aware of the model being run, as it calls the correct fitness function based on the command line parameter.
* test-genetic.py, test-individual.py, test-run.py: All include testing functions for testing the GA's implementation. They are not sufficient for fully testing the code.
* wolfsheep.py: Includes all fitness functions for the Wolf Sheep Predation NetLogo model.
* run.py: the main file that runs the program. 

## Command Line Parameters
The run.py file requires 15 parameters to run. Details on their requirements can be found in run.py:

1. The number of individuals in the population
2. The number of parameters for the model
3. Mutation rate
4. Target fitness
5. Maximum number of generations
6. Number of model replications to run for each individual
7. Number of individuals to keep via elitism
8. Tournament size for crossover
9. Path/name of the input file that contains the names and valid ranges for each model parameter to be learned
10. Maximum number of steps for each model to run
11. Fitness function to be used
12. Path/name of the model .nlogo file to be run
13. The prefix to put in front of each results file and intermediate step output file. Should be unique to identify results.
14. A file similar in format to #9, but containing the values of any model parameters that are held constant on all model instances. 

## To Run the Tool

```python3 run.py [the 14 command line parameters]```

Dependencies:

1. Java file in API folder has been compiled
2. Any desired fitness functions have been added within the code, including references to them in run.py and individual.py
3. NetLogo model is available and the path is sent as a command line parameter

