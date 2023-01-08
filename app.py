from flask import Flask, render_template

app = Flask(__name__)

headings = ("Name")
data = ("Course1", "Course2", "Course3", "Course4", "Course5")

@app.route("/")
def table():
    return render_template("table.html", headings=headings, data=data)