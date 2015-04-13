########################
# Prune File Python Script for AtomPy 2.1
#
# Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
#
# Takes a file and removes all the empty rows and columns for better memory management.
# Since we are using xlsxwriter so that we can maintain our hyperlinks, then create the new
# file with the old filename so that it is overwritten. No data is lost in this process.
#
# Initial tests show that it will save 40% of data space from eliminating empty rows/cols.
########################

#Include needed libraries
import xlsxwriter, openpyxl, sys, os

def pruneFile(filename):

	#Open the original workbook
	wb_original = openpyxl.load_workbook(filename)

	#Open up the new workbook
	wb_new = xlsxwriter.Workbook(filename)

	#Add the url formatting for the new workbook (xlsx formatting)
	url_format = wb_new.add_format({
		'font_color': 'blue',
		'underline':  1
	})
	url_format.set_font_name('Arial')
	url_format.set_font_size(10)
	
	#Header formatting (just bold)
	header_format = wb_new.add_format()
	header_format.set_bold()
	header_format.set_font_name('Arial')
	header_format.set_font_size(10)
	
	#Category row / Source Row formatting (lgith gray background)
	category_format = wb_new.add_format()
	category_format.set_bg_color('#D3D3D3')
	category_format.set_font_name('Arial')
	category_format.set_font_size(10)
	
	#Regular formatting (size/font)
	regular_format = wb_new.add_format()
	regular_format.set_font_name('Arial')
	regular_format.set_font_size(10)

	#Go through the original original worksheets
	for i in range(len(wb_original.worksheets)):

		#Get the current sheet from the original workbook
		ws_original = wb_original.get_sheet_by_name(wb_original.get_sheet_names()[i])
		
		#Now create the new worksheet and title it with the original workbook title
		ws_new = wb_new.add_worksheet(wb_original.get_sheet_names()[i])
		print 'Pruning sheet: ' + wb_original.get_sheet_names()[i]
		
		#Adjust widths
		adjustedWidths = []
		for j in range(len(ws_original.columns)):
			adjustedWidths.append(0)
				
		#Find the category line (validation bot makes sure that it is the same for both the original and uploaded workbooks)
		categoryLine = -1
		for j in range(len (ws_original.rows)):
			if ws_original.cell(row=j+1, column=1).value == 'Z':
				categoryLine = j
				break
				
		#Now find the beginning of the data columns, each data column has a source box above it
		#The source is denoted as follows: S##
		dataColumn = -1
		for j in range(len(ws_original.columns)):
			if ws_original.cell(row=categoryLine+1-1, column=j+1).value != None:
				if 'S' in ws_original.cell(row=categoryLine+1-1, column=j+1).value:
					dataColumn = j+1
					break
		dataColumn = dataColumn - 1
		
		#Prune empty rows
		emptyRowStart = -1
		for j in range(len(ws_original.rows)):
			empty = True
			for k in range(len(ws_original.columns)):
				cValue = ws_original.cell(row=j+1, column=k+1).value
				try:
					cValue = str(cValue)
				except:
					cValue.replace(u'\xa0', u' ')
					
				if cValue != 'None':
					empty = False
			if empty == True:
				emptyRowStart = j
				break
		if emptyRowStart == -1:
			emptyRowStart = len(ws_original.rows)
		
		#Prune empty columns
		emptyColStart = -1
		for j in range(len(ws_original.columns)):
			empty = True
			for k in range(len(ws_original.rows)):
				cValue = ws_original.cell(row=k+1, column=j+1).value
				try:
					cValue = str(cValue)
				except:
					cValue.replace(u'\xa0', u' ')
					
				if cValue != 'None':
					empty = False
			if empty == True:
				emptyColStart = j
				break
		if emptyColStart == -1:
			emptyColStart = len(ws_original.columns)
		
		#Go through the rows in the original workbook
		for j in range(emptyRowStart):
		
			#Go through the columns in the original workbook
			for k in range(emptyColStart):
			
				#Get current cell value
				cValue = ws_original.cell(row=j+1, column=k+1).value
				
				#Make a backup of the cValue and then convert to string
				backup_cValue = cValue
				try:
					cValue = str(cValue)
					if cValue == 'None':
						cValue = ''
				except:
					cValue.replace(u'\xa0', u' ')
					
				#Double-check width and adjust if required
				if 'HYPERLINK' not in cValue:
					if j != 0 and adjustedWidths[k] < len(cValue) + 1:
						adjustedWidths[k] = len(cValue) + 1
						ws_new.set_column(k, k, len(cValue)+1)
				else:
					if j != 0 and adjustedWidths[k] < len(cValue.split('","')[1].split('")')[0]) + 1:
						adjustedWidths[k] = len(cValue.split('","')[1].split('")')[0]) + 1
						ws_new.set_column(k, k, len(cValue.split('","')[1].split('")')[0])+1)
					
				#Formula filled cells auto to 15 width
				if j > 2 and '=' in cValue:
					ws_new.set_column(k, k, 15)
				
				#Header row will be merged throughout
				if j == 0 and k == 0:
					ws_new.merge_range(0, 0, 0, emptyColStart-1, cValue, header_format)
					
				#Category row and source row
				if j > 0 and j <= 2:
					ws_new.write(j, k, cValue, category_format)
					
				#Key Cells (keep original formatting, so numbers and such)
				if j > 2 and k < dataColumn:
					ws_new.write(j, k, backup_cValue, regular_format)
					
				#Data Cells with hyperlinks
				if j > 2 and k >= dataColumn:
				
					if 'HYPERLINK' not in cValue:	
						ws_new.write(j, k, cValue, regular_format)
					else:
						ws_new.write(j, k, cValue, url_format, cValue.split('","')[1].split('")')[0])
		
	#Close the workbook
	wb_new.close()
	
	print 'Pruned: ' + filename