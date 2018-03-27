#!/usr/bin/env python
#
"""
Convert Sanitas SBF70 database to a csv file that openScale can import
Tested with openScale v1.7.1 and HealthCoach v2.4
.
.1) Copy "Healthcoach.db" from "de.sanitas_online.healthcoach/databases" path
.2) Run this script with: python sanitas2openscale.py
.3) Inside OpenScale tab "Table" run "Import" and choose converted CSV "openScale.csv"
.4) Profit!
"""
import sys
import os
import csv
import sqlite3
from dateutil.parser import parse

#Check if DB exists
if os.path.isfile('Healthcoach.db'):
    pass
else:
    print "Healthcoach.db file not found!"
    sys.exit(1)


#RAW EXPORT FROM DATABASE
db = sqlite3.connect('Healthcoach.db')
cursor = db.cursor()

cursor.execute("SELECT * FROM ScaleMeasurements")

with open('/tmp/sanitas.csv', 'wb') as out_csv_file:
    csv_out = csv.writer(out_csv_file)
    for result in cursor:
        csv_out.writerow(result)

cursor.close()
db.close()

#CONVERT TO OPENSCALE FORMAT CSV
r = csv.reader(file('/tmp/sanitas.csv'))
writer = csv.writer(file("openScale.csv", "w"), delimiter=",")

for w in r:
    if len(w) == 0 or w[0].startswith("#"):
        continue
    #print w
    time = w[3]
    weight = w[4]
    fat = w[6]
    water = w[9]
    muscle = w[10]
    bone = w[13]
    comment = w[19]
    d = parse(time)
    #id, userId,enabled,Datetime,Weight,Fat,Water,Muscle,Lbw,Bone,Waist,Hip,Comment
    writer.writerow([d.strftime('%d.%m.%Y %H:%M'), weight, fat, water, muscle, 0.0, bone, 0.0, 0.0, comment])

#Remove temp file
os.remove('/tmp/sanitas.csv')

#EOF
