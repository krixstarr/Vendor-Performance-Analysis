import pandas as pd
import os
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="tatatiago",
    port=3306
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS inventory")

conn.commit()

print("inventory database created!")
conn.close()

from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:tatatiago@localhost:3306/inventory"
)

with engine.connect() as conn:
    print("Connected to inventory!")


def ingest_db(df,table_name,engine):
    df.to_sql(table_name, con=engine,if_exists="append", index = False)

'''INGESTING FILES EXCEPT SALES.CSV'''
def load_data():
    for file in os.listdir("data"):
        if file.endswith(".csv") and file.lower() != "sales.csv":
            df=pd.read_csv("data/"+ file)
            print(df.shape)
            ingest_db(df,file[:-4],engine)
               
'''INGESTING SALES.CSV SEPERATELY IN CHUNKS DUE TO LARGE DATA'''
def sales_data():
    file = "sales.csv"
    for df in pd.read_csv("data/" + file, chunksize=50000):
        print(df.shape)
        ingest_db(df, file[:-4], engine)


if __name__ == "main":
    load data()
    sales data()
