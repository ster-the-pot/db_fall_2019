from flask import Flask, render_template, request

from wtforms import Form,StringField,TextAreaField,validators

app = Flask(__name__)
app.debug= True


@app.route("/")
def homePage():
        return render_template('index.html')

@app.route("/input")
def aboutPage():
        return render_template("input.html")

class AddConditionForm(Form):
        conditions = StringField('Name', validators=[validators.Length(min=1,max=50)])
        username = StringField('Username', validators=[validators.Length(min=4,max=25)])

if __name__ == "__main__":
    app.run()
