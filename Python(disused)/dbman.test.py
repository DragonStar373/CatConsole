import sqlite3
conn = sqlite3.connect('ConsoleMan/man.db')

c = conn.cursor()
from ConsoleMan.ProgCom import prog_com
c.execute("SELECT * FROM progcom")
print(c.fetchall())
prog_com()