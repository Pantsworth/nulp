__author__ = 'DoctorWatson'

import json


file_path = "/Users/DoctorWatson/Documents/College Stuff/Spring 2015/EECS 348 AI/nulp/movies_reviews/"

obj = open(file_path, "r")

print obj

for data in obj:
    print data

for file in