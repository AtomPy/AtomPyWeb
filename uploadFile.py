import sys, xlrd, xlwt
import DownloadAPI as API

#First, lets download the file to compare to
drive = API.getDriveService()
filename = sys.argv[2]
fileIndex = -1
wb = None
for x in range(len(fileList)):
	if fileList[x]['title'] == filename:
		fileIndex = x
		break

if fileIndex == -1:
	print "FILE NOT FOUND";
	sys.exit(1)
else:
        file = API.getRawFile(drive, fileList[fileIndex]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'], filename)
        wb1 = xlrd.open_workbook(file_contents=file)

#Now get the workbook from the PHP script
wb2 = xlrd.open_workbook(sys.argv[1])

#And, finally, make our final workbook which will be the
#finished result of this process
wb3 = xlwt.Workbook()

#Cycle through all of the sheets in the original file
for x in range(wb.nsheets):

    #Now grab our sheets
    ws = wb.sheet_by_index(x)
    ws2 = wb2.sheet_by_index(x)
    ws3 = wb3.add_sheet(ws.name)

    #Now we need to compare the indices?
    #Indexs can change? Row insertion?

    #Now begin to go through each and every cell in the worksheet
    #The algorithm is as follows:
    #   First, lets figure out what the indexs will be
    #   9 params for Energy Levels
    #   5 params for A values
    #   5 params for Collisions







    

    
