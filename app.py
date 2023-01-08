from flask import Flask, render_template
from schedule import *

app = Flask(__name__)

headings = ["Sem1", "Sem2","Sem3","Sem4","Sem5","Sem6","Sem7","Sem8"]

json_data = open_json("ualberta_data/courses.json")
degree_data = open_json("ualberta_data/CMPUTcatalouge.json")

degree = build_degree(json_data, degree_data)



data1 = degree[0:5] 
data2 = degree[5:10] 
data3 = degree[10:15] 
data4 = degree[15:20] 
data5 = degree[20:25] 
data6 = degree[25:30] 
data7 = degree[30:35] 
data8 = degree[35:40] 



@app.route("/")
def table():
    return render_template("table.html", headings=headings, data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7, data8=data8)