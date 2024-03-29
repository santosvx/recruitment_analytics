import pandas as pd
import numpy as np
import codecs
import math
import datetime as dt
import os
import csv

import listsforrec

def fix_unicode(tracker_file):

    with codecs.open(f"{cwd}/PhoneDBs/{tracker_file}", "r",encoding='utf-8', errors='ignore') as fdata:
        file_lines = csv.reader(fdata, delimiter=',')

        write_lines = []

        for row in file_lines:
            write_lines.append(row)

    with open(f"{cwd}/PhoneDBs/{tracker_file}", "w") as out_csv:
        writer = csv.writer(out_csv)

        for row in write_lines:
            writer.writerow(row)

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
fix_unicode(tracker_file)

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
df["Status Fixed"] = np.where((df["Status"] == "Inelgible") |
(df["Status"] == "Inelibible") | (df["Status"] == "Ineligble") |
(df["Status"] == "Ineligible"), "Ineligible", "X")

df = df.set_index(df["Phone Screen Date"])
df = df.sort_values("Phone Screen Date")

dt_list = df["Phone Screen Date"].tolist()

dt_indexes = []
for row in dt_list:
    if row >= start_date and row <= end_date:
        dt_indexes.append(row)

start_index = dt_indexes.pop(0)
end_index = dt_indexes.pop(-1)

df = df.ix[start_index:end_index]

df["Eligible Count"] = np.where((df["Status"] == "Eligible (HID: No)")
| (df["Status"] == "Eligible (HID: Yes)") | (df["Status"] == "Eligible"), 1, None)

df["Ineligible Count"] = np.where(df["Status Fixed"] == "Ineligible", 1, None)

df["Male Eligible Count"] = np.where((df["Eligible Count"] == 1) & (df["Gender"] == "M"), 1, None)
df["Female Eligible Count"] = np.where((df["Eligible Count"] == 1) & (df["Gender"] == "F"), 1, None)
df["Male Ineligible Count"] = np.where((df["Ineligible Count"] == 1) & (df["Gender"] == "M"), 1, None)
df["Female Ineligible Count"] = np.where((df["Ineligible Count"] == 1) & (df["Gender"] == "F"), 1, None)

df.to_csv("there.csv")

num_eligible = df["Eligible Count"].count()
num_male_eligible = df["Male Eligible Count"].count()
num_female_eligible = df["Female Eligible Count"].count()
num_ineligible = df["Ineligible Count"].count()
num_male_ineligible = df["Male Ineligible Count"].count()
num_female_ineligible = df["Female Ineligible Count"].count()
ineligible_reasons = df["Ineligibility Tracker_1"].value_counts()
where_they_heard = df["Where they heard about the study"].value_counts()
total_gender = df["Gender"].value_counts()

out_file = open("export_sheet.txt", "w")

out_file.write("""This is an export for a phone screen tracker between the dates of
{} and {}. \n""".format(start_index, end_index))
out_file.write("-------------------\n")
out_file.write(f"START DATE: {start_index}\n")
out_file.write(f"END DATE: {end_index}\n")
out_file.write("-------------------\n")
out_file.write(f"NUM ELIGIBLE: {num_eligible}\n")
out_file.write(f"NUM INELIGIBLE: {num_ineligible}\n")
totl = num_ineligible + num_eligible
per_eli = round((num_eligible / totl) * 100)
out_file.write(f"PERCENT ELIGIBLE: {per_eli}\n")
out_file.write(f"TOTAL PHONE SCREENS: {totl}\n")
out_file.write("-------------------\n")
out_file.write(f"GENDER DEMOGRAPHICS:\n")
out_file.write(str(total_gender) + "\n")
out_file.write("-------------------\n")
out_file.write(f"Male Eligible: {num_male_eligible}\n")
out_file.write(f"Female Eligible: {num_female_eligible}\n")
out_file.write(f"Male Ineligible: {num_male_ineligible}\n")
out_file.write(f"Female Ineligible: {num_female_ineligible}\n")
out_file.write("-------------------\n")
out_file.write("Reasons for ineligiblity:\n")
out_file.write(str(ineligible_reasons) + "\n")
out_file.write("-------------------\n")
out_file.write("Recruitment sites:\n")
out_file.write(str(where_they_heard) + "\n")

out_file.close()
