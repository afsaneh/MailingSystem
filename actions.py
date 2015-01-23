import createDB
import sqlite3
import os.path
from datetime import date, datetime

DB = sqlite3.connect('Mailing.db')
conn = DB.cursor()


def firstActions():
	while (1):
		action = raw_input("What do you want to do? 1-Register 2-Login 3-Quit \n")
		if (action == '3'):
			break
		elif (action == '1'): #register
			try:
				name = raw_input("name: ")
				family = raw_input("familyName: ")
				userName = raw_input("UserName: ")
				password = raw_input("password: ")
				Log = 0
				conn.execute("INSERT INTO USER (name, familyname, password, UserName, Login) VALUES(?,?,?,?,?)", (name,family, password, userName, Log))
				conn.execute("INSERT INTO ROLE (RoleName,Permission, UserName) VALUES(?,?,?)", ('OrdinaryUser', '0001', userName))
				DB.commit()
			except Exception as e:
				DB.rollback()
				print "UserName has been taken. Please try again"
				continue

		elif(action =='2'): #login
			# try:
			uName = raw_input("UserName: ")
			passw = raw_input("Password: ")
			conn.execute("SELECT count(*) FROM USER where UserName = ? and password = ?",(uName, passw))
			unique = conn.fetchone()[0]
			if (unique == 1):
				print "Logged in\n"
				conn.execute("UPDATE USER SET Login = ? WHERE userName = ?", (1, uName))
				DB.commit()
				#LoggedUser = uName
				afterLogin(uName)
			else:
				print "OOPS! Try again!\n"

			# except Exception as e:     DB.rollback()     print "Try again!
			# --Login error"     continue


def afterLogin(userName):
	while (1):
		action = raw_input("What do you want to do? 1-send Message 2-Inbox 3-Sent 4-Trash 5-Delete msg 6-Logout\n")

		if(action == '1'): #send message
			conn.execute("SELECT count(*) FROM USER where UserName = ? and Login = ?",(userName, 1))
			unique = conn.fetchone()[0]
			if (unique == 1):
				#try:
				reciever = raw_input("Reciever: ")
				conn.execute("SELECT count(*) FROM USER where UserName = ?",(reciever,))
				unique = conn.fetchone()[0]
				if (unique == 1):
					subject = raw_input("Subject: ")
					msg = raw_input("Message: ")
					time = datetime.now()
					conn.execute("INSERT INTO MESSAGE(SUBJ, TIMESENT, DELTAG, READTAG, BODY, UID1, UID2) VALUES(?,?,?,?,?,?,?)",\
						(subject,time, 0, 0, msg, userName,reciever))
					updateAttachTable(userName, conn.lastrowid)
					DB.commit()
				else:
					print "UserName is not valid. Try again"
					continue
				# except Exception as e:
				# 	DB.rollback()
				# 	print "OOPS! Please try again --sending error\n"
				# 	continue
			else:
				print "You should log in to the system first!\n"

		elif (action == '2'): #Show Inbox
			conn.execute("SELECT * from INBOX where UID2 = ? and DELTAG = ?", (userName, 0))
			allmsg = conn.fetchall()
			for msg in allmsg:
				print 'num: {0}, From: {1}, Subject: {2}, Body: {3}, On: {4}, Read: {5} '.format(msg[0], msg[5], msg[1], msg[4], msg[2], msg[3])
				print "\n"
				conn.execute("SELECT FileContent, fileName from ATTACHMENT where MsgKEY = ?", (msg[0],))
				allAttach = conn.fetchall()
				for attach in allAttach:
					with open(attach[1], "wb") as output_file:
						output_file.write(attach[0])


		elif (action == '3'): #Show Sent
			conn.execute("SELECT * from SENT where UID1 = ? and DELTAG = ?", (userName, 0))
			allmsg = conn.fetchall()
			for msg in allmsg:
				print 'num: {0}, To: {1}, Subject: {2}, Body: {3}, On: {4}, '.format(msg[0], msg[5] ,msg[1], msg[3], msg[2])
				print "\n"

		elif (action == '4'): #Show Trash
			conn.execute("SELECT * from TRASH where UID1 = ? and DELTAG = 1", (userName,))
			allmsg = conn.fetchall()
			for msg in allmsg:
				print 'num: {0}, To: {1}, Subject: {2}, Body: {3}, On: {4}, '.format(msg[0], msg[5] ,msg[1], msg[3], msg[2])
				print "\n"

		elif (action == '5'): #Delete msg from inbox
			conn.execute("SELECT * from MESSAGE where UID2 = ?", (userName,)) #delete from inbox	
			delmsg = raw_input("please enter the msg number: ")
			conn.execute("UPDATE MESSAGE SET DELTAG = ? WHERE MKEY = ?", (1, delmsg))
			DB.commit()


		elif (action == '6'): #logout
			try:
				conn.execute("UPDATE USER SET Login = ? WHERE userName = ?", (0, userName))
				DB.commit()
				print "Successfully Logged Out!\n"
				break
				#LoggedUser = ''
			except Exception as e:
				DB.rollback()
				print "Try again! --Logout error"
				continue

def updateAttachTable(userName, lastrowid):
	attachment = raw_input("Do you want to attach a file? Y/N\n")
	while (attachment == 'y' or attachment == 'Y'):
		path = raw_input("Enter file path: ")
		name = os.path.split(path)
		with open(path, "rb") as att:
			ablob = att.read()
			conn.execute("INSERT INTO ATTACHMENT (FileName, FileContent, MsgKEY) VALUES(?, ?, ?)",\
				(name[1], sqlite3.Binary(ablob),lastrowid))
			DB.commit()
		attachment = raw_input("Do you want to attach another file? Y/N\n")



firstActions()

DB.close()