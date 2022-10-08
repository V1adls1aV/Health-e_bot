import sqlite3
import csv

with open('new_additions.csv', encoding='utf-8') as file:
    items = list(csv.reader(file, delimiter=',', quotechar='"'))
items = list(filter(lambda x: x, items))


db = sqlite3.connect('Users_data.db')
curs = db.cursor()

for el in items:
    curs.execute(
    f"""
    INSERT INTO e_additions (e_number, e_name, harm, property, usage, influence)
    VALUES {tuple(el)}
    """)

db.commit()
db.close()