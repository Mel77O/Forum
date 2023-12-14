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