from flask import Flask, render_template, request, redirect
from db import connectToMySQL
app = Flask(__name__)

@app.route('/users')
def index():
    db = connectToMySQL("users")
    users = db.query_db("SELECT * FROM users;")
    print(users)
    return render_template("index.html", all_users=users)

#--------------------CREATE USER--------

@app.route("/users/new")
def addnew():
    db = connectToMySQL("users")
    return render_template("new.html")

@app.route("/users/new", methods=["POST"])
def add_user_to_db():
    db= connectToMySQL('users')
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s,%(ln)s, %(em)s, NOW(), NOW());"
    data = {
        "fn": request.form["first_name"],
        "ln": request.form["last_name"],
        "em": request.form["email"]
    }
    id = db.query_db(query,data)
    return redirect("/users/" + str(id))
     #QUERY: INSERT INTO first_flask (first_name, last_name, occupation, created_at, updated_at) VALUES (fname from form, lname from form, occupation from form, NOW(), NOW());"

#-------------------------------SHOW INFO-----

@app.route("/users/<id>")
def showid(id):
    db= connectToMySQL('users')
    query = ('SELECT * FROM users WHERE ID = %(id)s;')
    data = {
        "id": id
    }
    users =  db.query_db(query,data)
    print(users)
    return render_template("show.html", show_user = users)

#------------------------------EDIT---------------------

@app.route("/users/<id>/edit")
def editshow(id):
    db = connectToMySQL("users")
    query = ('SELECT * FROM users WHERE ID = %(id)s;')
    data = {
        "id": id
    }
    users =  db.query_db(query,data)
    return render_template("edit.html", show_user = users)

@app.route("/users/edit", methods=["POST"])
def update():
    db = connectToMySQL('users')
    query = 'UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s WHERE id = %(id)s'
    data = {
        "fn": request.form["first_name"],
        "ln": request.form["last_name"],
        "em": request.form["email"],
        "id": request.form["id"]
    }
    db.query_db(query,data)
    return redirect("/users")

#-------------------------------DELETE------------------
@app.route("/users/<id>/delete")
def delete(id):
    db = connectToMySQL('users')
    query = 'DELETE FROM users WHERE id = %(id)s'
    data = {
        "id": id
    }
    db.query_db(query,data)
    return redirect("/users")

if __name__=="__main__":
    app.run(debug=True)

