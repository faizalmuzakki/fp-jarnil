import sys
import os
import uuid
import datetime

class Chat:
	def __init__(self):
		self.sessions={}
		self.users = {}
		self.users['messi']={'nama': 'Lionel Messi', 'negara': 'Argentina', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
		self.users['henderson']={'nama': 'Jordan Henderson', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
		self.users['lineker']={'nama': 'Gary Lineker', 'negara': 'Inggris', 'password': 'surabaya','incoming': {}, 'outgoing':{}}
	
	def proses(self, data):
		j = data.decode().split(" ")
		try:
			command=j[0].strip()
			if (command == 'auth'):
				username=j[1].strip()
				password=j[2].strip()
				print("auth {}" . format(username))

				return self.autentikasi_user(username,password)

			elif (command=='send'):
				del j[3]
				sessionid = j[1].strip()
				usernameto = j[2].strip()
				message = ""

				for w in j[3:-2]:
					message = "{} {}" . format(message, w)

				lifetime = 0
				try:
					lifetime = int(j[-2])
				except ValueError:
					return {'status': 'ERROR', 'message': '**Lifetime bukan angka'}
				
				usernamefrom = self.sessions[sessionid]['username']
				print("send message from {} to {}" . format(usernamefrom, usernameto))
				
				return self.send_message(sessionid, usernamefrom, usernameto, message, lifetime)
			
			elif (command=='inbox'):
				sessionid = j[1].strip()
				username = self.sessions[sessionid]['username']
				print("inbox {}" . format(sessionid))
				
				return self.get_inbox(username)

			else:
				return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
		
		except IndexError:
			return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}
	
	def autentikasi_user(self,username,password):
		if (username not in self.users):
			return {'status': 'ERROR', 'message': 'User Tidak Ada'}
 		
		if (self.users[username]['password'] != password):
			return {'status': 'ERROR', 'message': 'Password Salah'}
		
		tokenid = str(uuid.uuid4()) 
		self.sessions[tokenid] = {'username': username, 'userdetail':self.users[username]}
		
		return {'status': 'OK', 'tokenid': tokenid}
	
	def get_user(self,username):
		if (username not in self.users):
			return False
		
		return self.users[username]
	
	def send_message(self, sessionid, username_from, username_dest, message, lifetime):
		if (sessionid not in self.sessions):
			return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
		
		s_fr = self.get_user(username_from)
		s_to = self.get_user(username_dest)
		
		if (s_fr==False or s_to==False):
			return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

		expired_at = datetime.datetime.now() + datetime.timedelta(0, lifetime)
		message = {'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message, 'expired_at': expired_at}
		outqueue_sender = s_fr['outgoing']
		inqueue_receiver = s_to['incoming']
		
		try:	
			outqueue_sender[username_from].append(message)
		except KeyError:
			outqueue_sender[username_from] = []
			outqueue_sender[username_from].append(message)
		
		try:
			inqueue_receiver[username_from].append(message)
		except KeyError or TypeError:
			inqueue_receiver[username_from] = []
			inqueue_receiver[username_from].append(message)
		
		return {'status': 'OK', 'message': 'Message Sent'}

	def get_inbox(self,username):
		s_fr = self.get_user(username)
		incoming = s_fr['incoming']
		msgs={}
		for users in incoming:
			msgs[users]=[]
			
			if(len(incoming[users]) != 0):
				# sentinel = object()
				for item in incoming[users]:
					if(item['expired_at'] > datetime.datetime.now()):
						msgs[users].append(item)
			
		s_fr['incoming'] = {}
		return {'status': 'OK', 'messages': msgs}

if __name__=="__main__":
	j = Chat()
	sesi = j.proses("auth messi surabaya")
	print(sesi)
	tokenid = sesi['tokenid']
	print(j.proses("send {} henderson hello gimana kabarnya son " . format(tokenid)))
	print(j.get_inbox('messi'))
















