import sqlite3

def executeStatement(statement):
    try:
        # conn = sqlite3.connect(settings.config['db_name'])
        conn = sqlite3.connect('../../sim_data.sqlite')

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
    