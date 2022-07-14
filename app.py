import string
import time
import pyodbc
import os
from flask import Flask, Request, render_template, request, flash
from azure.storage.blob import BlobServiceClient, ContentSettings, PublicAccess

app = Flask(__name__, template_folder="templates")

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbsai.database.windows.net,1433;Database=adb;Uid=sainath;Pwd=Shiro@2018;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')

cursor = connection.cursor()



@app.route('/', methods=['POST', 'GET'])
def Hello():
    return render_template('index.html')



@app.route('/ShowAllRecords')
def showAllRecords():
    cursor = connection.cursor()
    cursor.execute("select * from quiz1")
    data = cursor.fetchall()
    link = "https://adbimages.blob.core.windows.net/assignment1/"
    return render_template('ShowAllRecords.html',data=data, link=link)


@app.route('/ShowDetails', methods=['GET', 'POST'])
def showDetails():
    cursor = connection.cursor()    
    startAge = int(request.form.get("StartAge"))    
    endAge = int(request.form.get("EndAge"))    
    cursor.execute("select * from dbo.[data-1] where class>={} AND class <={}".format(startAge,endAge))
    data = cursor.fetchall()
    link = "https://adbimages.blob.core.windows.net/assignment1/"
    return render_template('showDetails.html', data = data, link = link)   

@app.route('/Modify', methods=['GET', 'POST'])
def update():
    cursor = connection.cursor()   
    name =  request.form.get("Name")    
    cursor.execute("select * from dbo.[data-1] a where a.name = '"+name+"'")
    data = cursor.fetchall()  
    comments = data[0][4]
    print(comments)
    name = data[0][0]
    classno = data[0][2]
    print(data[0]) 
    return render_template('ModifyForm.html', comments = comments, name = name, classno=classno)  


@app.route('/ModifySubmit', methods=['GET', 'POST'])
def modifySubmit():
    cursor = connection.cursor()   
    name =  request.form.get("Name")  
    classnumber = int(request.form.get("ClassNumber"))
    comments = request.form.get("Comments")
    print(comments)
    sqlq = "UPDATE dbo.[data-1] SET class = "+str(classnumber)+", comments = '"+comments+"' WHERE name = '"+name+"'"   
    print(sqlq)
    cursor.execute(sqlq)     
    
    return render_template('index.html')     


if __name__ == '__main__':    
    app.run()

