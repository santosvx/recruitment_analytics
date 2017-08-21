import pandas as pd
import numpy as np
import math
import datetime as dt
import os
import csv

import listsforrec

cwd = os.getcwd()
tracker_file = input("Please input the file name for your phone screen tracker: ")
#start_date = input("Please enter the start date time. ('mm/dd/yyyy'): ")
#end_date = input("Please enter the start date time. ('mm/dd/yyyy'): ")
start_date = "10/22/1990"
end_date = "11/22/1990"

def get_file_location():
    """Locates phone_tracker.csv file in refs directory. Returns .csv as a
    pandas dataframe."""

    df = pd.read_csv(f"{cwd}/phoneDbs/{tracker_file}")
    return(df)

def get_datetime(date_string):
    """Convert dates in format mm/dd/yyyy to datetime objects."""
    if date_string != None:
        date_time = dt.datetime.strptime(date_string, "%m/%d/%y")
        return(date_time)

def format_date_string(date_string):
    """Convert strings to proper format for get_datetime to use."""

    date_string = date_string.split("/")

    if date_string[0] == "nan":
        pass
    else:
        if len(date_string[0]) != 2:
            date_string[0] = "0" + date_string[0]
        if len(date_string[1]) != 2:
            date_string[1] = "0" + date_string[1]
        if len(date_string[2]) != 2:
            new_date = []
            for i, char in enumerate(date_string[2]):
                if i >= 2:
                    new_date.append(char)
            date_string[2] = "".join(new_date)

        date_string = "/".join(date_string)

        return(date_string)

df = get_file_location()

for i, cell in enumerate(df["Date Participant Calls"]):
    cell = str(cell) # for some reason one of the cells was being counted as an int. Probably Simone.
    cell = format_date_string(cell)
    cell = get_datetime(cell)
    print(cell)
