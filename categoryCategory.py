from dbCategory import fetchall, fetchone, execute

def create_catuser(data):
  cur = execute("""CALL create_catuser(%s, %s, %s, %s)""",
          (data["category"], data["hashtag"], data["hashtag"], data["date"]))
  row = cur.fetchone()
  data["id"] = row["id"]
  return data

def get_all_catusers():
  rv = fetchall("""SELECT * FROM catusers_view""")
  return rv

def get_catuser_by_id(id):
  rv = fetchone("""SELECT * FROM catusers_view WHERE id = %s""", (id,))
  return rv

def update_catuser(id, data):
  cur = execute("""CALL update_catuser(%s, %s, %s, %s, %s)""",
          (id, data["category"], data["hashtag"], data["hashtag"], data["date"]))
  row = cur.fetchone()
  data["id"] = row["id"]
  return data

def delete_catuser(id):
  cur = execute("""CALL delete_catuser(%s)""", (id,))
  row = cur.fetchone()
  if row is None:
    return True
  return False

## NABUA
# CREATE
def create(data):
  cur = execute("""CALL save_post(%s, %s)""",
          (data["title"], data["content"]))
  row = cur.fetchone()
  data["tid"] = row["tid"]
  return data

    
# GET ALL
def get_post():
    rv = fetchall("""SELECT * FROM post_view""")
    return rv

# GET ONE ID
def get_post_by_id(tid):
    rv = fetchone("""SELECT * FROM post_view WHERE tid = %s""", (tid,))
    if rv is None:
        return {"error":"id doesn't match to any post"}
    return rv
    
## UPDATE
def update(id, data):
    cur = execute("""CALL check_id(%s)""", (id,))
    exist = cur.fetchone()
    print(exist["message"])
    if exist["message"] == 1:
        cur = execute("""CALL update_post(%s, %s, %s)""", (id, data["title"], data["content"]))
        row = cur.fetchone()
        data["tid"] = row["tid"]
        return data
    return {"error": "id doesn't match to any post"}

# DELETE
def delete(id):
    cur = execute("""CALL check_id(%s)""", (id,))
    exist = cur.fetchone()
    print(exist["message"])
    if exist["message"] == 1:
        cur = execute("""CALL delete_post(%s)""", (id,))
        row = cur.fetchone()
        return row
    return {"error":"id doesn't match to any post"}

# CREATE REPLY
def create_reply(data):
    cur = execute("""CALL save_reply(%s, %s, %s, %s)""",
                   (data["post_id"], data["user_id"], data["content"], data["reply_date"]))
    row = cur.fetchone()
    if row:
        data["reply_id"] = row["reply_id"]
        return data
    else:
        return {"error": "Failed to create reply"}

def get_replies_for_post(post_id):
    rv = fetchall("""SELECT * FROM replies WHERE post_id = %s""", (post_id,))
    return rv if rv else [] 
