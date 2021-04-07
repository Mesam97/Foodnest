import configparser
import pyodbc as db

def connect():
    return db.connect(server = '127.0.0.1',
                        username = 'sa',
                        password = 'A1234567a',
                        database = 'foodnest')

'''server = 'localhost'
username = 'sa'
password = 'A1234567a'
database = 'conference'
connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' +
                        database + ';UID=' + username + ';PWD=' + password)
cursor = connection.cursor() # type: db.Cursor'''