# Adam Johnson
# CNE 370
# 3/12/2024
# sharding and python code geekforgeeks.com
# Got some help with the code from Celine Watcharaapakorn
import mysql.connector
from tabulate import tabulate

db = mysql.connector.connect(host="172.17.0.1", port="4000", user="maxuser", password="maxpwd")
cursor = db.cursor()

#Query 1 selects the Zipcode column from the "zipcode_one" table, orders the results in descending order, and limits the output to one row. 
#The fetchone() method retrieves the first row of the result set. the largest zipcode is printed.
# The largest zipcode in zipcodes_one
print('The largest zipcode in zipcodes_one:')
cursor.execute("SELECT Zipcode FROM zipcodes_one ORDER BY Zipcode DESC LIMIT 1;")
result = cursor.fetchone()
print(result[0])

# Query 2 selects all zipcodes from the "zipcodes_one" table where the state is KY the fetchall() method retrieves all rows of the result set.
# The tabulate() function formats the results as a grid with the column header Zipcode and prints the tabulated results to the console.
# All zipcodes where state = KY
print('All zipcodes where state = KY:')
cursor.execute("SELECT Zipcode FROM zipcodes_one WHERE State = 'KY';")
results = cursor.fetchall()
print(tabulate(results, headers=['Zipcode'], tablefmt='grid'))

#Query 3 selects all zipcodes from the "zipcode_one" table where the zip code falls within the 40000 and 41000 The results are tabulated and printed to the console.
# All zipcodes between 40000 and 41000
print('All zipcodes between 40000 and 41000:')
cursor.execute("SELECT Zipcode FROM zipcodes_one WHERE Zipcode BETWEEN 40000 AND 41000;")
results = cursor.fetchall()
print(tabulate(results, headers=['Zipcode'], tablefmt='grid'))

#Query 4 selects the TotalWages column from the zipcode_one table where the state is PA The tabulated results are printed to the console.
# The TotalWages column where state = PA
print('The TotalWages column where state = PA:')
cursor.execute("SELECT TotalWages FROM zipcodes_one WHERE state = 'PA';")
results = cursor.fetchall()
print(tabulate(results, headers=['TotalWages'], tablefmt='grid'))

# Close the database connection
db.close()
