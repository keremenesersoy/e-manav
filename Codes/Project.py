from tkinter.tix import Form
from flask import Flask ,render_template,flash,url_for,redirect,session,logging,request

#Register Form
class RegisterForm(Form):
    pass


app = Flask(__name__)
app.secret_key = "E-MANAV"

name = "Kerem Enes Ersoys"
name_2 = "Ipek Cidik"
x = 4

@app.route("/")
def index():
    return render_template("indexflask.html")

@app.route("/register")
def register():
    return render_template("register.html")



if __name__ == "__main__":
    app.run(debug=True)
