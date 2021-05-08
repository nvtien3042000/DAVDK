import mysql.connector
##
##data = mysql.connector.connect(
##  host="localhost",
##  user="root",
##  password="nguyenvantien9",
##  database="data"
##)
##print(data)
##
##mycursor = data.cursor()
##
##mycursor.execute("SELECT * FROM listplate")
##
##myresult = mycursor.fetchall()
##print(len(myresult))
##for x in myresult:
##  print(x[0])
  

def connect(HOST, USER, PASS, DB):
    return mysql.connector.connect(
          host=HOST,
          user=USER,
          password=PASS,
          database=DB
    )

def query(connectDB, plate):
    mycursor = connectDB.cursor()
    
    mycursor.execute("SELECT * FROM vehicle where number_plate = '" + plate + "'")

    myresult = mycursor.fetchall()

    return len(myresult)
    
