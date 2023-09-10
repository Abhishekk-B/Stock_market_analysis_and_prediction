from dataFetchAPI import dataFetch
import pandas as pd
import pymysql



class databaseAPI():
    def __init__(self):
        print("calling............")
        try:
            conn = pymysql.connect(user='root', password='mysql')
            query = "CREATE DATABASE IF NOT EXISTS stockdb"
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            print("Database Added")
        except:
            print("Database already exist.")
       

    def dataInsertion(self,tableName):
        a=dataFetch()
        df=a.fetchingData(tableName)
        # df=pd.read_csv('TSLA1.csv')
        print('Data Fetched')
        print(df.head())
        print(df.shape[1])
        conn = pymysql.connect(user='root', password='mysql',database='stockdb')
        query = "create table IF NOT EXISTS " + tableName + " (open float, high float, low float,close float, volume float,stockdate date);"
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        insert_query = 'INSERT INTO ' + tableName + ' VALUES '
        for i in range(1,df.shape[0]):
            insert_query += "("

            for j in range(df.shape[1]):
                insert_query += '"' + str(df[df.columns.values[j]][i]) + '"' + ", "
            insert_query = insert_query[:-2] + "), "

        insert_query = insert_query[:-2] + ";"
        cursor.execute(insert_query)
        conn.commit()
        conn.close()
        print("Table created and data added")

    def data_fetch(self,tablename,start_date,end_date):
        conn = pymysql.connect(user='root', password='mysql', database='stockdb')
        query = f'SELECT * FROM {tablename} where stockdate between "{start_date}" and "{end_date}";'
        df1 = pd.read_sql(query, conn)
        df1['stockdate']=df1['stockdate'].astype(str)
        conn.close()
        return df1

    def data_fetchAll(self,tablename):
        conn = pymysql.connect(user='root', password='mysql', database='stockdb')
        query = f"SELECT * FROM {tablename};"
        df = pd.read_sql(query, conn)
        
        # Convert datetime to string/object
        df['stockdate']=df['stockdate'].astype(str)
        # print(df.info())
        conn.close()
        print("All data fetched!.")
        return df

















# df=pd.read_csv('TSLA1.csv')
# print(df.head())
# channel='TSLA'


# def mysqldb(channel_name):
#     channel = channel_name.replace(' ', '')
#     # df = pd.read_csv(channel_name+'Details.csv')
#     conn = pymysql.connect(user='root', password='mysql')
#     query1 = "CREATE DATABASE IF NOT EXISTS " + channel + "db;"
#     query2 = "Use " + channel + "db;"
#     query3 = "create table " + channel + " (id int primary key auto_increment, open float, high float, low float,close float, volume float,stockdate date);"
#     cursor = conn.cursor()
#     cursor.execute(query1)
#     conn.commit()
#     cursor.execute(query2)
#     conn.commit()
#     cursor.execute(query3)
#     conn.commit()
#     insert_query = insert_query = 'INSERT INTO ' + channel + ' VALUES '
#     for i in range(df.shape[0]):
#         insert_query += "("

#         for j in range(df.shape[1]):
#             insert_query += '"' + str(df[df.columns.values[j]][i]) + '"' + ", "
#         insert_query = insert_query[:-2] + "), "

#     insert_query = insert_query[:-2] + ";"
#     cursor.execute(insert_query)
#     conn.commit()
#     conn.close()
#     print("Database added")

# # mysqldb("TSLA")

# def data_fetch(start_date,end_date):
#     conn = pymysql.connect(user='root', password='mysql', database='tsladb')
#     query = f'SELECT * FROM tsla where stockdate between "{start_date}" and "{end_date}";'
#     df = pd.read_sql(query, conn)
#     conn.close()
#     return df

# def data_fetchAll():
#     conn = pymysql.connect(user='root', password='mysql', database='tsladb')
#     query = f'SELECT * FROM tsla;'
#     df = pd.read_sql(query, conn)
#     conn.close()
#     return df

# # df=data_fetchAll()