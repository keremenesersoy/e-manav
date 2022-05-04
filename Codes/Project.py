import email_validator
from flask import Flask, render_template, flash, url_for, redirect, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt



# Register Form
class RegisterForm(Form):
    Name = StringField("isim",validators=[validators.Length(min=2, max=40)])
    SurName = StringField(validators=[
                          validators.Length(min=2, max=40)])
    Password = PasswordField(validators=[
        validators.DataRequired(message="Lütfen Parola Belirleyin"),
        validators.EqualTo(fieldname="Confirm", message="Parola Uyuşmuyor")
    ])
    Confirm = PasswordField()
    Email = StringField(validators=[validators.Email(
        message="Lütfen geçerli bir e-mail adresi giriniz")])

    Phone = StringField(validators=[validators.Length(max = 13,min = 11)])
    Adress = TextAreaField(validators=[validators.Length(max = 250,min = 0)])
   
app = Flask(__name__)
app.secret_key = "E-MANAV"

@app.route("/")
def index():
    return render_template("indexflask.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():

        Name = form.Name.data
        SurName = form.SurName.data
        Password = form.Password.data
        Email = form.Email.data

        #cursor = mysql.connection.cursor
        redirect(url_for("/"))
    else:
        return render_template("register.html",form = form)


    return render_template("register.html")


app.route("/login",methods = ["GET","POST"])
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
