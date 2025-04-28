import os
import csv

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'genre_title.csv')
outhput_path = os.path.join(current_dir, 'genre_title_ne_demo.csv')

with open(file_path, encoding='utf-8') as file:
    rows = csv.reader(file, delimiter=',', quotechar='"')
    data = []
    for index, row in enumerate(rows):
        row = row[1:]
        row[0] = str(int(row[0]) + 32)
        row[1] = str(int(row[1]) + 15)
        data.append(row)
    for row in data[:3]:
        print(row)

with open(outhput_path, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"')
    for row in data:
        writer.writerow(row)