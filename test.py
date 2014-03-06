import DownloadAPI as API
import gdata

GDClient = API.getGDClient()
q = gdata.spreadsheet.service.DocumentQuery()
feed = GDClient.GetSpreadsheetsFeed(query=q)
workbook_id = feed.entry[0].id.text.rsplit('/',1)[1]
feed = GDClient.GetWorksheetsFeed(workbook_id)
worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]

cells = GDClient.GetCellsFeed(workbook_id, worksheet_id)
batchRequest = gdata.spreadsheet.SpreadsheetsCellsFeed()
cells.entry[0].cell.inputValue = str(cells.entry[0].content.text) + ' TESTING'
batchRequest.AddUpdate(cells.entry[0])
GDClient.ExecuteBatch(batchRequest, cells.GetBatchLink().href)
