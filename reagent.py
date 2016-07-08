# -*- coding:utf-8 -*- 
# author：zhouyang
import pandas as pd
import MySQLdb
from datetime import datetime
import numpy as np
from util import delete_table,rebuild_table

con = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", db="ezlife", charset="utf8")

# 删除原来表的内容
delete_table("reagent",con)

df = pd.read_csv("/Users/zhouyang/Downloads/20160706/reagent.csv")

# 需要更换列名的列,及更换之后的列名对应关系
rename_dict = {
    "purchase_data": "purchase_date",
    "arrival_data": "arrival_date",
    "created_data": "create_date"
}
df = df.rename(columns=rename_dict)
df['purchase_date'] = df['purchase_date'].map(lambda x: x if pd.isnull(x) else str(int(x)))
df['arrival_date'] = df['arrival_date'].map(lambda x: x if pd.isnull(x) else str(int(x)))
df['create_date'] = df['create_date'].map(lambda x: x if pd.isnull(x) else str(int(x)))


# 将日期字符串转换为datetime数据类型
def transform_date(x):
    # 对不规范日期,记为空
    if len(x) != 14:
        print 'date is wrong. please check it later!'
        print 'the wrong date is ', x
        return np.nan
    year = int(x[:4])
    month = int(x[4:6])
    # 月份出现了0,非法!
    if month <= 0:
        month = 1
    day = int(x[6:8])
    # 日期出现了0,非法!
    if day <= 0:
        day = 1
    hour = int(x[8:10])
    min = int(x[10:12])
    second = int(x[12:])
    return datetime(year=year, month=month, day=day, hour=hour, minute=min, second=second)


df['purchase_date'] = df['purchase_date'].map(lambda x: x if pd.isnull(x) else transform_date(x))
df['arrival_date'] = df['arrival_date'].map(lambda x: x if pd.isnull(x) else transform_date(x))
df['create_date'] = df['create_date'].map(lambda x: x if pd.isnull(x) else transform_date(x))
try:
    pd.io.sql.to_sql(df, 'reagent', con, flavor='mysql', if_exists='append', index=False)
except Exception,e:
    print e
    print 'there is an error, please fix it before continue!'
    exit(-1)
    
# transfer data to remote mysql server
yihuo_con = MySQLdb.connect(host="52.192.115.115", user="root", passwd="yihuo_root", port=3306, charset="utf8",
                            db="ezlife")
rebuild_table(table_name="reagent", con=yihuo_con, df=df)
