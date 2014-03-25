import sys, xlrd, xlwt, gdata
import DownloadAPI as API

filename = '00_00'

#And, finally, open up our access to the file on the
#database itself
GDClient = API.getGDClient()
q = gdata.spreadsheet.service.DocumentQuery()
feed = GDClient.GetSpreadsheetsFeed(query=q)
counter = 0
while feed.entry[counter].title.text != filename:
        counter = counter + 1
print feed.entry[counter].title.text
workbook_id = feed.entry[counter].id.text.rsplit('/',1)[1]
wsFeed = feed

#Get worksheet ID
feed = GDClient.GetWorksheetsFeed(workbook_id)
worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
print workbook_id
print worksheet_id

worksheet = feed.entry[0]
worksheet.title.text = '42'
GDClient.UpdateWorksheet(worksheet)

#Print out statement for done
print 'DONE'
