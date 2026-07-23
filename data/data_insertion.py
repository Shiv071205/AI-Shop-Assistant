import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  

#connect csv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, "shop-product-catalog.csv")
data=pd.read_csv(csv_file)

#connect mysql
db_connect = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT"))
)

cursor=db_connect.cursor()

#upload data to the table
for index,row in data.iterrows():
    sql="""
    INSERT INTO products (ProductID,ProductName,ProductBrand,Gender,Price,Description,PrimaryColor)
    VALUES(%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(sql,tuple(row))

db_connect.commit()

cursor.close()
db_connect.close()



