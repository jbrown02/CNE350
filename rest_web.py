#Restful interface that has search and update options for navigating a Zip code database on Phpmyadmin.


#https://stackoverflow.com/questions/8211128/multiple-distinct-pages-in-one-html-file
#https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python
#https://stackoverflow.com/questions/1081750/python-update-multiple-columns-with-python-variables
#https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
#https://github.com/vimalloc/flask-jwt-extended/issues/175

# Joshua Brown
# 5/31/2023 - Midterm Project
# CNE 350 - Justin Ellis

from mysql import connector
from flask import Flask, redirect, url_for, request, render_template
import mysql.connector
app = Flask(__name__, static_url_path='')

#connect to database
conn = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='zipcodes',
                               port='8889',
                               buffered = True)
cursor = conn.cursor()

#Search state database
@app.route('/searchZIPCODE/<searchZipcode>')
def searchstate(searchZipcode):
    # Get data from database
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [searchZipcode])
    test = cursor.rowcount
    if test != 1:
        return searchZipcode + " was not found"
    else:
        searched = cursor.fetchall()
        return 'Success! Here you go: %s' % searched

#update state database population for a specified state
@app.route('/updatestatepop/<updateZIPCODE> <updatePOPULATION>')
def updatestatepop(updateZIPCODE, updatePOPULATION):
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [updateZIPCODE])
    test = cursor.rowcount
    if test != 1:
        return updateZIPCODE + " was not found"
    else:
        cursor.execute("UPDATE `zipcodes` SET Population = %s WHERE zip= %s;", [updatePOPULATION,updateZIPCODE])
        cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s and Population=%s", [updateZIPCODE,updatePOPULATION])
        test1 = cursor.rowcount
        if test1 != 1:
            return updateZIPCODE + "  failed to update"
        else:
            return 'Population has been updated successfully for zip: %s' % updateZIPCODE

#update webpage
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        user = request.form.get('ustate')
        user2 = request.form.get('upop')
        if user and user2:
            return redirect(url_for('updatestatepop', updateZIPCODE=user, updatePOPULATION=user2))
    return render_template('update.html')

#search page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        user = request.form.get('sstate')
        if user:
            return redirect(url_for('searchstate', searchZipcode=user))
    return render_template('search.html')

#root of web server and gots to template (login.html)
@app.route('/')
def root():
   return render_template('login.html')

#main
if __name__ == '__main__':
   app.run(debug = True)
