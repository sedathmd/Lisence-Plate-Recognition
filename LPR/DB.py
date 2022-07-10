import mysql.connector

connection = mysql.connector.connect(
                              host='localhost',
                              user='root',
                              password='',
                              database='lisenceplaterecognition')                         
 
cur = connection.cursor()
   
def karsılastırma(text):
    
    cur.execute("SELECT isim, unvan FROM `information` WHERE plaka = '{}'".format(f"{text}"))
    data = cur.fetchall()
    return data
