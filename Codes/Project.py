from flask import Flask ,render_template,flash,url_for,redirect,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
import email_validator

class RegisterForm(Form):
    name = StringField("İsim Soyisim:",validators=[validators.Length(min = 4 , max = 5 , message="")]) 
    username = StringField("Kullanici Adi:",validators=[validators.Length(min = 4 , max = 5 , message="")])
    email = StringField("E-mail:",validators=[validators.Email(message = "Lutfen gecerli bir email adresi giriniz")])
    password = PasswordField("Parola:",validators=[
        validators.DataRequired(message="Lutfen parola belirleyin") , validators.EqualTo(fieldname = "confirm" , message="Parola Uyusmuyor")
        ])
    confirm = PasswordField("Parola Dogrula")
app = Flask(__name__)

islem = 3

#app.config["MYSQL_HOST"] = "localhost"
#app.config["MYSQL_USER"] = "root"   
#app.config["MYSQL_PASSWORD"] = parola
#app.config["MYSQL_DB"] = "myblog"   
#app.config["MYSQL_CURSORCLASS"] = "DictCursor" 
                                               

#mysql = MySQL(app)


@app.route("/")
def index():
    numbers = [1,2,3,4,5]
    dict_ = [
        {"id":1 , "title":"deneme1" , "content":"deneme1 içerik"},
        {"id":2 , "title":"deneme2" , "content":"deneme2 içerik"},
        {"id":3 , "title":"deneme3" , "content":"deneme3 içerik"}
    ]
    return render_template("indexflask2.html",answer = "evett" , islem = islem , numbers = numbers , dict_ = dict_)

@app.route("/about")
def about():
   return render_template("about.html")

@app.route("/article/<string:id>") 
def detail(id):                                                 
    return "bu sayfanın idsi = " + id
    
#Register
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST":
        pass
    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)