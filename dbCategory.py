mysql = None

def set_database(mysql_instance):
  global mysql
  mysql = mysql_instance

def get_connection():
  return mysql.connection

def get_cursor():
  return get_connection().cursor()

def execute(query, params=()):
  cur = get_cursor()
  cur.execute(query, params)
  #return cur.lastrowid
  return cur

def fetchone(query, params=()):
  cur = execute(query, params)
  return cur.fetchone()

def fetchall(query, params=()):
  cur = execute(query, params)
  return cur.fetchall()

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

