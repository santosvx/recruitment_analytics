import pandas as pd
import numpy as np
import datetime as dt
import os
import csv

cwd = os.getcwd()
tracker_file = input("Please input the file name for your phone screen tracker: ")

def open_with_python(path):
    """Attempts to open the .csv and resave it in a format pandas can open."""

    with open(path, "r") as in_csv:
        content = csv.reader(in_csv, delimiter=",")

        for row in content:
            print(row)

def get_dataframe_file():
    """Locates phone_tracker.csv file in refs directory. Returns .csv as a
    pandas dataframe."""

    pth = ("{}/phoneDbs/{}".format(cwd, tracker_file))
    return(pth)


tracker_file = get_dataframe_file()
open_with_python(tracker_file)
