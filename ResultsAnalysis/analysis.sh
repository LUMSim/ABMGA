# read through and process output files, put in csv format
# need last 10 lines of "end" file. Rest is done by the python script
for file in GAS100*end.txt #replace GAS100 with prefix of files to be analyzed
do
	head -n 1 $file > analysis-$file
    tail -n 9 $file >> analysis-$file
    python3 results-to-csv.py analysis-$file 
    #rm analysis-$file 
done