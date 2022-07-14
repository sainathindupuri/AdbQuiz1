import time
import pyodbc
import os
from flask import Flask, Request, render_template, request, flash
from azure.storage.blob import BlobServiceClient, ContentSettings, PublicAccess

app = Flask(__name__, template_folder="templates")

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbdatabaseserver.database.windows.net,1433;Database=adbdatabase;Uid=adbserveruser;Pwd=Darshan@07;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')

cursor = connection.cursor()


columnNames = ['Name','State', 'Salary', 'Grade', 'Room', 'Telnum', 'Picture', 'Keywords']
datasetPath = './people.csv'


@app.route('/', methods=['POST', 'GET'])
def Hello():
    return render_template('index.html')



@app.route('/ShowAllRecords')
def showAllRecords():
    cursor = connection.cursor()
    cursor.execute("Select * from data")
    data = cursor.fetchall()
    link = "https://adbimages.blob.core.windows.net/assignment1/"
    return render_template('ShowAllRecords.html',data=data, link=link)


@app.route('/ShowDetails', methods=['GET', 'POST'])
def showDetails():
    cursor = connection.cursor()    
    classNumber = int(request.form.get("ClassNumber"))    
    cursor.execute("select * from dbo.data where class ={}".format(classNumber))
    data = cursor.fetchall()
    link = "https://adbimages.blob.core.windows.net/assignment1/"
    return render_template('ShowDetails.html', data = data, link = link)   

@app.route('/ModifyComments', methods=['GET', 'POST'])
def update():
    cursor = connection.cursor()   
    name =  request.form.get("name")
    comments = request.form.get("Comments")
    cursor.execute("select * from dbo.data where class ={}".format(comments))
    data = cursor.fetchall()    
    return render_template('ShowAllRecords.html', data = data)     


if __name__ == '__main__':    
    app.run()

