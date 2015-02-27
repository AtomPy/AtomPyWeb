########################
# ViewFile Python Script for AtomPy 2.1
#
# Created by Josiah Lucas Boswell (www.josiahboswell.com)
#
# Called from a PHP script with two arguments, filename and sheet number.
#
########################

#Import necessary plugins
import openpyxl, os, sys, time, locale, json
locale.setlocale(locale.LC_ALL, '')

#Get filename and sheet number from the PHP script
filename = str(sys.argv[1])
SheetNum = int(sys.argv[2])
BackupArg = int(sys.argv[3])
Backups = json.loads(sys.argv[4])
for i in range(len(Backups)):
	print Backups[i]

#Now open the file and grab the sheet
wb = openpyxl.load_workbook('Database//' + filename)
ws = wb.get_sheet_by_name(wb.get_sheet_names()[SheetNum])

#Get the column widths
column_widths = []
for i in range(len(ws.columns)):
	if ws.column_dimensions[openpyxl.cell.get_column_letter(i+1)].width != None:
		column_widths.append(ws.column_dimensions[openpyxl.cell.get_column_letter(i+1)].width)

#Get the headerRow
headerRow = -1
for i in range(len(ws.rows)):
	if ws.cell(row = i+1, column = 1).value == 'Z':
		headerRow = i-1
		break

#Create our webpage string which will be output to the PHP script
#when we are all done
webpage = ''

#Display what version of the database we are on
webpage += '<br>Current Displaying: '
if BackupArg == '-1':
	webpage += 'Most Recent Version'
else:
	webpage += str(Backups[BackupArg])

#Add the sheet selection table
webpage += '<table style="width:300px"><tr>'
for i in range(len(wb.get_sheet_names())):
	webpage += '<td><form action="viewFile.php" method="post">'
	webpage += '<input type="hidden" name="filename" value=' + str(filename)
	webpage += '><input type="hidden" name="SheetNum" value=' + str(i)
	webpage += '><input type="submit" value="' + wb.get_sheet_by_name(wb.get_sheet_names()[i]).title
	webpage += '"></form></td>'
webpage += '</tr></table><br><br>'

#Debug print
webpage += "Retrieved " + str(len(ws.columns)*len(ws.rows)) + " cells...<br>"

#Display cell data (header and everything)
webpage += '<table>'
for i in range(len(column_widths)):
	webpage += "<col width='" + str(column_widths[i]*10) + "'>"

#Go through all of the cells and do the CSS stylings
for i in range(len(ws.rows)):
	webpage += "<tr>"
	for j in range(len(ws.columns)):
		
		#First, get out current cell (cCell)
		cCell = ws.cell(row = i+1, column = j+1)
		
		#Begin column with text alignment and spanning
		webpage += "<td "
		if i < headerRow-1:
			webpage += " colspan='" + str(len(ws.columns)) + "'"
		webpage += ">"
		
		#Begin creating the css style for this cell
		if cCell.value == '' or cCell.value == None:
			#No styling needed, print out nothing but the row end
			webpage += "</td>"
		else:
			#Add decimals, commas to numbers
			if not (type(cCell.value) is unicode):
				if not (cCell.style.number_format == 'Scientific'):
					cCell.value = locale.format("%.2f", cCell.value, grouping=True)
				else:
					cCell.value = locale.format("%.4E", cCell.value, grouping=True)
			
			#Hyperlink handling
			if type(cCell.value) is unicode:
				if 'HYPERLINK' in cCell.value:
					temp = cCell.value.split('"')
					cCell.value = '<a href="' + temp[1] + '">' + temp[3] + '</a>';
			
			#Print out the cell value
			if type(cCell.value) is unicode:
				cCell.value = cCell.value.replace(u'\xa0','')
			webpage += str(cCell.value)
			
			#End the column
			webpage += "</td>";
		
		#Skip to next row if this cell was a header row
		if i < headerRow:
			break
			
	webpage += "</tr>"

webpage += "</table>"

#Return the webpage to the PHP script
print webpage
