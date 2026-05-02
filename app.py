import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

# SQLAlchemy config — replaces get_connection()
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# This replaces your CREATE TABLE — SQLAlchemy knows your table structure now
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Home — fetch all users
@app.route("/")
def home():
    users = User.query.all()
    return render_template("index.html", users=users)

# Search
@app.route("/search")
def search():
    query = request.args.get("q", "")
    results = User.query.filter(User.name.like(f"%{query}%")).all()
    return render_template("search.html", results=results, query=query)

# Add user
@app.route("/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    return render_template("add.html")

# Delete user
@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)