import os
from flask import Flask, request, jsonify
from categoryCategory import get_all_catusers, get_catuser_by_id, create_catuser, update_catuser, delete_catuser, get_post, get_post_by_id,create,update,delete,add_reply_to_post
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
        

##reply

# New route to create a post and add a reply
@app.route("/post", methods=["POST"])
def create_post_and_reply():
    if request.method == "POST":
        data = request.get_json()

        # Create the post
        result_post = create(data)

        # Check if the post creation was successful
        if "error" in result_post:
            return jsonify(result_post), 400

        # Add a reply to the created post
        reply_data = {"Content": "This is a new reply to the post", "OriginalMessageID": result_post["tid"]}
        result_reply = add_reply_to_post(result_post["tid"], reply_data)

        # Check if the reply addition was successful
        if "error" in result_reply:
            return jsonify(result_reply), 400

        return jsonify({"message": "Post and reply added successfully"})

    return jsonify({"error": "Invalid request"}), 400
