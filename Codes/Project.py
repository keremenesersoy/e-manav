<<<<<<< HEAD
from flask import Flask ,render_template,flash,url_for,redirect,session,logging,request
=======
import email_validator
from flask import Flask, render_template, flash, url_for, redirect, session, logging, request
>>>>>>> f711e109fc20a7de42db525a4066d949db733a43
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
<<<<<<< HEAD
import email_validator

=======
>>>>>>> f711e109fc20a7de42db525a4066d949db733a43


# Register Form
class RegisterForm(Form):
    Name = StringField("İsim :", validators=[validators.Length(min=2, max=40)])
    SurName = StringField("Soyisim :", validators=[
                          validators.Length(min=2, max=40)])
    Password = PasswordField("Parola :", validators=[
        validators.DataRequired(message="Lütfen Parola Belirleyin"),
        validators.EqualTo(fieldname="Confirm", message="Parola Uyuşmuyor")
    ])
    Confirm = PasswordField("Parola Doğrula :")
    Email = StringField("Email :", validators=[validators.Email(
        message="Lütfen geçerli bir e-mail adresi giriniz")])


app = Flask(__name__)
app.secret_key = "E-MANAV"

name = "Kerem Enes Ersoys"
name_2 = "Ipek Cidik"
x = 4


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
<<<<<<< HEAD
        redirect(url_for("/"))
    else:
        return render_template("register.html",form = form)
=======

    return render_template("register.html")
>>>>>>> f711e109fc20a7de42db525a4066d949db733a43


if __name__ == "__main__":
    app.run(debug=True)
