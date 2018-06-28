# ABMGA
A genetic algorithm tool for learning behaviors in an agent-based model. This tool is written in Python, and uses the NetLogo API for running NetLogo models. The API calling code is written in Java. 

Any paper that is written that needs to reference this tool should reference:

> M. Olsen, J. Laspesa, T. Taylor-D'Ambrosio. ON GENETIC ALGORITHM EFFECTIVENESS FOR FINDING BEHAVIORS IN
AGENT-BASED PREDATOR PREY MODELS. Proceedings of the Summer Simulation Multi-Conference (SummerSim'18). July 2018.

## Folders

A README within each folder will give details on its files:

* Python: Core tool code
* API: Code for running the NetLogo API (Java)
* WolfSheep: The modified NetLogo files for the Wolf Sheep Predation Model
* ResultsAnalysis: Python code for analyzing results from the GA, specifically for the Wolf Sheep model
* lib: libraries for NetLogo

## Dependencies

* Python 3.X 
* Java 8 JDK
* NetLogo jar file (found in lib folder)
