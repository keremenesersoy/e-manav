import email_validator
from flask import Flask, render_template, flash, url_for, redirect, session, logging, request
from flask_mysqldb import MySQL
from regex import F
from requests import RequestException
from sqlalchemy import true
from sympy import product
from urllib3 import Retry
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

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
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "e_manav"   
app.config["MYSQL_CURSORCLASS"] = "DictCursor"  
app.secret_key = "E_MANAV"                                     
mysql = MySQL(app)

TOTAL = 0

products = {
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
    "Uzum" : 8,
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


def sql_ChangeFunc(query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()
    cursor.close()

def sql_SelectFunc(query):
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    
    return data


@app.route("/")
def index():
    session["status"] = "homepage"
    return render_template("homepage.html")

@app.route("/login",methods = ["GET","POST"])
def login():
    session["status"] = "login"
    if request.method == "POST":
        e_mail = request.form["e_maill"]
        password = request.form["passwordd"]

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
    query = "select * from urun"
    data = sql_SelectFunc(query)
    query = "select islem_tutar from urun"
    toplam = sql_SelectFunc(query)
    result = 0
    for i in toplam:
        result += i['islem_tutar']
    print(len(data))
    
    session["TF"] = True
    if len(data) == 0:
        session["TF"] = False
    
    return render_template("basket.html" , datas = data , toplam = result) 


@app.route("/myaccount")
@login_required
def myaccount():
    session["status"] = "myaccount"
    return render_template("myaccount.html")

@app.route("/meyvelermenu" , methods = ["GET","POST"])
def meyveler():  
    session["status"] = "meyvelermenu"
    if request.method == "POST":
        print(request.form["product"])
        print(request.form["bakiye"])
        urun_isim = request.form["product"]
        adet = request.form["bakiye"]
        fiyat = products[urun_isim]
        img_url = "static/img/" + urun_isim.lower() + ".jpg"
        islem_tutar = int(fiyat) * int(adet)

        data = sql_SelectFunc("select urun_isim from urun")
        ui = []
        for i in data:
            ui.append(i['urun_isim'])
        
        if urun_isim in ui:
            data = sql_SelectFunc(f"select adet from urun where urun_isim = '{urun_isim}'")
            a = []
            for i in data:
                a.append(i['adet'])
            adet = int(a[0]) + int(adet)
            query = f"update urun set adet = {adet} , islem_tutar = {adet * int(fiyat)} where urun_isim = '{urun_isim}'"
            sql_ChangeFunc(query)
        else:
            query = f"insert into urun(urun_isim,islem_tutar,fiyat,img_url,adet) values('{urun_isim}',{islem_tutar},{fiyat},'{img_url}',{adet})"
            sql_ChangeFunc(query)
            
        return redirect(url_for("basket"))
    else:
        return render_template("meyvelermenu.html")

@app.route("/sebzelermenu" , methods = ["GET" , "POST"])
def sebzeler():
    session["status"] = "sebzelermenu"
    if request.method == "POST":
        print(request.form["bakiye"])
        print(request.form["product"])
        
        urun_isim = request.form["product"]
        adet = request.form["bakiye"]
        fiyat = products[urun_isim]
        img_url = "static/img/" + urun_isim.lower() + ".jpg"
        islem_tutar = int(fiyat) * int(adet)

        data = sql_SelectFunc("select urun_isim from urun")
        ui = []
        for i in data:
            ui.append(i['urun_isim'])
        
        if urun_isim in ui:
            data = sql_SelectFunc(f"select adet from urun where urun_isim = '{urun_isim}'")
            a = []
            for i in data:
                a.append(i['adet'])
            adet = int(a[0]) + int(adet)
            query = f"update urun set adet = {adet} , islem_tutar = {adet * int(fiyat)} where urun_isim = '{urun_isim}'"
            sql_ChangeFunc(query)
        else:
            query = f"insert into urun(urun_isim,islem_tutar,fiyat,img_url,adet) values('{urun_isim}',{islem_tutar},{fiyat},'{img_url}',{adet})"
            sql_ChangeFunc(query)
        return redirect(url_for("basket"))
    else:
        return render_template("sebzelermenu.html")

@app.route("/delete" , methods = ["GET" , "POST"])
def delete():
    if request.method == "POST":
        delete = request.form['delete'].lower()
        query = f"delete from urun where urun_isim = '{delete}'"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('basket'))
    return render_template("basket.html")


if __name__ == "__main__":
    app.run(debug=True)