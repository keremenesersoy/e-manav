from flask import Flask ,render_template

app = Flask(__name__)

name = "Kerem Enes Ersoy"
name_2 = "Ipek Cidik"

@app.route("/")
def index():
    return render_template("indexflask.html", name1 = name , name_2 = name_2)

if __name__ == "__main__":
    app.run(debug=True)
