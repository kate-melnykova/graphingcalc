from collections import namedtuple
import sqlite3

User = namedtuple('User', ['name', 'email', 'password'])

conn = sqlite3.connect('test.db')
cur = conn.cursor()

for row in cur.execute('SELECT * from users'):
    print(User(*row).name)
