"""CSC110 COVID-19 Final Project: Modelling the Canadian Housing Market

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Terence Liu, Woojin Jang, and Charlie Tao.
"""
import datetime
import csv


# Convert csv file to tuple[list]
def csv_to_dict(filename: str) -> dict[datetime: float]:
    """Returns a dictionary of datetime to floats from a given csv file
     to represent the x and y axis when graphed
    """
    data = {}
    with open(filename) as file:
        reader = csv.reader(file)

        for n in reader:
            if n[0][0:2] == 'q1':
                date = datetime.date(int('20' + n[0][3:5]), 1, 1)
                data[date] = float(n[1])
            elif n[0][0:2] == 'q2':
                date = datetime.date(int('20' + n[0][3:5]), 4, 1)
                data[date] = float(n[1])
            elif n[0][0:2] == 'q3':
                date = datetime.date(int('20' + n[0][3:5]), 7, 1)
                data[date] = float(n[1])
            elif n[0][0:2] == 'q4':
                date = datetime.date(int('20' + n[0][3:5]), 10, 1)
                data[date] = float(n[1])
            elif not n[0].isalpha() and not n[1].isalpha():
                date = datetime.date(int(n[0][0:4]), int(n[0][5:7]), int(n[0][8:10]))
                data[date] = float(n[1])

    return data
