import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="username",
    passwd="password",
    database="scrapping"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM companies")

myresult = mycursor.fetchall()
# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("Michelle", "Blue Village")
# mycursor.execute(sql, val)

# mydb.commit()

print(myresult)


def get_db_conn():
    # mycursor.execute(
    #     "INSERT INTO companies (name, headquarters) VALUES (%s, %s)",
    #     ("test", None))
    # mycursor.execute("SELECT * FROM companies")
    # myresult = mycursor.fetchall()
    # mydb.commit()
    # print(myresult)
    return mydb
