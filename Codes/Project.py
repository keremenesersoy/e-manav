from flask import Flask ,render_template,flash,url_for,redirect,session,logging,request

app = Flask(__name__)
app.secret_key = "E-MANAV"

name = "Kerem Enes Ersoys"
name_2 = "Ipek Cidik"
x = 4
@app.route("/")
def index():
    return render_template("indexflask.html")



if __name__ == "__main__":
    app.run(debug=True)
