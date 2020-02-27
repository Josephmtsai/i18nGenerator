import xlrd
import validators
import xlsxwriter,datetime
def readExcelToDictionary(fileName,sheetName):
	excelBook = xlrd.open_workbook(fileName,encoding_override = 'utf-8')
	# select the sheet that the data resids in
	workSheet = excelBook.sheet_by_name(sheetName)
	#get Headers
	headers = [str(cell.value) for cell in workSheet.row(0)]
	"""
	header =[] 
	for cell in workSheet.row(0):
    	header.append(str(cell.value))
	"""
	userDataList = []
	for row in range(1,workSheet.nrows):
		userData = {}
		for column in range(workSheet.ncols):
			dataValue  = (workSheet.cell(row,column).value)
			if workSheet.cell(row,column).ctype == 3: # 3 means 'xldate' , 1 means 'text'
				year, month, day, hour, minute, second = xlrd.xldate_as_tuple(dataValue, 
				excelBook.datemode)
				dateDate = datetime.datetime(year, month, day, hour, minute, second)
				dataValue = dateDate.strftime("%Y/%m/%d")
			try:
				dataValue = str(dataValue)
			except ValueError:
				pass
			finally:
				key = headers[column]
				userData[key] = dataValue
				#userData['userName'] = "AAA"
		userDataList.append(userData)
	return userDataList
	
def DictionaryToExcel(fileName,dataList):
	#dataList = {key : [{.....}]}

	#dataList = {'sheet1' :[{'AA':''},{'AA':'C'}] , 'sheet2' :[{'AA':''},{'AA':'C'}]}
	workbook = xlsxwriter.Workbook(fileName)
	for key, sheetDataList in dataList.items():
		worksheet = workbook.add_worksheet(key)
		bold = workbook.add_format({'bold': 1})
		headings = list(sheetDataList[0].keys())	
		worksheet.write_row('A1', headings, bold)
		row_count = 1
		for rowIndex in range(len(sheetDataList)):
			format = workbook.add_format()
			for columnIndex in range(len(headings)):
				head = headings[columnIndex]
				worksheet.set_column(0, 0, 80) # width of columns 80
				worksheet.set_column(1,1,10)
				worksheet.set_column(2,2,80)
				worksheet.set_column(3,3,20)
				if head in sheetDataList[rowIndex]:
					if validators.url(sheetDataList[rowIndex][head]):
						red_format = workbook.add_format({'font_color': 'red','bold':1,'underline':  1,'font_size':  12,})
						worksheet.write_url(row_count, columnIndex, sheetDataList[rowIndex][head],red_format,'Link')
					else:
						worksheet.write(row_count, columnIndex, sheetDataList[rowIndex][head],format)
				else:
					format.set_bg_color('green') 
					worksheet.write(row_count, columnIndex, "Value Not Exist!!",format)
			row_count+=1
	workbook.close()
	

