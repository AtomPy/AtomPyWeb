########################
# Download Bot Python Script for AtomPy 2.0
# Created by Josiah Lucas Boswell (www.josiahboswell.com)
# 
# Takes arguments for the file that the user wants,
# searches the Google Drive Database for it, and then
# returns it to the PHP script.
########################

import DownloadAPI as API
import sys, time, os.path

#Get our PHP args
Z = -1
N = -1
database = ""
try:
	Z = sys.argv[1]
	N = sys.argv[2]
	database = str(sys.argv[3])
except:
	print "ERROR: INCORRECT ARGS"
	sys.exit(1)

#Build our filename
filename = ''
if len(Z) == 1:
	filename = filename + '0' + Z
else:
	filename = filename + Z
filename = filename + '_'
if len(N) == 1:
	filename = filename + '0' + N
else:
	filename = filename + N

if database == 'google':
	#Get our file
	drive = API.getDriveService()
	fileList = API.getFileList(drive)

	fileIndex = -1
	for x in range(len(fileList)):
		if fileList[x]['title'] == filename:
			fileIndex = x
			break

	if fileIndex == -1:
		print "ERROR: FILE NOT FOUND IN GOOGLE DRIVE DATABASE"
		sys.exit(1)
	else:
			filename = filename + ".xlsx"
			file = API.getRawFile(drive, fileList[fileIndex]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'])
			f = open("TempFiles//" + filename, 'wb')
			f.write(file)
			f.close()
			print filename

else:
	if database == 'atompy':

		filename = filename + ".xlsx"
		if os.path.isfile("Database//" + filename):
			print filename
		else:
			print "ERROR: FILE NOT FOUND IN ATOMPY DATABASE"
			sys.exit(1)
		
	else:
		print "ERROR: INCORRECT DATABASE VALUE"
		sys.exit(1)
