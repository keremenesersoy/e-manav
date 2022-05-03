from flask import Flask ,render_template,flash,url_for,redirect,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
import email_validator
from functools import wraps


app = Flask(__name__)
app.secret_key = "E-MANAV"

name = "Kerem Enes Ersoys"
name_2 = "Ipek Cidik"
x = 4
@app.route("/")
def index():
    return render_template("indexflask.html", name1 = name , name_2 = name_2 , sayi = x)



if __name__ == "__main__":
    app.run(debug=True)
