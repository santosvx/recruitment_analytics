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

    try:
        date_string = date_string.split("/")
    except AttributeError:
        return(date_string)

    if date_string[0] == "nan" or len(date_string) != 3:
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

def format_datewecall_string(cell):
    cell = str(cell)
    cell = cell.split(",")
    cell = cell.pop(-1)
    cell = cell.split("/")
    if len(cell) == 2:
        cell.append("16")
    this = cell[0].split("-")
    this = this.pop(-1)
    cell[0] = this
    cell = ("/").join(cell)
    if "-" in cell:
        dash_point = cell.rfind("-")
        cell = cell[dash_point:]
    try:
        if cell != "nan":
            if cell[0] == "-" and cell[1] == " ":
                cell = cell[2:]
            if cell[0] == " " or cell[0] == "-":
                cell = cell[1:]
            if cell[0] == "M" or cell[0] == "G":
                cell = cell[3:]
            if cell[0] == "e":
                cell = cell[8:]
        if len(cell) < 6:
            cell = "nan"
        return(cell)
    except IndexError:
        return(cell)

df = get_file_location()

# for cell in df["Date Participant Calls"]:
#     cell = str(cell) # for some reason one of the cells was being counted as an int. Probably Simone.
#     cell = format_date_string(cell)
#     cell = get_datetime(cell)
#     print(cell)

for i, cell in enumerate(df["Date We Call Participant"]):
    cell = format_datewecall_string(cell)
    cell = format_date_string(cell)
    cell = get_datetime(cell)
    print(cell, i)
