#! /usr/bin/python
# -*- coding: UTF-8 -*-

import xlrd
import xlwt
import os
from datetime import date,datetime

#配置相关
#过滤的文件类型
file_type = ".xls"
#捕获的符合类型的名字
catch_title = "小白鞋"

#标题行暂存
newFile_titles = []
newFile_lists = []

#读取指定文件下的所有文件
def read_File_List(file_dir):
    for root, folders, files in os.walk(file_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if isIgnoreType(file_path):
                read_File(file_path)
    
#是否属于符合规则的文件类型
def isIgnoreType(file_path):
    global file_type
    ext = os.path.splitext(file_path)[1]
    if ext == file_type:
        return True
    return False  


def read_File(file_name):
    # 打开文件
    global newFile_titles, catch_title, newFile_lists

    workbook = xlrd.open_workbook(file_name)
    sheetFirst = workbook.sheet_by_index(0)

    if len(newFile_titles) == 0 :
        newFile_titles = sheetFirst.row_values(0)
        
    row_tempNum = 1
    while 1:
        if row_tempNum >= sheetFirst.nrows:
            break

        cell = sheetFirst.row_values(row_tempNum)
        if cell:
            if sheetFirst.cell(row_tempNum,2).ctype == 1:
                catch_temp_title = sheetFirst.row(row_tempNum)[2].value.encode('utf-8')
                row_tempNum+=1
                if catch_title in catch_temp_title:
                    newFile_lists.append(sheetFirst.row_values(row_tempNum-1))
            else:
                row_tempNum+=1 
        else:
            break
    
    
def write_NewFile():
    global newFile_lists, newFile_titles
    newFilePath = os.path.join('total.xls')

    if os.path.exists(newFilePath):
        os.remove(newFilePath)
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('page 1', cell_overwrite_ok=True)

    for num, val in enumerate(newFile_titles):
        sheet.write(0, num, val)

    for num1, val1 in enumerate(newFile_lists):
        for num2, val2 in enumerate(val1):
            print '行数：%d' %(num1+1)
            print '列数：%d' %(num2)
            sheet.write(num1+1, num2, val2)
            
    book.save(newFilePath)

if __name__ == "__main__":
    read_File_List('files')
    write_NewFile()
