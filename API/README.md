# API

The java file RunNetLogoModelSeed.java must be compiled before the tool can be run. It is model and GA agnostic. This code takes as input information that is required for running a NetLogo model. The Python/run.py file sends the necessary command line parameters to this program when it calls it. The file RunNetLogoModel.java is used by a python script in the ResultsAnalysis directory. It will need to be similarly compiled before use.

## Compilation

On a Mac:

``` javac -classpath ../lib/netlogo-mac-app.jar  RunNetLogoModelSeed.java ```

On linux:

``` javac -classpath ../lib/NetLogo.jar  RunNetLogoModelSeed.java ```
