import sqlite3
db = 'ChatDeVoz'
table = db

def insert_sql(sql):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	cursor.execute(sql)
	conn.commit()
	conn.close()

def voice_started(groupid, messageid):
	insert_sql(f"""INSERT INTO Chats_de_Voz (groupid, messageid)
		VALUES ('{groupid}', '{messageid}')""")
	
def voice_ended(groupid):
	insert_sql(f"""DELETE FROM Chats_de_Voz 
		WHERE id = {groupid}""")

def create_group_table(groupid):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	cursor.execute(f"""CREATE TABLE {groupid} (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		userid TEXT);""")

def select_info(table, col, arg):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	aux = (f'''SELECT * FROM {table} WHERE
	   {col} ="{arg}"''')
	cursor.execute(aux)
	data = cursor.fetchone()
	conn.close()
	return data

def select_all(table):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	aux = (f'''SELECT userid FROM {table}''')
	cursor.execute(aux)
	data = cursor.fetchall()
	conn.close()
	return data

def add_group(groupid, adminid, pinid):
	insert_sql(f"""INSERT INTO {table} (groupid, adminid, pinid)
		VALUES ('{groupid}', '{adminid}', '{pinid}')""")

def add_sub(groupid, userid):
	insert_sql(f"""INSERT INTO {(groupid)} (userid)
		VALUES ('{userid}')""")

def del_sub(groupid, userid):
	insert_sql(f"""DELETE FROM {(groupid)}
		WHERE userid = {userid}""")

def del_group(table, groupid): 
	insert_sql(f"""DELETE FROM {table}
		WHERE groupid = {groupid}""")
