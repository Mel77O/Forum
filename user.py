from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from category import home

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'forum'

mysql = MySQL(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(f"select username, password from userstbl where username='{username}'")
        user = cur.fetchone()
        cur.close()
        if user and pwd == user[1]:
            session['username'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(f"insert into userstbl (name, username, email, password) values ('{name}', '{username}', '{email}', '{pwd}')")
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT name, email FROM userstbl WHERE username='{username}'")
        user_data = cur.fetchone()
        cur.close()

        if request.method == 'POST':
            new_name = request.form['name']
            new_email = request.form['email']

            cur = mysql.connection.cursor()
            cur.execute(f"UPDATE userstbl SET name='{new_name}', email='{new_email}' WHERE username='{username}'")
            mysql.connection.commit()
            cur.close()

            # Update the session data
            session['name'] = new_name

    except Exception as e:
        # Log the exception
        print(f"An error occurred: {e}")

    return render_template('profile.html', user_data=user_data)



if __name__ == '__main__':
    app.run(debug=True)