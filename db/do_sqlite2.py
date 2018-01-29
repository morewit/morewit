import sqlite3
import math

cx = sqlite3.connect("mydatabase.db")
cu = cx.cursor()
cu.execute('create table student (id varchar(20) primary key, name varchar(20),age inter)')

i = 0
for i in range(50, 60):
    # (1)插入方式： 先构造数据，然后再插入
    v = (i, 'zhang', 4)
    ins = "insert into student values(?,?,?);"
    cu.execute(ins, v)

    # (2)插入方式：直接组合数据插入，note:需要将数值转换为字符串
    # sqls = "insert into student values('" + str(i) + "', 'wa', 5)"
    # cu.execute(sqls)
    i = i + 1

cx.commit()
cx.close()

#raw_input()