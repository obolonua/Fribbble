import os
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

# configure upload folder
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    q = request.args.get("q")
    if q:
        pictures = db.search_pictures(q)
    else:
        pictures = db.get_pictures()
    return render_template("index.html", pictures=pictures, search_query=q)

@app.route("/new_picture")
def new_picture():
    return render_template("new_picture.html")

@app.route("/create_picture", methods=["POST"])
def create_picture():
    name = request.form["name"]
    description = request.form["description"]
    style = request.form["style"]
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    file = request.files.get("picture")
    file_path = None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        # store relative path for later display
        file_path = "/" + file_path  

    db.add_picture(name, description, style, user_id, file_path)

    return redirect("/")

@app.route("/edit/<int:picture_id>")
def edit_picture(picture_id):
    picture = db.get_picture(picture_id)
    return render_template("edit.html", picture = picture)

@app.route("/update_picture", methods=["POST"])
def update_picture():
    print("first")
    name = request.form["name"]
    description = request.form["description"]
    style = request.form["style"]
    user_id = session.get("user_id")
    picture_id = request.form["picture_id"]

    if not user_id:
        return redirect("/login")

    file = request.files.get("picture")
    file_path = None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        file_path = "/" + file_path  

    db.update_picture(name, description, style, user_id, file_path, picture_id)

    return redirect("/picture/" + str(picture_id))

@app.route("/delete_picture/<int:picture_id>", methods=["POST"])
def delete_picture(picture_id):
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    db.delete_picture(picture_id, user_id)
    return redirect("/")

@app.route("/picture/<int:picture_id>")
def show_picture(picture_id):
    picture = db.get_picture(picture_id)
    return render_template("picture.html", picture=picture)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")    
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        results = db.query(sql, [username])

        if not results:
            return "VIRHE: väärä tunnus tai salasana"
        
        result = results[0]
        
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect("/")