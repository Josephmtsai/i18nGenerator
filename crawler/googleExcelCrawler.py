import os
from apiclient import discovery
import datetime
import re

def geti18nFromExcel(apiKey, excelsheetid,keys):
    sheetList = [u'Resource']
    outputSource = {}
    for key in keys:
        outputSource[key] = {}
    service = discovery.build('sheets', 'v4', developerKey=apiKey,
                              discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')
    result = service.spreadsheets().values().batchGet(spreadsheetId=excelsheetid, ranges=sheetList,
                                                      valueRenderOption='FORMULA', dateTimeRenderOption='FORMATTED_STRING').execute()
    responseSheet = result.get('valueRanges', [])
    headers = {}
    for index, sheet in enumerate(responseSheet):
        rows = sheet.get('values', [])
        for rowIndex, row in enumerate(rows):
            if  rowIndex == 0:
                for cellIndex,cell in enumerate(row):
                    headers[cellIndex]= str(cell)
            else:
                for cellIndex,cell in enumerate(row):
                    cellName = headers[cellIndex]
                    print(cellName)
                    translateName = row[0]
                    if cellName in keys:
                        outputSource[cellName][translateName] = cell
    return outputSource


