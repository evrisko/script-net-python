#!/usr/bin/env python
import paramiko
import sys
import time
import os
import getpass
import socket
import signal
from datetime import datetime

#parameter
paramiko.util.log_to_file('ssh.log')
path = os.getcwd()
current = datetime.strftime(datetime.now(), "%Y-%m-%d")

#auth
def auth():
	user = raw_input("Username: ")
	passwd = getpass.getpass("Password: ")
	if len(user) == 0 or len(passwd) == 0:
		print "login or password is empty"
		sys.exit()
	return user,passwd

#Validate ip address in file 'ip'
def validate_ip(ip):
	try:
		socket.inet_aton(ip)
		return True
	except:
		print ip
		return False

#ctrl+c
def handler(signal, frame):
        print "exit"
        sys.exit()

#connect ssh
def connect_ssh(host,login,password):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh.connect(host, username = login, password = password)
	except (paramiko.transport.socket.error,paramiko.transport.SSHException,paramiko.transport.socket.timeout,paramiko.auth_handler.AuthenticationException) as error:
		print error
		sys.exit()
	return ssh

#command in console device
def console_command(ssh):
	file = open('command','r')
	console = ssh.invoke_shell()
	for line in file.readlines():
		output = console.send(line)
	time.sleep(5)
	output = console.recv(50000)
	file.close()
	return output


#create result file
def create_file(buffer,host):
	if os.path.exists(path + '/' + host):
		file = open(host+ '/env-' + current,'a')
		file.write(buffer)
		file.close()
	else:
		os.mkdir(path + '/' +  host)
		file = open(host+ '/env-' + current,'a')
		file.write(buffer)
		file.close()

def Main():
	signal.signal(signal.SIGINT, handler)
	user,passwd = auth()
	if os.path.exists(path + '/ip'):
		file = open('ip','r')
		for line in file.readlines():
			if validate_ip(line):
				print "------------------"
				print "Connect to host %s" % line
				ssh = connect_ssh(line,user,passwd)
				print "Execute command"
				output = console_command(ssh)
				print "Create result file"
				line = line.strip('\n')
				create_file(output,line)
				ssh.close()
				print "SSH socket close"
				print "------------------"
			else:
				print "invalid address"
				print "------------------"
	else:
		print "--------------------"
		print "File ip does not exist"
		print "Please, create file ip"
		print "--------------------"

if __name__ == "__main__":
	Main()
