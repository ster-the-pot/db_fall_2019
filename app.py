from flask import Flask, render_template,request,redirect,url_for,session, logging, flash
from wtforms import Form,StringField,TextAreaField,validators, SelectField
import forms
import queries
import sys
sys.path.append('Backend/')
import Backend.csvparse as csvparse
from queries import cursor,mydb
import Backend.input as input



## SQL Server connection 


###### Main Web App ######

app = Flask(__name__)
app.debug= True
app.secret_key="bryceSterlingCool"


@app.route("/")
def homePage():
        return render_template('index.html')

@app.route("/query/experiment", methods=["GET","POST"])
def experimentPage():
        formMVal = forms.QueryMeasurementForm(request.form)
        
        if(request.method=="POST"):
                if(request.form["btn"] == "mVal" and formMVal.validate()):
                        print("Do Experiment Lookup")
                        #results of query
                        conditionList = formMVal.getConditions()
                        sequence = formMVal.sequence.data
                        #################################
                        measurements = input.experimentInfo(sequence,conditionList,cursor)
                        print(measurements)

                        return render_template('experiment.html',formMVal=formMVal, measurements=measurements) 
                elif(request.form["btn"] == "addCond"):
                        print("add conditions")
                        formMVal.addCondition()
                        
                        return render_template('experiment.html',formMVal=formMVal, showMeasure="true")                
        return render_template('experiment.html',formMVal=formMVal)



@app.route("/query/side", methods=["GET","POST"])
def sideBySidePage():
        
        
        formMVal = forms.DualQueryMeasurementForm(request.form)
        
        
        if(request.method=="POST"):
                
                if(request.form["btn"] == "mVal" and formMVal.validate()):
                        print("Do Experiment Lookup")
                        
                        
                        conditions1 =formMVal.getConditions(1)
                        conditions2=formMVal.getConditions(2)

                        measurements = input.side_by_side(formMVal.getSequence(1),conditions1,formMVal.getSequence(2),conditions2,cursor)
                        print(measurements)
                        mydb.commit()
                        experiments = [
                                        {"sequence":formMVal.getSequence(1),
                                        "conditionList":conditions1
                                        },{"sequence":formMVal.getSequence(2),
                                        "conditionList":conditions2
                                        }
                                ]
                        
                        return render_template('side.html',formMVal = formMVal, measurements=measurements, experiments=experiments) 
                elif(request.form["btn"] == "addCond"):
                        print("add conditions")
                        formMVal.addCondition(1)
                        return render_template('side.html',formMVal=formMVal, showMeasure="true")

                elif(request.form["btn"] == "addCond2"):
                        print("add conditions2")
                        formMVal.addCondition(2)
                        
                        return render_template('side.html',formMVal=formMVal, showMeasure="true")
         
        

        return render_template('side.html',formMVal=formMVal )



@app.route("/input", methods=["GET","POST"])
def inputPage():
        formCond = forms.AddConditionForm(request.form)
        formMeasure = forms.AddMeasurementForm(request.form)
        formSeq = forms.ModifySequenceForm(request.form)
        formMVal = forms.InsertMeasurementForm(request.form)
        formFile = forms.CSVFileUpload(request.form)


        
        #seqList=queries.getAllSequences()

        if(request.method == 'POST'):

                #print(request.form)
                #print(formMVal.validate())

                if(request.form["btn"] == "condition" and formCond.validate()):
                        print("Do Condition Insert")
                        print(formCond.conditions.data)
                        print(formCond.domain.data)
                
                        if(input.conditionAdd(formCond.conditions.data, formCond.domain.data,cursor)):
                                flash("Insertion Successful","success")
                                mydb.commit()
                        else:
                                flash("Insertion Failed", "failed")
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, formFile=formFile)

                elif(request.form["btn"] == "measure" and formMeasure.validate()):
                        print("Do measure Insert")
                        print(formMeasure.measurement.data)
                        print(formMeasure.domain.data)
                        if(input.measurementAdd(formMeasure.measurement.data,formMeasure.domain.data,cursor)):
                                flash("Insertion Successful","success")
                                mydb.commit()
                        else:
                                flash("Insertion Failed", "failed")
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, formFile=formFile)

                elif(request.form["btn"] == "sequence" and formSeq.validate()):
                        print("Do sequence modify")
                        
                        if(input.sequenceAdd(formSeq.sequence.data,formSeq.description.data,cursor,formSeq.filename.data)):
                                flash("Insertion Successful","success")
                                mydb.commit()
                        else:
                                flash("Insertion Failed", "failed")
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, formFile=formFile)


                elif(request.form["btn"] =="mVal" and formMVal.validate()):
                        print("Do mval insert")
                        #resultSet of form submission
                        sequence = formMVal.sequence.data
                        measurementList = formMVal.getMeasureList()
                        print(measurementList)


                        conditionList = formMVal.getConditions()

                        if(input.experimentAdd(sequence,conditionList,measurementList,cursor)):
                                 flash("Insertion Successful","success")
                                 mydb.commit()
                        else:
                                 flash("Insertion Failed", "failed")

                        #input.experimentAdd()
                        
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, formFile=formFile)
                        
                        #insertion into database

                elif(request.form["btn"] == "addCond"):
                        formMVal.addCondition()
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, showMeasure="true",formFile=formFile)
                elif(request.form["btn"] == "addMeasure"):
                        formMVal.addMeasure()
                        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal, showMeasure="true",formFile=formFile)
                elif(request.form["btn"] == "fileUpload" and formFile.validate()):
                        print("file upload")
                        if(forms.validateFile(request.files["file"])!= False):
                                # send file to database
                                csvparse.csvInput(request.files["file"],cursor)
                                mydb.commit()
                                flash("File Uploaded Successfully","success")
                        else:
                                flash("File Failed to Upload. Invalid File Type!","failed")

                        
        
        return render_template("input.html",formCond=formCond, formMeasure=formMeasure, formSeq = formSeq, formMVal=formMVal,formFile=formFile)

@app.route("/about", methods =["GET","POST"])
def aboutPage():
        return render_template("about.html")

if __name__ == "__main__":
    app.run()
