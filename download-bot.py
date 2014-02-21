import DownloadAPI as API
import sys, time

#Get our PHP args
Z = -1
N = -1
try:
	Z = sys.argv[1]
	N = sys.argv[2]
except:
	print "ERROR"
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

#Get our file
drive = API.getDriveService()
fileList = API.getFileList(drive)

fileIndex = -1
for x in range(len(fileList)):
	if fileList[x]['title'] == filename:
		fileIndex = x
		break

if fileIndex == -1:
	print "FILE NOT FOUND";
	sys.exit(1)
else:
        filename = filename + ".xlsx"
        file = API.getRawFile(drive, fileList[fileIndex]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'])
        f = open("TempFiles\\" + filename, 'wb')
        f.write(file)
        f.close()
        print filename
