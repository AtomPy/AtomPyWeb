########################
# BackupBoy.py for AtomPy 2.1
#
# Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
#
# This will be called every time that the upload tool is run
# and has validated a file to replace an existing file in the
# database.
########################

#Imports
import sys, time, os, shutil

#Get our args
filename = sys.argv[1]
filelocation = sys.argv[2]

#Directories we will be working in
databaseDIR = "Database//"
backupDIR = "Database//Backups//"

#Create the backup folder
backupFolder = backupDIR + time.strftime("%Y-%m-%dT%H-%M-%S")
os.makedirs(backupFolder)

#Copy from the database to the backup folder
shutil.copy2(databaseDIR + filename, backupFolder + '//' + filename)

#Copy from the temp location to the database
shutil.copy2(filelocation, databaseDIR + filename)