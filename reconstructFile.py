########################
# Reconstruct File Python Script for AtomPy 2.1
#
# Created by Josiah 'Lucas' Boswell (www.josiahboswell.com)
#
# Takes two files and compares the original one to the new one for data cohesion
########################

#Include needed libraries
import xlsxwriter, openpyxl, sys

def reconstructFile():

	#Get the filename
	filename = str(sys.argv[1])

	#Open the original workbook
	wb_original = openpyxl.load_workbook(filename)

	#Open up the new workbook
	wb_new = xlsxwriter.Workbook('new_' + filename)

	url_format = wb_new.add_format({
		'font_color': 'blue',
		'underline':  1,
		'font_name': 'Arial',
		'font_size': 10
	})

	format = wb_new.add_format()
	format.set_font_name('Arial')
	format.set_font_size(10)

	#Go through the original workbook
	for i in range(len(wb_original.worksheets)):

		#Get the current sheet from the original workbook
		ws_original = wb_original.get_sheet_by_name(wb_original.get_sheet_names()[i])
		
		#Now create the new worksheet
		ws_new = wb_new.add_worksheet(wb_original.get_sheet_names()[i])
		
		#Get the column widths from the original workbook and set the column widths in the new workbook
		for i in range(len(ws_original.columns)):
			if ws_original.column_dimensions[openpyxl.cell.get_column_letter(i+1)].width != None:
				ws_new.set_column(i, i, ws_original.column_dimensions[openpyxl.cell.get_column_letter(i+1)].width)
		
		#Go through the rows in the original workbook
		for j in range(len(ws_original.rows)):
		
			#Go through the columns in the original workbook
			for k in range(len(ws_original.columns)):
				
				#Get the original value
				cValue = ws_original.cell(row=j+1, column=k+1).value
				try:
					cValue = str(cValue)
				except:
					cValue.replace(u'\xa0', u' ')
				
				#Grab the number format
				format.set_num_format(ws_original.cell(row=j+1, column=k+1).style.number_format)
				url_format.set_num_format(ws_original.cell(row=j+1, column=k+1).style.number_format)
				
				#Write the cell regardless and format it
				if format.num_format == 'General':
					ws_new.write(j, k, cValue)
				else: 
					ws_new.write(j, k, cValue, format)
					
				#Deal with formulas and hyperlinks
				if type(cValue) is unicode:
					if '=' in cValue:
						if 'HYPERLINK' in cValue:
							ws_new.write_url(j, k, cValue.split('"')[1], url_format, cValue.split('"')[3])
						else:
							if format.num_format == 'General':
								ws_new.write_formula(j, k, cValue)
							else:
								ws_new.write_formula(j, k, cValue, format)
								
		break#REMOVE WHEN DONE

	#Close the workbook
	wb_new.close()