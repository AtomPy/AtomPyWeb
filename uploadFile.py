import sys, xlrd, xlwt, gdata
import DownloadAPI as API
import tempfile, os

try:
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

        #We now have the original and altered workbooks
        #Create a third, new workbook for storing the merged data
        wb3 = xlwt.Workbook()
        categoryLine = -1

        # ERROR CHECK: Make sure that the original and altered
        #              workbooks have the same number of sheets
        if wb1.nsheets != wb2.nsheets:
                print 'ERROR: Number of sheets not equal.<br>'
                print 'Please re-download source document and re-apply alterations.<br>'
                sys.exit(1)

        #Cycle through all of the sheets in the original file
        #(The altered file SHOULD have the same number of sheets)
        for x in range(wb1.nsheets):

                #Now grab our sheets
                ws1 = wb1.sheet_by_index(x)
                ws2 = wb2.sheet_by_index(x)

                # ERROR CHECK: Make sure that the altered worksheet
                #              has more than the original worksheet
                #              in terms of columns and rows
                if ws2.ncols < ws1.ncols:
                        print 'ERROR: Number of columns not greater than or equal to original data columns.<br>'
                        print 'Please re-download source document and re-apply alterations.<br>'
                        sys.exit(1)
                if ws2.nrows < ws1.nrows:
                        print 'ERROR: Number of rows not greater than or equal to original data rows.<br>'
                        print 'Please re-download source document and re-apply alterations.<br>'
                        sys.exit(1)

                #Create our new sheet
                ws3 = wb3.add_sheet(ws1.name)

                #Cycle through all of the rows in the altered workbook
                #And append any new rows
                offset = 0
                for row in range(ws2.nrows):

                        #Figure out if the row is original or not
                        if row < ws1.nrows:
                                #Go through each col (original size)
                                altered = False
                                for col in range(ws1.ncols):
                                        if(ws1.cell(row-offset, col).value != ws2.cell(row, col).value):
                                                altered = True
                                                break
                                        
                                #Write the correct info
                                if altered:
                                        for col in range(ws1.ncols):
                                                ws3.write(row, col, ws2.cell(row, col).value)
                                        offset = offset + 1
                                else:
                                        for col in range(ws1.ncols):
                                                ws3.write(row, col, ws1.cell(row-offset, col).value)
                        else:
                                for col in range(ws1.ncols):
                                        ws3.write(row, col, ws2.cell(row, col).value)

                        #While we are here, get the category line
                        if categoryLine == -1 and ws2.cell(row, 0).value == 'Z':
                                categoryLine = row
                
                #Go through all the columns in the altered workbook
                #And append any new columns
                for col in range(ws2.ncols):
                        if col > ws1.ncols-1:
                                for row in range(ws2.nrows):
                                        ws3.write(row, col, ws2.cell(row, col).value)

        #Convert our xlwt workbook to a xlrd workbook, then delete the temp file
        temp = tempfile.NamedTemporaryFile(dir='TempFiles\\',suffix='.xls',delete=False)
        temp.close()
        wb3.save(temp.name)
        wb3 = xlrd.open_workbook(temp.name)
        os.remove(temp.name)

        #And, finally, open up our access to the file on the
        #database itself
        GDClient = API.getGDClient()
        q = gdata.spreadsheet.service.DocumentQuery()
        feed = GDClient.GetSpreadsheetsFeed(query=q)
        counter = 0
        while feed.entry[counter].title.text != filename:
                counter = counter + 1
        workbook_id = feed.entry[counter].id.text.rsplit('/',1)[1]
        wsfeed = GDClient.GetWorksheetsFeed(workbook_id)

        #Go through all of the worksheets
        for sheet in range(wb1.nsheets):

                #Get our worksheet
                ws3 = wb3.sheet_by_index(sheet)

                #Get worksheet ID and alter worksheet size
                worksheet_id = wsfeed.entry[x].id.text.rsplit('/',1)[1]
                wsfeed.entry[x].col_count.text = str(ws3.ncols)
                wsfeed.entry[x].row_count.text = str(ws3.nrows)
                GDClient.UpdateWorksheet(wsfeed.entry[x])
                
                #Get our cell feed and batch request ready
                query = gdata.spreadsheet.service.CellQuery()
                query['return-empty'] = "true"
                cells = GDClient.GetCellsFeed(workbook_id, worksheet_id, query=query)
                batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()

                #Append any new title columns
                for col in range(ws3.ncols):
                        if col > ws1.ncols - 1:
                                row = categoryLine
                                cells.entry[col + (row*ws3.ncols)].cell.inputValue = str(ws3.cell(row, col).value)
                                batchRequest.AddUpdate(cells.entry[col + (row*ws3.ncols)])
                
                #Go through all of our rows AFTER the category title (to retain formatting info)
                for row in range(ws3.nrows):
                        if row > categoryLine:

                                #Go through all the columns, updating the cells as we go
                                for col in range(ws3.ncols):
                                        cells.entry[col + (row*ws3.ncols)].cell.inputValue = str(ws3.cell(row, col).value)
                                        batchRequest.AddUpdate(cells.entry[col + (row*ws3.ncols)])

                #Execute our batch request
                GDClient.ExecuteBatch(batchRequest, cells.GetBatchLink().href)

        print 'File upload completed.'

except Exception,e:
        print 'Unfortunately, an unforseen error occured:<br>'
        print str(e)




    

    
