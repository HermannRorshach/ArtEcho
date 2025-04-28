import os
import csv

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'review.csv')
outhput_path = os.path.join(current_dir, 'review_ne_demo.csv')

with open(file_path, encoding='utf-8') as file:
    rows = csv.reader(file, delimiter=',', quotechar='"')
    data = []
    for index, row in enumerate(rows):
        if index == 0:
            data.append(row[1:])
        else:
            row = row[1:]
            row[0] = str(int(row[0]) + 32)
            row[2] = str(int(row[2]) + 5)
            data.append(row)
    for row in data[:3]:
        print(row)

with open(outhput_path, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"')
    for row in data:
        writer.writerow(row)