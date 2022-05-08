from re import X
import email_validator
from flask import Flask, render_template, flash, url_for, redirect, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import jyserver.Flask as jyf



#Kullanıcı Giriş Decoratarı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu Sayfayı Görüntülemek İçin Lütfen Giriş Yapın",category="danger")
            return redirect(url_for("login"))
    return decorated_function

fruits = {
    "Ananas" : 15,
    "Avokado" : 6,
    "Armut" : 11,
    "Cilek" : 30,
    "Elma" : 5,
    "Erik" : 35,
    "Karpuz" : 8,
    "Kavun" : 7,
    "Kiraz" : 12,
    "Kivi" : 14,
    "Limon" : 10,
    "Mandalina" : 6,
    "Mango" : 16,
    "Muz" : 16,
    "Portakal" : 7,
    "Incir" : 10,
    "Seftali" : 13,
    "Uzum" : 8
}
vegetables = {
    "Barbunya" : 12,
    "Biber" : 18,
    "Domates" : 14,
    "Fasulye" : 27,
    "Havuc" : 4,
    "Ispanak" : 13,
    "Kabak" : 2,
    "Lahana" : 11,
    "Marul" : 4,
    "Maydanoz" : 2,
    "Patates" : 5,
    "Patlican" : 9,
    "Salatalik" : 8,
    "Sarimsak" : 21,
    "Sogan" : 4
}

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

    Phone = StringField("Telefon",validators=[validators.Length(max = 13,min = 10)])
    Adress = TextAreaField("Adres",validators=[validators.Length(max = 250,min = 0)])

app = Flask(__name__)


app.config["MYSQL_HOST"] = "localhost" 
app.config["MYSQL_USER"] = "root"  
app.config["MYSQL_PASSWORD"] = "projesifre123"
app.config["MYSQL_DB"] = "e_manav"   
app.config["MYSQL_CURSORCLASS"] = "DictCursor"  
app.secret_key = "E_MANAV"                                     
mysql = MySQL(app)


@jyf.use(app)
class App:
    def increment(self , fruit):
        
        print(fruit)
        #session["selectfruit"] = self.js.document.getElementById('fruit').innerHTML
        #print(session["selectfruit"])
        


@app.route("/")
def index():
    session["status"] = "homepage"
    return render_template("homepage.html")

@app.route("/login",methods = ["GET","POST"])
def login():
    session["status"] = "login"
    if request.method == "POST":
        e_mail = request.form["e_mail"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        query = f"select * from users where email = '{e_mail}'"

        result = cursor.execute(query)

        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]

            if sha256_crypt.verify(password,real_password):
                session["logged_in"] = True
                session["name"] = data["name"].title()
                session["email"] = data["email"]
                flash(f"Hoşgeldin {session['name']}" , category="success")
                cursor.close()
                return redirect(url_for("index"))
            else:
                flash("Şifre Yanlış" , category="danger")
                cursor.close()
                return redirect(url_for("login"))

        else:
            flash("Böyle Bir Kullanıcı Bulunmuyor" , category="danger")
            cursor.close()
            return redirect(url_for("login"))        
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session["status"] = "register"

    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():

        Name = form.Name.data
        SurName = form.SurName.data
        Password = sha256_crypt.encrypt(form.Password.data)
        Email = form.Email.data
        Number = form.Phone.data
        Adress = form.Adress.data

        cursor = mysql.connection.cursor()
        query = f"Insert into users(name,surname,password,email,number,adress) VALUES('{Name}','{SurName}','{Password}','{Email}','{Number}','{Adress}')"

        cursor.execute(query)
        mysql.connection.commit()
        cursor.close()

        flash("Başarı İle Kayıt Oldunuz" , category="success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form = form)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Başarı İle Çıkış Yapıldı" , category="success")
    return redirect(url_for("index"))

@app.route("/basket",methods = ["GET" , "POST"])
def basket():
    session["status"] = "basket"
    return render_template("basket.html") 

@app.route("/myaccount")
@login_required
def myaccount():
    session["status"] = "myaccount"
    return render_template("myaccount.html")

@app.route("/meyvelermenu" , methods = ["GET","POST"])
def meyveler():
    
    session["status"] = "meyvelermenu"
    if request.method == "POST":
        session["Mmiktar"] = request.form["bakiye"]
        return redirect(url_for("calculate_fruit"))
    else:
        return App.render(render_template("meyvelermenu.html"))

@app.route("/sebzelermenu" , methods = ["GET" , "POST"])
def sebzeler():
    session["status"] = "sebzelermenu"
    if request.method == "POST":
        session["Smiktar"] = request.form["bakiye"]
        return redirect(url_for("calculate_vegetable"))
    else:
        return render_template("sebzelermenu.html")

@app.route("/calculate_fruit" , methods = ["GET","POST"])
def calculate_fruit():
    print(session["Mmiktar"])
    return render_template("basket.html")

@app.route("/calculate_vegetable" , methods = ["GET","POST"])
def calculate_vegetable():
    print(session["Smiktar"])
    return render_template("basket.html")

if __name__ == "__main__":
    app.run(debug=True)