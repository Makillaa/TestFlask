import csv
import os
import sqlite3
from api_application import basedir

con = sqlite3.connect(os.path.join(basedir, 'test_results.db'))
cur = con.cursor()

with open('test_results.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Device type'], i['Operator'], i['Time'], i['Success']) for i in dr]


cur.executemany("INSERT INTO results_model (type, operator, datetime, result) VALUES (?, ?, ?, ?);", to_db)
con.commit()
con.close()

