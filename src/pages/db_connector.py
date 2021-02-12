import sqlite3
import csv

def get_report():
    filename = 'pages/reports/report.csv'
    inpsql3 = sqlite3.connect('../sim_data.sqlite')
    sql3_cursor = inpsql3.cursor()
    sql3_cursor.execute('SELECT ID, manufacturer, Name, Model, cell, RFID_ID FROM "id_factory" WHERE cell IS NOT Null')
    with open(filename,'w', encoding='utf-8') as out_csv_file:
        csv_out = csv.writer(out_csv_file)
        # write header                        
        csv_out.writerow([d[0] for d in sql3_cursor.description])
        # write data                          
        for result in sql3_cursor:
            csv_out.writerow(result)
    inpsql3.close()
    return 'pages/reports/report.csv'

def executeStatement(statement):
    try:
        # conn = sqlite3.connect(settings.config['db_name'])
        conn = sqlite3.connect('../sim_data.sqlite')

    except:
        print('Connection to DB was not established')
    else:
        cursor = conn.cursor()
        cursor.execute(statement)
        if statement.startswith('SELECT'):
            result = cursor.fetchall()
            conn.close()
            return result
        else:
            conn.commit()
            conn.close()


def get_schedule():
    statement = 'SELECT ID, manufacturer, Name, Model, "Date", "Time in", "Time out" FROM "id_factory";'
    return executeStatement(statement)


def create_cell_dict(row):
    return {'empty': False, 'id':row[0], 'manuf':row[1], 'name':row[2], 'model':row[3], 'cell_id':row[4], 'RFID_ID':row[5]}


def get_warehouse():
    warehouse_1 = [[{'cell_id': j * 9 + i + 1, 'empty':True} for i in range(9)] for j in range(6)]

    warehouse_2 = [[{'cell_id': j * 9 + i + 55, 'empty':True} for i in range(9)] for j in range(6)]
    warehouse_3 = [[{'cell_id': j * 9 + i + 109, 'empty':True} for i in range(9)] for j in range(6)]
    warehouse_4 = [[{'cell_id': j * 9 + i + 163, 'empty':True} for i in range(9)] for j in range(6)]

    statement = 'SELECT ID, manufacturer, Name, Model, cell, RFID_ID FROM "id_factory" WHERE cell IS NOT Null;'
    db = executeStatement(statement)
    empty_count = 216 - len(db)
    for row in db:
        cell_id = int(row[4])
        if cell_id < 55:
            row_id = cell_id // 9
            col_id = cell_id % 9 - 1
            warehouse_1[row_id][col_id] = create_cell_dict(row)
        elif cell_id < 109:
            row_id = (cell_id - 54) // 9
            col_id = (cell_id - 54) % 9 - 1
            warehouse_2[row_id][col_id] = create_cell_dict(row)
        elif cell_id < 163:
            row_id = (cell_id - 108) // 9
            col_id = (cell_id - 108) % 9 - 1
            warehouse_3[row_id][col_id] = create_cell_dict(row)
        else:
            row_id = (cell_id - 162) // 9
            col_id = (cell_id - 162) % 9 - 1
            warehouse_4[row_id][col_id] = create_cell_dict(row)
        

    return (empty_count, (warehouse_1, warehouse_2, warehouse_3, warehouse_4))

def get_database():
    statement = 'SELECT ID, manufacturer, Name, Model, RFID_ID, cell FROM "id_factory" WHERE cell IS NOT Null;'
    db = executeStatement(statement)
    statement = 'SELECT COUNT(DISTINCT model) FROM id_factory WHERE cell IS NOT Null'
    model_count = executeStatement(statement)
    statement = 'SELECT COUNT(DISTINCT manufacturer) FROM id_factory WHERE cell IS NOT Null'
    manuf_count = executeStatement(statement)
    statement = 'SELECT COUNT(DISTINCT "Date") FROM id_factory WHERE cell IS NOT Null'
    date_count = executeStatement(statement)
    return (model_count[0][0], manuf_count[0][0], date_count[0][0], db)