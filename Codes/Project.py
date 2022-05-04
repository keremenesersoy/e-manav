import email_validator
from flask import Flask, render_template, flash, url_for, redirect, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

# Register Form
class RegisterForm(Form):
    Name = StringField("İsim",validators=[validators.Length(min=2, max=40)])
    SurName = StringField("Soyisim",validators=[
                          validators.Length(min=2, max=40)])
    Password = PasswordField("Parola",validators=[
        validators.DataRequired(message="Lütfen Parola Belirleyin"),
        validators.EqualTo(fieldname="Confirm", message="Parola Uyuşmuyor")
    ])
    Confirm = PasswordField("Parola Doğrula")
    Email = StringField("Email",validators=[validators.Email(
        message="Lütfen geçerli bir e-mail adresi giriniz")])

    Phone = StringField("Telefon",validators=[validators.Length(max = 13,min = 11)])
    Adress = TextAreaField("Adres",validators=[validators.Length(max = 250,min = 0)])

class LoginForm(Form):
    e_mail = StringField("Email",validators=[validators.Email(message="Geçerli bir email adresi giriniz")])
    Password = PasswordField("Parola")

app = Flask(__name__)
app.secret_key = "E-MANAV"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["e_mail"]
        return render_template("indexflask.html",usr = user)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():

        Name = form.Name.data
        SurName = form.SurName.data
        Password = form.Password.data
        Email = form.Email.data

        #cursor = mysql.connection.cursor
        redirect(url_for("index"))
    else:
        return render_template("register.html",form = form)

if __name__ == "__main__":
    app.run(debug=True)
