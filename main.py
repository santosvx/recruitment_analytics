import pandas as pd
import numpy as np
import datetime as dt
import os
import csv

import listsforrec

cwd = os.getcwd()
tracker_file = input("Please input the file name for your phone screen tracker: ")
start_date = input("Please enter the start date time. ('mm/dd/yyyy'): ")
end_date = input("Please enter the start date time. ('mm/dd/yyyy'): ")

print(start_date[2:3], start_date[5:6])

def get_file_location():
    """Locates phone_tracker.csv file in refs directory. Returns .csv as a
    pandas dataframe."""

    df = pd.read_csv(f"{cwd}/phoneDbs/{tracker_file}")
    return(df)

def get_datetime(date_string):
    if (date_string[2:3] == "/") and (date_string[5:6] == "/"):
        date_time = dt.datetime.strptime(date_string, "%m/%d/%Y")
        return(date_time)


def get_date_parameters(df):
    pass


proper_format_date(start_date)
