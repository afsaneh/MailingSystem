import sqlite3

DB = sqlite3.connect('Mailing.db')
conn = DB.cursor()
print "Opened DataBase successfully"


conn.execute('''CREATE TABLE if not exists USER
	(Name TEXT NOT NULL,
	FamilyName TEXT NOT NULL,
	UserName char(10) PRIMARY KEY,
	password char(10) NOT NULL,
	login bit NOT NULL);''')

#(UID INTEGER PRIMARY KEY AUTOINCREMENT,

conn.execute('''CREATE TABLE if not exists ROLE
	(RoleName TEXT NOT NULL,
	Permission bit(4) NOT NULL,
	UserName INT NOT NULL,
	FOREIGN KEY (UserName) REFERENCES USER(UserName));''')

conn.execute('''CREATE TABLE if not exists MESSAGE
	(MKEY INTEGER PRIMARY KEY AUTOINCREMENT,
	SUBJ TEXT NOT NULL,
	TIMESENT timestamp NOT NULL,
	DELTAG bit NOT NULL,
	READTAG bit NOT NULL,
	BODY TEXT,
	UID1 INT NOT NULL,
	UID2 INT NOT NULL);''')


conn.execute('''CREATE TABLE if not exists ATTACHMENT
	(Attkey INTEGER PRIMARY KEY AUTOINCREMENT,
	FileName TEXT NOT NULl,
	FileContent TEXT);''')

conn.execute('''CREATE VIEW if not exists INBOX AS
	select MKEY, SUBJ, TIMESENT, READTAG, BODY, UID1, UID2, DELTAG
	from MESSAGE;''')

conn.execute('''CREATE VIEW if not exists SENT AS
	select MKEY, SUBJ, TIMESENT, BODY, UID1, UID2, DELTAG
	from MESSAGE;''')

conn.execute('''CREATE VIEW if not exists TRASH AS
	select MKEY, SUBJ, BODY, DELTAG, UID1, UID2
	from MESSAGE;''')

print "TableS created successfully"


DB.commit()
DB.close()