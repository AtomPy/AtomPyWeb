########################
# Reconstruct File Python Script for AtomPy 2.1
#
# Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
#
# Takes two files: the original and pre-backed-up file, and the new uploaded file.
# It then creates a new file, taking the original data and building it first, then taking
# the new data and appending it to the original data. Hyperlinks are also constructed
# in here aswell. Third argument is the location/name of the new reconstructed data
# file.
########################

#Include needed libraries
import xlsxwriter, openpyxl, sys

def reconstructFile(original_backedup_filename, uploaded_filename, new_filename):

	#Open the original backed up workbook
	wb_original = openpyxl.load_workbook(original_backedup_filename)
	workbook_name = original_backedup_filename.split('\\')[len(original_backedup_filename.split('\\'))-1]
	
	#Open the uploaded workbook
	wb_uploaded = openpyxl.load_workbook(uploaded_filename)

	#Open up the new workbook
	wb_new = xlsxwriter.Workbook(new_filename)

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

	#Go through the original, backed-up workbook
	for i in range(len(wb_original.worksheets)):

		#Get the current sheet from the original and uploaded workbooks
		ws_original = wb_original.get_sheet_by_name(wb_original.get_sheet_names()[i])
		ws_uploaded = wb_uploaded.get_sheet_by_name(wb_uploaded.get_sheet_names()[i])
		
		#Now create the new worksheet and title it with the original workbook title
		ws_new = wb_new.add_worksheet(wb_original.get_sheet_names()[i])
		
		#Adjust widths
		adjustedWidths = []
		for j in range(len(ws_uploaded.columns)):
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
		
		#Go through the rows in the original workbook
		for j in range(len(ws_original.rows)):
		
			#Go through the columns in the original workbook
			for k in range(len(ws_original.columns)):
			
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
				if j != 0 and adjustedWidths[k] < len(cValue) + 1:
					adjustedWidths[k] = len(cValue) + 1
					ws_new.set_column(k, k, len(cValue)+1)
				
				#Formula filled cells auto to 100 width
				if j > 2 and '=' in cValue:
					ws_new.set_column(k, k, 15)
				
				#Header row will be merged throughout
				if j == 0 and k == 0:
					ws_new.merge_range(0, 0, 0, len(ws_original.columns)-1, cValue, header_format)
					
				#Category row and source row
				if j > 0 and j <= 2:
					ws_new.write(j, k, cValue, category_format)
					
				#Key Cells (keep original formatting, so numbers and such)
				if j > 2 and k < dataColumn:
					ws_new.write(j, k, backup_cValue, regular_format)
					
				#Data Cells with hyperlinks
				if j > 2 and k >= dataColumn:
				
					#Grab the source ID from the source box above the data column  
					try:
						sourceID = str(ws_original.cell(row=categoryLine-1+1, column=k+1).value).split('S')[1]
					except:
						sourceID = str(1)
					
					if 'HYPERLINK' not in cValue:	
						ws_new.write(j, k,'=HYPERLINK("http://141.218.60.56/~jnz1568/getInfo.php?workbook=' + workbook_name + '&sheet=' + wb_original.get_sheet_names()[i] + '&row=' + str(j+1) + '&col=' + str(k+1) + '&number=' + cValue + '&sourceID=' + sourceID + '","' + cValue + '")', url_format, cValue)
					else:
						ws_new.write(j, k, cValue, url_format, cValue.split('","')[1].split('")')[0])
		
	#Close the workbook
	wb_new.close()
	
reconstructFile('testing\\08_06.xlsx','testing\\uploaded.xlsx','testing\\test.xlsx')