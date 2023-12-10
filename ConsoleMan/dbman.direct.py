import sqlite3
conn = sqlite3.connect('man.db')

c = conn.cursor()
c.execute("""CREATE TABLE progcom (
			primarycommand TEXT,
			location TEXT,
			function TEXT,
			help TEXT
			secondarycommands TEXT
	)""")

conn.commit()