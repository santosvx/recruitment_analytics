import pandas as pd
import numpy as np
import math
import datetime as dt
import os
import csv

import listsforrec

def determine_time():

    if dt.datetime.now() <= dt.datetime(2017, 9, 15):
        return(dt.datetime.now())
    else:
        return(dt.datetime(2017, 9, 15))

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
            if cell[-1:] == "" or cell[-1:] == " ":
                cell = cell[-1:] + "17"
        if len(cell) < 6:
            cell = "nan"
        return(cell)
    except IndexError:
        return(cell)

cwd = os.getcwd()
tracker_file = input("Please input the file name for your phone screen tracker: ")
start_date = dt.datetime(2016, 9, 16)
end_date = determine_time()

df = get_file_location()

date_time_list = []
for i, cell in enumerate(df["Date We Call Participant"]):
    cell = format_datewecall_string(cell)
    cell = format_date_string(cell)
    cell = get_datetime(cell)
    date_time_list.append(cell)

df["Final Call"] = date_time_list

df["Final Contact"] = np.where(df["Final Call"] == None, df["Date Participant Calls"], df["Final Call"])
df["Final Contact"] = pd.to_datetime(df["Final Contact"], unit='ns')
df["Phone Screen Date"] = np.where(df["Phone screened?"] == "Yes", df["Final Call"], None)
df["Phone Screen Date"] = pd.to_datetime(df["Phone Screen Date"], unit='ns')

df = df.set_index(df["Phone Screen Date"])
df = df.sort_values("Phone Screen Date")

df.to_csv("here.csv")

dt_list = df["Phone Screen Date"].tolist()

dt_indexes = []
for row in dt_list:
    if row >= start_date and row <= end_date:
        dt_indexes.append(row)

start_index = dt_indexes.pop(0)
end_index = dt_indexes.pop(-1)

print(f"START DATE: {start_index}")
print(f"END DATE: {end_index}")

df = df.ix[start_index:end_index]

df["Eligible Count"] = np.where((df["Eligible/Ineligible"] == "Eligible (HID: No)")
| (df["Eligible/Ineligible"] == "Eligible (HID: Yes)"), 1, None)

df["Ineligible Count"] = np.where(df["Eligible/Ineligible"] == "Ineligible", 1, None)

df.to_csv("there.csv")

num_eligible = df["Eligible Count"].count()
num_ineligible = df["Ineligible Count"].count()

print(f"NUM ELIGIBLE: {num_eligible}")
print(f"NUM INELIGIBLE: {num_ineligible}")
totl = num_ineligible + num_eligible
per_eli = round((num_eligible / totl) * 100)
print(f"PERFECT ELIGIBLE: {per_eli}")
print(f"TOTAL PARTICIPANTS: {totl}")
