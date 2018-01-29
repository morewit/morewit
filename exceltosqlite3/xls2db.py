#!/usr/bin/python
# encoding=utf-8
'''
Created on 2013-4-2
@author: ting
'''
from xlrd import open_workbook
import sqlite3
import types
def read_excel(sheet):
	#判断有效sheet
	if sheet.nrows > 0 and sheet.ncols > 0:
		for row in range(1, sheet.nrows):
			row_data = []
			for col in range(sheet.ncols):
				data = sheet.cell(row, col).value
				# excel表格内容数据类型转换 float->int，unicode->utf-8
				#if type(data) is types.UnicodeType:
				if isinstance(type(data), str):
					data = data.encode("utf-8")
				elif type(data) is float:
					data = int(data)
				row_data.append(data)
			check_data_length(row_data)
# 检查row_data长度
def check_data_length(row_data):
	if len(row_data) > 0:
		insert_sqlite(row_data)
		print(row_data)
def insert_sqlite(row_data):
	# 打开数据库（不存在时会创建数据库）
	con = sqlite3.connect("sdfz.db")
	cur = con.cursor()
	try:
		#cur.execute("create table if not exists contacts(_id integer primary key autoincrement,name text,age integer,number integer)")
		cur.execute(
			"create table if not exists contacts(xuehao integer primary key,banji integer,name text,kaohao integer,yuwenA integer,yuwenB integer,shuxueA integer,shuxueB integer,yingyuA integer,yingyuB integer,wuliA integer,wuliB integer,shengwu integer,dili integer)")
		# 插入数据不要使用拼接字符串的方式，容易收到sql注入攻击
		#cur.execute("insert into contacts(name,age,number) values(?,?,?)", row_data)
		cur.execute("insert into contacts(xuehao,banji,name,kaohao,yuwenA,yuwenB,shuxueA,shuxueB,yingyuA,yingyuB,wuliA,wuliB,shengwu,dili) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row_data)
		con.commit()
	except sqlite3.Error as e:
		print(('An error occurred: %s', e.args[0]))
	finally:
		cur.close
		con.close
if __name__ == '__main__':
	xls_file = "./sdfz.xls"
	book = open_workbook(xls_file)
	for sheet in book.sheets():
		read_excel(sheet)
		print(str(sheet)+'------ Done ------')