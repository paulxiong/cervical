import numpy as np
import os
import sys
import ntpath
from matplotlib import pyplot as plt
import pandas as pd
import shutil
import glob
import datetime

ROOT_FOLDER = 'datasets/classify/'
FOLDER_PATTERN = '*.png_output'
RESULT_FILE = "/preview/final_result.csv"
ANALYSIS_REPORT = "analysis_report.txt"
current_time = datetime.datetime.now()

def analyze():
    if not os.path.exists(ROOT_FOLDER): print("This script is not in the right folder. pls run it under: ", ROOT_FOLDER)

    TOTAL_CELL_NUM = 0
    POSITIVE_CELL_NUM = 0    
    THRESHOLD = 0.48

    if os.path.exists(ANALYSIS_REPORT):
        os.remove(ANALYSIS_REPORT)  

    with open(ANALYSIS_REPORT, 'a+') as f:
        f.write(str(current_time))
        f.write("\nWith threshold as: " + str(THRESHOLD) +", ")
        f.write("The analysis report is as following: \n\n\n")
        total_folders = np.sort(glob.glob(os.path.join(ROOT_FOLDER, FOLDER_PATTERN)))

        for folder in total_folders:
            f.write("Positive cell in folder "+ folder + ":\n")
            filename = folder + RESULT_FILE

            try:
                data = pd.read_csv(filename)
                for i in range(len(data)):
                    TOTAL_CELL_NUM += 1
                    #print("score is: ", data.iloc[i][1])
                    if float(data.iloc[i][1]) >= THRESHOLD:
                        POSITIVE_CELL_NUM += 1
                        f.write(str(data.iloc[i][0]) + " : " + str(data.iloc[i][1]) + "\n")
            except:
                continue

        print("---------Analysis Summary Report (threshold as %s, detail in %s)---------\n" % (str(THRESHOLD), ANALYSIS_REPORT)) 
        print("Total cell num is: %d" % TOTAL_CELL_NUM)
        print("Positive num is: %d" % POSITIVE_CELL_NUM)
        print("Positive ratio is: %f" % (POSITIVE_CELL_NUM * 1.0/TOTAL_CELL_NUM))
        f.write("\n\n---------------SUMMARY------------------\n\n")
        f.write("Total cell num is: " + str(TOTAL_CELL_NUM) + "\n")
        f.write("Positive cell num is: " + str(POSITIVE_CELL_NUM) + "\n")
        f.write("Positive ratio is: " + str(POSITIVE_CELL_NUM * 1.0/TOTAL_CELL_NUM))
    f.close()

if __name__ == '__main__':
    analyze()
