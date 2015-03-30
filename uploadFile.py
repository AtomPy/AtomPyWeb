########################
# Upload File Python Script for AtomPy 2.1
#
# Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
#
# This program will take the file the user uploaded and the file
# currently in the database and compare the two for data validation. Then
# create a new workbook that copies the original data from the original file,
# and then goes ahead and adds the new data and hyperlinks.
#
# Order of operations: Prune, Validate, Backup, Reconstruct
########################

#Includes
import sys, time, os, shutil
import openpyxl, xlsxwriter
import validateFile, backupFile, pruneFile, reconstructFile

#Get the filename of the file we will be working with
filename = str(sys.argv[1])

#Database, upload, and backup directories
databaseDIR = 'Database//'
uploadDIR = 'Uploads//'
backupDIR = 'Backups//'

#Open up the log file
log = open('log.txt','a')

#Prune both the original and uploaded files
try:
	pruneFile.pruneFile(databaseDIR + filename)
	pruneFile.pruneFile(uploadDIR + filename)
except:
	log.write('FAILED,' + time.strftime("%H_%M_%S_%m_%d_%Y") + ',' + filename + ', Error occured while pruning.')
	log.close()
	sys.exit(1)

#Validate uploaded file against the original one
result = validateFile.validateFile(databaseDIR + filename, uploadDIR + filename)
if 'ERROR' in result:
	log.write('FAILED,' + time.strftime("%H_%M_%S_%m_%d_%Y") + ',' + filename + ',' + result)
	log.close()
	sys.exit(1)

#Backup the original datafile
try:
	backupFile.backupFile(databaseDIR, backupDIR, filename)
except:
	log.write('FAILED,' + time.strftime("%H_%M_%S_%m_%d_%Y") + ',' + filename + ', Error occured while backing up file.')
	log.close()
	sys.exit(1)

#Reconstruct the database file with the new data
try:
	reconstructFile.reconstructFile(databaseDIR + backupDIR + filename, uploadDIR + filename, filename)
except:
	log.write('FAILED,' + time.strftime("%H_%M_%S_%m_%d_%Y") + ',' + filename + ', Error occured while reconstructing file.')
	log.close()
	sys.exit(1)

#Log that everything went alright
log.write('SUCCESS,' + time.strftime("%H_%M_%S_%m_%d_%Y") + ',' + filename + ', No errors.')

#Close log file
log.close()