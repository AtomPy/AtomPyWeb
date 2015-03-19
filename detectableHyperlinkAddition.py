import xlsxwriter

wb = xlsxwriter.Workbook('test.xlsx')
ws = wb.add_worksheet('test')

url_format = wb.add_format({
    'font_color': 'blue',
    'underline':  1
})

#ws.write_url('A1', 'http://www.google.com', url_format, 'TEST1')
ws.write('A1','=HYPERLINK("http://www.google.com", "TEST1")', url_format, "TEST1")

wb.close()