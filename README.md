# CS5530Assignment1
# Name: Riley Bruce

For this assignment, we were tasked with outlining the steps of a reproducible workflow (question 1) and generating data graphics (question 2). I've separated the questions into their respective folders with notebooks outlining my process/thoughts, and python scripts for easily running everything at once. 

question 1:
I seperated the data getting/cleaning code (clean_data.py) and the data analysis code (analysis.py) and when testing the scripts, clean_data.py will need ran before analysis.py. The script clean_data.py generates a two csv files (the raw/cleaned data), while analysis.py generates two images and a file with the results of the t-test.

question 2:
For this question I had one python script (generate_vis.py) and one notebook outlining my process. I opted not to separate the script into two separate scripts, because really the only data cleaning being done is mapping categorical variables to integer values. The script generates one csv file and 17 images upon execution. I may have went overboard with the images, but many have to do with the same kind of analysis and I used loops to generate them.
