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
        formFile = forms.CSVFileUpload(request.form)

        seqList = [("Seq1","Seq1"),("Seq2","Seq2")]
        #seqList=queries.getAllSequences()
        formSeq.sequence.choices=seqList
        formMVal.sequence.choices=seqList

        if(request.method == 'POST'):

                #print(request.form)
                #print(formMVal.validate())
        

                if(request.form["btn"] == "condition" and formCond.validate()):
                        print("Do Condition Insert")
                elif(request.form["btn"] == "measure" and formMeasure.validate()):
                        print("Do measure Insert")
                elif(request.form["btn"] == "sequence" and formSeq.validate()):
                        print("Do sequence modify")
                elif(request.form["btn"] =="mVal" and formMVal.validate()):
                        print("Do mval insert")
                        #resultSet of form submission
                        sequence = formMVal.sequence.data
                        measurement = formMVal.measurement.data
                        mVal = formMVal.value.data
                        print(sequence)
                        print(measurement)
                        print(mVal)
                        conditionList = formMVal.getConditions()
                        print(conditionList)
                        
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, formFile=formFile)
                        
                        #insertion into database

                elif(request.form["btn"] == "addCond"):
                        formMVal.addCondition()
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, showMeasure="true",formFile=formFile)
                elif(request.form["btn"] == "fileUpload" and formFile.validate()):
                        print("file upload")
                        forms.validateFile(request.files["file"])

                        
        
        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal,formFile=formFile)

@app.route("/about", methods =["GET","POST"])
def aboutPage():
        return render_template("about.html")

if __name__ == "__main__":
    app.run()
