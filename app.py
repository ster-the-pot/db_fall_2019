from flask import Flask, render_template, request,redirect,url_for,session, logging
from wtforms import Form,StringField,TextAreaField,validators
import mysql.connector

app = Flask(__name__)
app.debug= True


@app.route("/")
def homePage():
        return render_template('index.html')

@app.route("/input")
def inputPage():
        return render_template("input.html")

@app.route("/about")
def aboutPage():
        return render_template("about.html")

class AddConditionForm(Form):
        conditions = StringField('Name', validators=[validators.Length(min=1,max=50)])
        username = StringField('Username', validators=[validators.Length(min=4,max=25)])

if __name__ == "__main__":
    app.run()
