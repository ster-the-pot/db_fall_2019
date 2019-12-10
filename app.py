from flask import Flask, render_template,request,redirect,url_for,session, logging
from wtforms import Form,StringField,TextAreaField,validators, SelectField
import mysql.connector
import forms

app = Flask(__name__)
app.debug= True


@app.route("/")
def homePage():
        return render_template('index.html')

@app.route("/input")
def inputPage():
        form = forms.AddConditionForm(request.form)
        if(request.method == 'POST' and form.validate()):
                print(form.validate)
                print(form.domain.data)
                print(form.conditions.data)
        return render_template(".html",form=form)

@app.route("/about", methods =["GET","POST"])
def aboutPage():
        return render_template("about.html",form=form)

if __name__ == "__main__":
    app.run()
