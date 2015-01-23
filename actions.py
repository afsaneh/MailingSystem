import createDB
import sqlite3
from datetime import date, datetime

DB = sqlite3.connect('Mailing.db')
conn = DB.cursor()

loginUsers =[]


while (1):
	action = raw_input("What do you want to do? 1-Register 2-send Message 3-Login 4-Quit \n")
	if (action == '4'):
		break;
	elif (action == '1'):
		# try:
		name = raw_input("name: ")
		family = raw_input("familyName: ")
		userName = raw_input("UserName: ")
		password = raw_input("password: ")
		Log = 0
		conn.execute("INSERT INTO USER (name, familyname, password, UserName, Login) VALUES(?,?,?,?,?)", (name,family, password, userName, Log))
		conn.execute("INSERT INTO ROLE (RoleName,Permission, UserName) VALUES(?,?,?)", ('OrdinaryUser', '0001', userName))
		DB.commit()
		# except Exception as e:
		# 	DB.rollback()
		# 	print "UserName has been taken. Please try again"
		# 	continue
	elif(action == '2'): #send message
		#conn.execute("SELECT userName, Login FROM USER WHERE userName IN loginUsers")
		try:
			reciever = raw_input("Reciever: ")
			subject = raw_input("Subject: ")
			msg = raw_input("Message: ")
			time = datetime.now()
			conn.execute("INSERT INTO MESSAGE(SUBJ, TIMESENT, DELTAG, READTAG, BODY, UID1, UID2) VALUES(?,?,?,?,?,?,?)",\
				(subject,time, 0, 0, msg, 2,reciever))
			DB.commit()
		except Exception as e:
			DB.rollback()
			print "OOPS! Please try again"
			continue

	elif(action =='3'): #login
		uName = raw_input("UserName: ")
		passw = raw_input("Password: ")
		conn.execute("SELECT count(*) FROM USER where UserName = ? and password = ?",(uName, passw))
		unique = conn.fetchone()[0]
		if (unique == 1):
			print "Logged in"
			conn.execute("UPDATE USER SET Login = ? WHERE userName = ?", (1, uName))
			DB.commit()
			loginUsers.append(uName)
		else:
			print "OOPS! Try again!"



DB.commit()

DB.close()