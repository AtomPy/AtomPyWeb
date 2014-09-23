########################
# AtomPy WebAPI
# Created by Josiah Lucas Boswell (www.josiahboswell.com)
#
# This will be called every time that the upload tool is run
# and has validated a file to replace an existing file in the
# database.
#
# This program will look for the latest backup folder if one
# exists. Once found, it will read in a file called "index.txt". 
# This file is the index of the database at the time that backup
# folder was created. An "image" of the database is thus created
# for various times. The backup program will then go through all
# of the files in the database, comparing their "date modified"
# times against those on record in the index file. All files that
# have a date later than that recorded will be copied into a new
# backup folder with the current date/time. A new index file will
# then be created with the most up to date file times.
########################

#Imports
import sys, time, os, shutil

#Directories we will be working in
databaseDIR = "Database//"
tempDIR = "TempFIles//"
backupDIR = "Backups//"

#Get a listing of all the backup folders
backupFolders = os.listdir(backupDIR)

#Create an array of files to back
filesToBackup = []

#Get a listing of all the files currently in the database
databaseFiles = os.listdir(databaseDIR)

#Create an array of strings to be written out at the end of
#the backup
logFile = []

#Is this the first backup? If so, backup everything
if len(backupFolders) == 0:
	filesToBackup = databaseFiles
	logFile.append('First backup, everything backed up!')
else:
	#Figure out which backup was the latest
	lastBackup = 0
	for i in range(len(backupFolders)):
		if backupFolders[i] > backupFolders[lastBackup]:
			lastBackup = i
			
	#Now open the index file of the latest backup, read in the
	#backup information, and close the index file
	f = open(backupDIR + backupFolders[lastBackup] + '//index.txt','rb')
	refs = f.readlines()
	f.close()
		
	#Bug fix: newlines create issues
	for i in range(len(refs)):
		refs[i] = refs[i].replace('\r\n','')

	#Now we will go through all of the files in the database
	for dataFile in databaseFiles:
			
			#Attempt to find the index of this file in the r
			cIndex = -1
			for i in range(len(refs)):
				if refs[i].split(',')[0] == dataFile:
					cIndex = i
					break
					
			#Case 1: cIndex is still -1, meaning this file is new
			if cIndex == -1:
				filesToBackup.append(dataFile)
				logFile.append('New File:\t' + dataFile)
				#print 'New File:\t' + dataFile
				
			#Case 2: cIndex is not -1, so it exists in the database
			else:
				
				#Case 3: cIndex is not -1 AND the file has changed
				if time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(os.path.getmtime(databaseDIR + dataFile))) > refs[i].split(',')[1]:
					filesToBackup.append(dataFile)
					logFile.append('Mod File:\t' + dataFile)
					#print 'Mod File:\t' + dataFile
				else:
					#Nothing needs to be done
					i = i
					#print 'Old File:\t' + dataFile

#Now perform the backup (if any needed)
if len(filesToBackup) > 0:
	
	#Create the backup folder
	backupFolder = backupDIR + time.strftime("%Y-%m-%dT%H-%M-%S")
	os.makedirs(backupFolder)

	#Copy any modified files to the new backup folder
	for fileToBackup in filesToBackup:
		shutil.copy2(databaseDIR + fileToBackup, backupFolder + '//' + fileToBackup)
		
	#Save a new index file to the new backup folder
	f = open(backupFolder + '//index.txt', 'wb')
	for dataFile in databaseFiles:
		modifiedDate = time.strftime("%Y-%m-%dT%H-%M-%S", time.localtime(os.path.getmtime(databaseDIR + dataFile)))
		f.write(dataFile + ',' + modifiedDate + '\r\n')
	f.close()
	
	#Save the log file to the new backup folder
	f = open(backupFolder + '//log.txt','wb')
	for log in logFile:
		f.write(log + '\r\n')
	f.close()
