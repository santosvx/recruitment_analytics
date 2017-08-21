import pandas as pd
import numpy as np
import datetime as dt
import os
import csv

cwd = os.getcwd()
tracker_file = input("Please input the file name for your phone screen tracker: ")


def open_with_python(path):
    """Attempts to open the .csv and resave it in a format pandas can open."""

    rows_to_write = []

    with open(path, "r") as in_csv:
        csv_read = csv.reader(in_csv, delimiter = "\t")

        for row in csv_read:
                rows_to_write.append(row)

    with open(path + "'", "w") as out_csv:
        csv_write = csv.writer(out_csv, delimiter = ",")

        for row in rows_to_write:
            csv_write.writerow(row)

    return(out_csv)

def get_file_location():
    """Locates phone_tracker.csv file in refs directory. Returns .csv as a
    pandas dataframe."""

    pth = (f"{cwd}/phoneDbs/{tracker_file}")
    return(pth)

tracker_file = get_file_location()
tracker_file = open_with_python(tracker_file)
df = pd.read_csv(tracker_file)
print(df)
