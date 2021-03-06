import json
import os
import bayes



file_path = "/Users/DoctorWatson/Documents/College Stuff/Spring 2015/EECS 348 AI/nulp/movies_reviews/"
file_path_short = "/Users/DoctorWatson/Documents/College Stuff/Spring 2015/EECS 348 AI/nulp/"

json_object = []

def read_reviews(file_path):
    for file in os.listdir(file_path):
        obj = open(file_path + file, "r")
        review_title = file
        review_text = obj.read()
        review_status = review_title[7]
        tokenize_test = bayes.freed_tokenize(review_text)
        jsonString = {"name": review_title, "status": review_status, "text": review_text}
        json_object = json_object + [json.dumps(jsonString)]


    with open(file_path_short + 'data.json', 'w') as outfile:
        json.dump(json_object, outfile)

    with open(file_path_short + 'data.json', 'r') as f:
         data = json.load(f)
         # print data

    for datum in data:
        datum = json.loads(datum)
        print datum['text']
        print "done"


def load_json_database():
    """paths for each user will be different, and I didn't have a good way to specify it..."""

    path = bayes.relative_path('data.json')
    with open(path, 'r') as f:
         data = json.load(f)


    return data