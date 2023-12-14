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
    if 'tid' in data: 
        cur = execute("""CALL save_post(%s, %s, %s)""", (data['tid'], data["title"], data["content"]))
        row = cur.fetchall()
        
        if row:
            data["tid"] = row["tid"]  # Corrected: use row["tid"] instead of row["id"]
            return data
        else:
            # Handle error or return None
            return None
    else:
        # Handle error or return None
        return None

    
# GET ALL
def get_post():
    rv = fetchall("""SELECT * FROM post_view""")
    return rv
# GET ONE ID
def get_pos_by_id(id):
    rv = fetchone("""SELECT * FROM post_view WHERE tid = %s""", (id,))
    return rv
    
## UPDATE
def update(id, data):
    if 'tid' in data: 
        cur = execute("""CALL update_post(%s, %s, %s)""", (data['tid'], data["title"], data["content"]))
        row = cur.fetchall()
        
        if row:
            data["tid"] = row["tid"]  # Corrected: use row["tid"] instead of row["id"]
            return data
        else:
            # Handle error or return None
            return None
    else:
        # Handle error or return None
        return None

# DELETE
def delete(id):
    cur = execute("""CALL delete_post(%s)""", (id,))
    row = cur.fetchone()
    if row is None:
        return True
    return False


