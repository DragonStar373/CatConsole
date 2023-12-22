import sqlite3
conn = sqlite3.connect('man.db')

c = conn.cursor()
from ProgCom import prog_com
prog_com()