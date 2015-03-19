########################
# Backup File Python Script for AtomPy 2.1
#
# Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
#
# This will be called every time that a file needs to be backed up.
########################

#Import needed libraries
import time, os, shutil

#Backup function
def backupFile(databaseDIR, backupsDIR, filename):

	#The backup directory will be consisted of the current date and time
	backupFolder = time.strftime("%H_%M_%S_%m_%d_%Y") + '//'
	
	#Check to see if the backup folder exists, and if it doesn't, create it
	if not os.path.exists(databaseDIR + backupsDIR + backupFolder):
		os.makedirs(databaseDIR + backupsDIR + backupFolder)
		
	#Now move the original file from the database to the backup folder
	shutil.move(databaseDIR + filename, databaseDIR + backupsDIR + backupFolder + filename)
	
	#Double-make-sure that the permissions of the file are proper
	os.chmod(databaseDIR + backupsDIR + backupFolder + filename, 0777)