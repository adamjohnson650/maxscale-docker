# Adam Johnson
# CNE 370
# 3/12/2024
# sharding and python code geekforgeeks.com
# Got some help with the code from Celine Watcharaapakorn
import mysql.connector
from tabulate import tabulate

db = mysql.connector.connect(host="172.17.0.1", port="4000", user="maxuser", password="maxpwd")
cursor = db.cursor()

# The largest zipcode in zipcodes_one
print('The largest zipcode in zipcodes_one:')
cursor.execute("SELECT Zipcode FROM zipcodes_one ORDER BY Zipcode DESC LIMIT 1;")
result = cursor.fetchone()
print(result[0])

# All zipcodes where state = KY
print('All zipcodes where state = KY:')
cursor.execute("SELECT Zipcode FROM zipcodes_one WHERE State = 'KY';")
results = cursor.fetchall()
print(tabulate(results, headers=['Zipcode'], tablefmt='grid'))

# All zipcodes between 40000 and 41000
print('All zipcodes between 40000 and 41000:')
cursor.execute("SELECT Zipcode FROM zipcodes_one WHERE Zipcode BETWEEN 40000 AND 41000;")
results = cursor.fetchall()
print(tabulate(results, headers=['Zipcode'], tablefmt='grid'))

# The TotalWages column where state = PA
print('The TotalWages column where state = PA:')
cursor.execute("SELECT TotalWages FROM zipcodes_one WHERE state = 'PA';")
results = cursor.fetchall()
print(tabulate(results, headers=['TotalWages'], tablefmt='grid'))

# Close the database connection
db.close()
