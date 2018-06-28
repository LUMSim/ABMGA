/*
* Example from Wiki on Controlling-API Netlogo GitHub project.
* To run from wiki: 
** Wiki denotes Java VM options that are required
** NetLogo.jar must be in your classpath.
** The lib directory, containing additional required libraries, must also be present. 
** When running without GUI support, the system property java.awt.headless must be true, to force the VM to run in headless mode.

* Further expectations, from the wiki:
** current working directory at startup time is the installation directory in which NetLogo.jar resides. On Mac OS X this is NetLogo.app/Contents/Java/, on Windows this is C:\<Path to NetLogo>\app, and on linux this is <path to NetLogo>/app. 
** The lib subdirectory (relative to the working directory) includes native libraries for Mac (is not needed on other platforms)
** The natives subdirectory (relative to the working directory) includes native libraries for all platforms.
** Assumes that there will be models, docs, and extensions subdirectories of the working directory, but will look for them at a specific path if following java environment variables are set:
**** Docs - -Dnetlogo.docs.dir=<path-to-docs>
**** Extensions - netlogo.extensions.dir=<path-to-extensions>
**** Models - netlogo.models.dir=<path-to-models>
*/

// Author: Megan Olsen
// Date: December 2017

import org.nlogo.headless.HeadlessWorkspace;
import java.util.ArrayList;
import java.io.*;

public class RunNetLogoModelSeed {

  /* 
    Program expects at least five command line parameters: model name, name of the input file, 
    number of steps to run the model, and any reports to run at the end of the model for results gathering.
    The input file must contain model parameters and values, one per line, in the format "set <variable name> <value>".
  */
  public static void main(String[] argv) {
  	if(argv.length < 5) {
  		System.out.println("Not enough arguments. Expecting at least 5");
  		System.exit(-1);
  	}
    HeadlessWorkspace workspace =	HeadlessWorkspace.newInstance();
    //Process command line arguments
    String model_name = argv[0];
    System.out.println(model_name);
    String file_name = argv[1];
    int number_steps = Integer.parseInt(argv[2]);
    String seed = argv[3];
    int count = 4;
    ArrayList<String> reports = new ArrayList<String>();
    while(count < argv.length) {
      reports.add(argv[count]);
      count++;
    }
    
    ArrayList<String> parameter_list = readParameters(file_name);
    try {
      workspace.open(model_name);
      for(int i=0; i<parameter_list.size();i++){
        workspace.command(parameter_list.get(i));
      }
      //uses "set" before an actual parameter value, <set name value>
      workspace.command("random-seed "+seed);
      workspace.command("setup");
      workspace.command("repeat "+number_steps+" [ go ]");
      for(int i=0; i<reports.size(); i++)
      {
        System.out.println(workspace.report(reports.get(i)));
      }
      workspace.dispose();
    }
    catch(Exception ex) {
      ex.printStackTrace();
    }
  }

  /*  reads in all model parameters.
      Assumes model parameters are one per line, in the form "set <variable name> <value>"
      Returns the list of parameters and values.
  */
  public static ArrayList<String> readParameters(String file_name){
    ArrayList<String> parameters = new ArrayList<String>();
    try {
      // FileReader reads text files in the default encoding.
      FileReader fileReader = new FileReader(file_name);
      String line;
      // Always wrap FileReader in BufferedReader.
      BufferedReader bufferedReader = new BufferedReader(fileReader);

      while((line = bufferedReader.readLine()) != null) {
          parameters.add(line); //assumes that "set" is included before parameter names
      }   

      bufferedReader.close();         
    }
    catch(FileNotFoundException ex) {
        System.out.println("Unable to open file '" + file_name + "'");                
    }
    catch(IOException ex) {
        System.out.println("Error reading file '" + file_name + "'");
    }
    return parameters;
  }
}
