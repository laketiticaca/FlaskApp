import MySQLdb

def connection():
    conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '1fPigzc0u1d', db = 'classlist')
    c = conn.cursor()

    return c, conn