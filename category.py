from flask import Flask, request, jsonify
from categoryCategory import get_all_catusers, get_catuser_by_id, create_catuser, update_catuser, delete_catuser
from flask_mysqldb import MySQL
from dbCategory import set_database
from dotenv import load_dotenv
from os import getenv

app = Flask(__name__)

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
