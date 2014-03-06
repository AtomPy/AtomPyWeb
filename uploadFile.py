import sys, xlrd, xlwt, gdata
import DownloadAPI as API

#First, lets download the file to compare to
drive = API.getDriveService()
fileList = API.getFileList(drive)
filename = sys.argv[2][:-5]

fileIndex = -1
wb1 = None
for x in range(len(fileList)):
	if fileList[x]['title'] == filename:
		fileIndex = x
		break
if fileIndex == -1:
	print "FILE NOT FOUND";
	sys.exit(1)
else:
        file = API.getRawFile(drive, fileList[fileIndex]['exportLinks']['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'])
        wb1 = xlrd.open_workbook(file_contents=file)

#Now get the workbook from the PHP script
wb2 = xlrd.open_workbook(sys.argv[1])

#And, finally, open up our access to the file on the
#database itself
GDClient = API.getGDClient()
q = gdata.spreadsheet.service.DocumentQuery()
feed = GDClient.GetSpreadsheetsFeed(query=q)
workbook_id = feed.entry[fileIndex].id.text.rsplit('/',1)[1]
print feed.entry[fileIndex].title.text
feed = GDClient.GetWorksheetsFeed(workbook_id)

#Cycle through all of the sheets in the original file
for x in range(wb1.nsheets):

	#Now grab our sheets
	ws1 = wb1.sheet_by_index(x)
	ws2 = wb2.sheet_by_index(x)

	#Alter size and begin batch request
	worksheet = feed.entry[x]
	worksheet.Cols = ws2.ncols
	print ws2.ncols
	worksheet.Update()
	'''worksheet_id = feed.entry[x].id.text.rsplit('/',1)[1]
	cells = GDClient.GetCellsFeed(workbook_id, worksheet_id)
	batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()

	#Now we need to compare the indices?
	#Indexs can change? Row insertion?
	#Will do in later version

	#Find out where the new data begins
	colsStart = ws1.ncols+1

	#Now begin adding data
	for x in range(ws2.ncols):
		if x >= colsStart:
			#Now we are at the correct column, so
			#start cycling through the rows
			for y in range(ws1.nrows):
				inputValue = ws2.cell_value(y+1, x+1)
				cells.entry[x + (y*ws2.ncols)].cell.inputValue = inputValue
				batchRequest.AddUpdate(cells.entry[x + (y*ws2.ncols)])
				
	#Send the batch request
	GDClient.ExecuteBatch(batchRequest, cells.GetBatchLink().href)'''
        


    

    
