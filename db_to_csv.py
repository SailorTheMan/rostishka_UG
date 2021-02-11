import csv
import sqlite3

# TODO в русские буквы не может

conn = sqlite3.connect('sim_data.sqlite')
cursor = conn.cursor()
cursor.execute("select * from id_factory;")
with open("copy_db.csv", "w", newline='') as csv_file:  # Python 3 version    
#with open("out.csv", "wb") as csv_file:              # Python 2 version
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description]) # write headers
    csv_writer.writerows(cursor)