import configparser

def connect():
    return db.connect(server = '127.0.0.1',
                        username = 'sa',
                        password = 'A1234567a',
                        database = 'foodnest')