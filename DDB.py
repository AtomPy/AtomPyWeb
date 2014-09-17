#Downloads the entire google drive DB to the database folder

						###########
						# WARNING #
						###########

#THIS WILL OVERWRITE ALL FILES NAMED THE SAME IN THE FOLDER
#USE WITH EXTREME CAUTION AND ONLY IF ABSOLUTELY NEEDED
#COULD WIPE OUT LOTS OF DATA!!!

						###########
						# WARNING #
						###########
						
import DownloadAPI as API

print 'Fetching file listing...'
drive = API.getDriveService()
fileList = API.getFileList(drive)
print 'File listing retrieved: '
print len(fileList)
print ' database objects listed...\n\n'

for x in range(len(fileList)):
	filename = fileList[x]['title'] + ".xlsx"
	try:
		print 'Retrieving: ' + filename
		file = API.getRawFile(drive, fileList[x]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'])
		f = open("Database\\" + filename, 'wb')
		f.write(file)
		f.close()
		print 'Downloaded: ' + filename
	except KeyError:
		print 'Skipped (not a file): ' + filename
