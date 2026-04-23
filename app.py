from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

#Sql connection 
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",        #your sql username
        password="",          # your MySQL password
        database="test_db",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def home():
    #we added this block to fetch data from the users table
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    connection.close()
    #until here
    return render_template("index.html", users=users)

#add a search route sql syntax still
@app.route("/search")
def search():
    query = request.args.get("q", "")   # reads ?q=Alice from the URL
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE name LIKE %s",
            (f"%{query}%",)
        )
        results = cursor.fetchall()
    connection.close()
    return render_template("search.html", results=results, query=query)

#add a post Route ADDING/CREATING
@app.route("/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]    # reads from the form
        email = request.form["email"]
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (name, email)
            )
        connection.commit()   # IMPORTANT: saves the change
        connection.close()
        return redirect("/")  # go back to home page
    return render_template("add.html")
    #add redirect import at the top 

#delete route, note that a route is like a function
@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    connection.commit()
    connection.close()
    return redirect("/")

#initialize the application
if __name__ == "__main__":
    app.run(debug=True)