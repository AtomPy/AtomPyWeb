########################
# Validate File Python Script for AtomPy 2.1
#
# Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
#
# Takes two files and compares the original one to the new one for data cohesion
########################

#Include needed libraries
import os, openpyxl

#Validate function
def validateFile(original_filename, uploaded_filename):

	#Open our two files (the uploaded one and the one in the DB)
	wb_original = openpyxl.load_workbook(original_filename)
	wb_uploaded = openpyxl.load_workbook(uploaded_filename)

	#ERROR CHECK: Uploaded file should NOT be smaller than original
	if os.path.getsize(location) <= os.path.getsize(original_filename):
		return "ERROR: Uploaded file has a size smaller than or equal to the original file."
		
	#ERROR CHECK: Uploaded file should have the same number of sheets as the original file
	if len(wb_original.worksheets) != len(wb_uploaded.worksheets):
		return "ERROR: Uploaded file does not have same number of sheets as original file."

	#Begin going through all of the sheets in the workbooks
	for i in range(len(wb_original.worksheets)):

		#Get the current sheets
		ws_original = wb_original.get_sheet_by_name(wb_original.get_sheet_names()[i])
		ws_uploaded = wb_uploaded.get_sheet_by_name(wb_uploaded.get_sheet_names()[i])
		
		#ERROR CHECK: Uploaded file should NOT have fewer rows/cols
		#			  than the original file.
		if len(ws_uploaded.rows) < len(ws_original.rows):
			return "ERROR: Uploaded file has FEWER rows than original file. Perhaps you deleted some data?"
		if len(ws_uploaded.columns) < len(ws_original.columns):
			return "ERROR: Uploaded file has FEWER columns than original file. Perhaps you deleted some data?"
			
		#QUICK CHECK: Current sheet of the uploaded file has no
		#			  rows added to it
		rowsChanged = True
		if len(ws_uploaded.rows) == len(ws_original.rows):
			rowsChanged = False
			
		#QUICK CHECK: Current sheet of the uploaded file has no
		#			  columns added to it
		colsChanged = True
		if len(ws_uploaded.columns) == len(ws_original.columns):
			colsChanged = False
			
		#QUICK CHECK: Current sheet of the uploaded file has no
		#			  rows AND no columns added to it, so why bother?
		if rowsChanged == False and colsChanged == False:
			continue
		
		#Now we can finally get down to the actual data validation
		
		#Rows can be INSERTED
		#Columns can be APPENDED
		
		#Find the category data lines for each
		cLine_original = -1
		for j in range(len(ws_original.rows)):
			if ws_original.cell(row=j+1, column=1).value == 'Z':
				cLine_original = j
				break
		cLine_uploaded = -1
		for j in range(len(ws_uploaded.rows)):
			if ws_uploaded.cell(row=j+1, column=1).value == 'Z':
				cLine_uploaded = j
				break
				
		#Go through the original data and convert the rows to arrays
		originalRows = []
		for j in range(len(ws_original.rows)):
			originalRow = []
			for k in range(len(ws_original.columns)):
				cValue = ws_original.cell(row=j+1, column=k+1).value
				originalRow.append(cValue)
			originalRows.append(originalRow)
		
		#Go through the uploaded data and convert the rows to arrays
		uploadedRows = []
		for j in range(len(ws_uploaded.rows)):
			uploadedRow = []
			for k in range(len(ws_original.columns)):#ONLY what
				#The original data would have contained
				#This way appended columns don't interfere with
				#Data validation
				cValue = ws_uploaded.cell(row=j+1, column=k+1).value
				uploadedRow.append(cValue)
			uploadedRows.append(uploadedRow)
			
		#The way we will do the validation is as follows:
		#We will go through all of rows of the original data and try
		#to find them in the new data
		found = [-1 for x in xrange(len(ws_original.rows))]
		
		#Begin going through the rows
		for j in range(len(ws_original.rows)):
			if originalRows[j] in uploadedRows:
				found[j] = 1
				
		#Did we find all of the rows? If not, error out
		if -1 in found:
			return 'ERROR: Some original data not found in new data.'
			
	#Return OK
	return 'OK'