# Results Analysis

## Files

The files in this folder are for analyzing the results from the GA.

* runforplots.py: Used to analyze how well the parameters found by the GA works. Runs each set of best parameters a set number of times, and reports the result of each (swg/sdie/s10k/wdie/w10k). Also graphs the agent counts over time.
* analysis.sh: Pulls the data from the end results file and sends to results-to-csv.py to process.
* results-to-csv.py: Processes results from the GA. This is the main processing file for results.
* minmax.py: Takes results from runforplots.py and puts into columns to be addedto results-to-csv data. For fitness functions that care about agent count.
* agentspread.py: Takes results from runforplots.py and puts into columns to be addedto results-to-csv data. Is for fitness fuctions that care about standard deviation, not actual agent counts.
* combine.py: Pulls data from a csv and summarizes in a way that is needed for a plot.
* bar.py: Code for creating a bar chart
* multibar.py: Code for creating a multibar chart
* boxplot.py: Code for creating a boxplot
* All other files are for creating specific charts using bar.py, multibar.py, or boxplot.py.

## Process for analyzing GA Results

1. Run analysis.sh on log and end files
2. Run runforplots.py on the found NetLogo parameters, copy over results into the csv files to use as input files. Should be list of parameter names as first row, then list of parameter values (one set per row). Whitespace delimited.
3. For agent focused runs, run minmax.py, and copy over the results to the csv created by analysis.sh. For standard deviation focused runs, instead use agentspread.py
4. Run combine.py with desired combination of data for your plot
5. Run appropriate plotting function.