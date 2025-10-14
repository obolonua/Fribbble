import os
import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import db
import config
import users
import pictures

app = Flask(__name__)
app.secret_key = config.secret_key

# configure upload folder
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def check_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    q = request.args.get("q")
    if q:
        all_pictures = pictures.search_pictures(q)
    else:
        all_pictures = pictures.get_pictures()
    return render_template("index.html", pictures=all_pictures, search_query=q)

@app.route("/user/<int:user_id>")
def user_page(user_id):
    check_login()
    user = users.get_user(user_id)
    if not user:
        abort(404)
    publications = users.get_user_pictures(user_id)
    if not user:
        abort(404)
    return render_template("user.html", user=user, publications=publications)

@app.route("/new_picture")
def new_picture():
    check_login()
    classes = pictures.get_all_classes()
    return render_template("new_picture.html", classes=classes)

@app.route("/create_picture", methods=["POST"])
def create_picture():
    check_login()
    allowed_specs = pictures.get_all_classes()
    name = request.form["name"]
    if not name or len(name) > 50:
        abort(403)

    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)

    user_id = session.get("user_id")

    style = request.form["style"]
    print(style)

    style = request.form["style"].split(":")[1]
    classes = []
    for item in request.form.getlist("style"):
        if item:
            title, value = item.split(":")
            if title not in allowed_specs or value not in allowed_specs[title]:
                abort(403)

            classes.append((title, value))

    file = request.files.get("picture")
    file_path = None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        file_path = "/" + file_path  

    pictures.add_picture(name, description, style, classes, user_id, file_path)

    return redirect("/")

@app.route("/edit/<int:picture_id>")
def edit_picture(picture_id):
    check_login()
    picture = pictures.get_picture(picture_id)
    if not picture:
        abort(404)
    if picture["user_id"] != session["user_id"]:
        abort(403)

    all_classes = pictures.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = "" 
    for entry in pictures.get_specs(picture_id):
        classes[entry["title"]] = entry["style"]

    return render_template("edit.html", picture = picture, classes = classes, all_classes = all_classes)

@app.route("/update_picture", methods=["POST"])
def update_picture():
    check_login()
    allowed_specs = pictures.get_all_classes
    picture_id = request.form["picture_id"]
    picture = pictures.get_picture(picture_id)
    if not picture:
        abort(404)
    name = request.form["name"]
    if not name or len(name) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    style = request.form["style"]
    user_id = session.get("user_id")
    picture_user_id = int(request.form["user_id"])

    if picture_user_id != user_id:
        abort(403)

    classes = []
    for item in request.form.getlist("style"):
        if item:
            title, value = item.split(":")
            if title not in allowed_specs or value not in allowed_specs[title]:
                abort(403)
            classes.append((title, value))

    file = request.files.get("picture")
    file_path = None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        file_path = "/" + file_path  

    pictures.update_picture(name, description, style, user_id, file_path, picture_id, classes)
    return redirect("/picture/" + str(picture_id))

@app.route("/delete_picture/<int:picture_id>", methods=["POST"])
def delete_picture(picture_id):
    check_login()
    picture = pictures.get_picture(picture_id)
    if not picture:
        abort(404)
    user_id = session.get("user_id")

    pictures.delete_picture(picture_id, user_id)
    return redirect("/")

@app.route("/picture/<int:picture_id>")
def show_picture(picture_id):
    check_login()
    picture = pictures.get_picture(picture_id)
    if not picture:
        abort(404)
    picture_specs = pictures.get_specs(picture_id)
    return render_template("picture.html", picture=picture, picture_specs=picture_specs)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    check_login()
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