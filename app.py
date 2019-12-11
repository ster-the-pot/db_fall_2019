from flask import Flask, render_template,request,redirect,url_for,session, logging
from wtforms import Form,StringField,TextAreaField,validators, SelectField
import mysql.connector
import forms
import queries

app = Flask(__name__)
app.debug= True


@app.route("/")
def homePage():
        return render_template('index.html')

@app.route("/input", methods=["GET","POST"])
def inputPage():
        formCond = forms.AddConditionForm(request.form)
        formMeasure = forms.AddMeasurementForm(request.form)
        formSeq = forms.ModifySequenceForm(request.form)
        formMVal = forms.InsertMeasurementForm(request.form)

        seqList = [("Seq1","Seq1"),("Seq2","Seq2")]
        #seqList=queries.getAllSequences()
        formSeq.sequence.choices=seqList
        formMVal.sequence.choices=seqList

        formMVal.addCondition()
        
        

        if(request.method == 'POST'):


                if(request.form["btn"] == "condition" and formCond.validate()):
                        print("Do Condition Insert")
                elif(request.form["btn"] == "measure" and formMeasure.validate()):
                        print("Do measure Insert")
                elif(request.form["btn"] == "sequence" and formSeq.validate()):
                        print("Do sequence modify")
                elif(request.form["btn"] =="mVal" and formMVal.validate()):
                        print("Do mval insert")
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal)
                elif(request.form["btn"] == "addCond"):
                        formMVal.addCondition()
                        print("added")
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, showMeasure="true")

                        
        
        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal)

@app.route("/about", methods =["GET","POST"])
def aboutPage():
        return render_template("about.html")

if __name__ == "__main__":
    app.run()
