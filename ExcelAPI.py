import openpyxl

def openFile(filename):
	wb = openpyxl.load_workbook(filename)
	return wb

