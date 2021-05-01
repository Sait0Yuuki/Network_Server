import csv
import json

json_data = [json.dumps(d) for d in csv.DictReader(open('test.csv'))]

print (json_data)
