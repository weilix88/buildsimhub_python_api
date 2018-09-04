"""
AUTHOR: Haopeng Wang, Weili Xu
Date: 9/3/2018

What is this script for?
Assume the data is organized in an hourly interval -
This script can analyze the 8760 (8784) hours operation data, and post-process them into a schedule object in
EnergyPlus compact schedule format.

In the compact schedule, every hour in a week is averaged by all the same hours on the same date (Monday, Tuesday...).

This is useful for model calibrations.


How to use this script?
Prepare a csv file. Here is the preparation instruction:
1. The first row should be header row
1. The first column should be timestamp column
2. No missing values or N/A values. - please pay extra attention to outlinears as this script does not have the ability
to detect outlinears.

Package required:
pandas, numpy

"""

import pandas as pd
import numpy as np

if __name__ == "__main__":
    # CSV file should be in ASCII encoding
    path = "D:\\Chrome Download\\ss\\fanCoil_414.csv"

    with open(path + ".schedule.idf", 'w') as f:
        f.write("ScheduleTypeLimits,\n")
        f.write("    Fraction,                !- Name\n")
        f.write("    0,                       !- Lower Limit Value\n")
        f.write("    1,                       !- Upper Limit Value\n")
        f.write("    Continuous,              !- Numeric Type\n")
        f.write("    Dimensionless;           !- Unit Type\n")
        f.write("\n")
    f.close()

    record = pd.read_csv(path, skiprows=0, header=None)
    spots = len(record.columns)

    # First column is timestamp
    record[0] = pd.to_datetime(record[0])
    record["WeekDay"] = record[0].dt.dayofweek
    record["Date"] = record[0].dt.date

    record["Hour"] = record[0].dt.hour
    pd.to_numeric(record["Hour"], errors='coerce')

    weekdays = [i + 1 for i in range(7)]
    hours = [i for i in range(24)]

    # First row is sensor names
    for i in range(1, spots):
        name = record[i][0]
        res = pd.DataFrame(index=weekdays, columns=hours)

        for w in weekdays:
            date = record.loc[(record["WeekDay"] == w - 1)]
            for h in hours:
                date_hour = date.loc[(record["Hour"] == h)]
                values = date_hour.loc[:, i]
                values = values.astype(np.float)
                num = date_hour.shape[0]

                res[h][w] = round(sum(values) / num, 3)  # occupancy possibility

        # res.to_csv(path+".processed.csv")

        week_map = {1: 'Monday',
                    2: 'Tuesday',
                    3: 'Wednesday',
                    4: 'Thursday',
                    5: 'Friday'}

        with open(path + ".schedule.idf", 'a') as f:
            f.write("Schedule:Compact,\n")
            f.write("    " + name + ",    !- Name\n")
            f.write("    Fraction,                !- Schedule Type Limits Name\n")
            f.write("    Through: 31 Dec,         !- Field 1\n")

            for week in range(1, 6):
                f.write("    For: " + week_map[week] + ",\n")

                for hour in range(24):
                    f.write("    Until: " + str(hour + 1) + ":00,\n")
                    f.write("    " + str(res[hour][week]) + ",\n")

            f.write("    For: SummerDesignDay,\n")
            f.write("    Until: 24:00,\n")
            f.write("    1,\n")
            f.write("    For: WinterDesignDay,\n")
            f.write("    Until: 24:00,\n")
            f.write("    0,\n")
            f.write("    For: AllOtherDays,\n")
            f.write("    Until: 24:00,\n")
            f.write("    0.05;\n")
            f.write("\n")

        f.close()
