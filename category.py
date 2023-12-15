import os
from flask import Flask, request, jsonify
from categoryCategory import get_all_catusers, get_catuser_by_id, create_catuser, update_catuser, delete_catuser, get_post, get_post_by_id,create,update,delete
from flask_mysqldb import MySQL
from dbCategory import set_database
from dotenv import load_dotenv
from os import getenv

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


app.config["MYSQL_HOST"] = getenv("MYSQL_HOST")
#app.config["MYSQL_PORT"] = int(getenv("MYSQL_PORT"))
app.config["MYSQL_USER"] = getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = getenv("MYSQL_DB")
# to return results as dictionaries and not an array
app.config["MYSQL_CURSORCLASS"] = getenv("MYSQL_CURSORCLASS")
app.config["MYSQL_AUTOCOMMIT"] = True if getenv("MYSQL_AUTOCOMMIT") == "True" else False

mysql = MySQL(app)
set_database(mysql)

@app.route("/")
def home():
  return "<h1>Forum Category!</h1>"


@app.route("/catusers", methods=["GET", "POST"])
def catusers():
  if request.method == "POST":
    data = request.get_json()
    result = create_catuser(data)
  else:
    result = get_all_catusers()
  return jsonify(result)


@app.route("/catusers/<id>", methods=["GET", "PUT", "DELETE"])
def catusers_by_id(id):
  if request.method == "PUT":
    data = request.get_json()
    result = update_catuser(id, data)
  elif request.method == "DELETE":
    result = get_catuser_by_id(id)
    if result is not None:
      result = delete_catuser(id)
    else:
      result = {"error": "Users Category not found"}
  else:
    result = get_catuser_by_id(id)
  return jsonify(result)

##NABUA

#to create and read the post
@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method=="POST":
        data = request.get_json()
        result = create(data)
        return jsonify(result)
    else:
        result= get_post()
        return jsonify(result) if result else jsonify({"message": "No posts available"})
     
##delete update
@app.route("/post/<post>", methods=["GET", "PUT", "DELETE"])
def post_by_post(post):

    if request.method== "PUT":
        data = request.get_json()
        result = update(post, data)
     
    elif request.method=="DELETE":
        result = delete(post)

    else:
        result = get_post_by_id(post)
    return jsonify(result)
        

@app.route("/post/<post_id>/replies", methods=["GET", "POST"])
def post_replies(post_id):
    if request.method == "POST":
        data = request.get_json()
        data["post_id"] = post_id
        result = create_reply(data)
        return jsonify(result)
    else:
        result = get_replies_for_post(post_id)
        return jsonify(result) if result else jsonify({"message": "No replies for this post"})
