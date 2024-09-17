from flask import Flask, render_template, flash
from flask import request, make_response
from flask import redirect, send_file
from werkzeug.utils import secure_filename
from markupsafe import escape
from helper import hash
from db import *

server = Flask(__name__)

hashes = set()  # {hash1,hash2}
users = dict()  # {hash1:username1,hash2:username2}
files = dict()  # {hash1:[file1,fil2],hash2:[]}


@server.route("/aleena")
def hello_world():
    return "<h1>Hello,World aleena!</h1>"


def slash():
    return "<h1>ALEENA</h1>"


@server.route("/amal")
def amal():
    return "<marquee direction='right' ><h1>Stupid fool AMAL</h1></marquee>"


@server.route("/<name>")
def greeting(name):
    return f"hello <h1>{escape(name)}</h1>"


@server.route("/<name>/<int:age>")
def age(name, age):
    return f"hello <h1>{escape(name)}</h1><br><h4>your current age is <h1>{escape(age)}</h1></h4> <h4>your age after 10 years will br <h1>{escape(age+10)}</h1></h4>"


@server.route("/", methods=["POST", "GET"])
@server.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        hash_hex = request.cookies.get("hash_hex", None)
        if hash_hex == None:
            return render_template("login.html")
        else:
            return "<h2>you are already logged in  <a href='/user'><button>user</button></a></h2>"

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hash_hex = hash(username + password)

        hash_id = get_hash_id_from_hash(hash_hex)
        if hash_id == None:
            add_hash_entry(hash_hex)
            hash_id = get_hash_id_from_hash(hash_hex)
            add_user_entry(username, hash_id)
        resp = make_response(redirect("/user"))
        resp.set_cookie("hash_hex", hash_hex)
        return resp

        # if hash_hex not in hashes:
        #     hashes.add(hash_hex)
        #     files.update({hash_hex: []})

        #     resp = make_response(redirect("/user"))
        #     resp.set_cookie("hash_hex", hash_hex)
        #     return resp

        # else:
        #     resp = make_response(redirect("/user"))
        #     resp.set_cookie("hash_hex", hash_hex)
        #     return resp


@server.route("/user")
def user():
    hash_hex = request.cookies.get("hash_hex", None)
    if hash_hex == None:
        return redirect("/login")
    hash_id = get_hash_id_from_hash(hash_hex)
    file_names = get_files_from_hash_id(hash_id)
    if file_names == None:
        file_names = []
    # file_names = files[hash_hex]
    # for i in range(len(file_names)):
    #     file_names[i] = file_names[i].replace(hash_hex + "__", "")
    #     file_names[i] = file_names[i].replace("downloads/", "")
    return render_template(
        "user.html",
        username=get_username_from_hash_id(hash_id),
        hash=hash_hex,
        files=file_names,
    )


@server.route("/logout")
def logout():
    hash_hex = request.cookies.get("hash_hex", None)
    if hash_hex == None:
        return redirect("/login")
    resp = make_response(redirect("/login"))
    resp.delete_cookie("hash_hex")

    return resp


@server.route("/upload", methods=["GET", "POST"])
def upload():
    hash_hex = request.cookies.get("hash_hex", None)
    if hash_hex == None:
        return redirect("/login")
    if request.method == "GET":
        return render_template("upload.html")
    elif request.method == "POST":
        file = request.files["file"]
        file_name = f"downloads/{hash_hex}__{secure_filename(file.filename)}"
        file.save(file_name)
        hash_id = get_hash_id_from_hash(hash_hex)
        add_file_entry(secure_filename(file.filename), hash_id)
        # files.update({hash_hex: files[hash_hex] + [file_name]})
        return redirect("/user")


# @server.route("/myfiles")
# def my_files():
#     hash_hex = request.cookies.get("hash_hex", None)
#     if hash_hex == None:
#         return redirect("/login")
#     file_names = files[hash_hex]
#     for i in range(len(file_names)):
#         file_names[i] = file_names[i].replace(hash_hex + "__", "")
#     return render_template("myfiles.html", files=file_names)


@server.route("/files/<file_name>")
def view_file(file_name):
    hash_hex = request.cookies.get("hash_hex", None)
    if hash_hex == None:
        return redirect("/login")
    file_name_og = "downloads/" + hash_hex + "__" + file_name
    return send_file(file_name_og, download_name=file_name)


@server.route("/files/<file_name>/delete")
def delete_file_view(file_name):
    hash_hex = request.cookies.get("hash_hex", None)
    if hash_hex == None:
        return redirect("/login")
    hash_id = get_hash_id_from_hash(hash_hex)
    delete_file(file_name, hash_id)
    return redirect("/user")
