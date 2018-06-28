# API

The java file must be compiled before the tool can be run. It is model and GA agnostic. This code takes as input information that is required for running a NetLogo model. The Python/run.py file sends the necessary command line parameters to this program when it calls it.

## Compilation

On a Mac:

``` javac -classpath ../lib/netlogo-mac-app.jar  RunNetLogoModel.java ```

On linux:

``` javac -classpath ../lib/NetLogo.jar  RunNetLogoModel.java ```
