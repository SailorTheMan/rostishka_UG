
import csv
import sqlite3

def read_time(csv_file_location):
    csv.register_dialect('empDialect', skipinitialspace=True, strict=True)

    employee_file = csv.DictReader(open(csv_file_location), dialect = 'empDialect')
    employee_list = []
    for data in employee_file:
        employee_list.append(data)
    return employee_list


def write_to_db(full_list):
    conn = sqlite3.connect('sim_data.sqlite')
    cursor = conn.cursor()
    print(full_list)
    for item in full_list:
        print(item['Время погрузки']+item['Название'])
        cursor.execute("""
            UPDATE id_factory
            SET Время погрузки = ?
            WHERE Название = ?;
        """, ('%'+item['Время погрузки']+'%', item['Название']))
        conn.commit()



    conn.close()





id_list = read_time('id_factory.csv')
write_to_db(id_list)

