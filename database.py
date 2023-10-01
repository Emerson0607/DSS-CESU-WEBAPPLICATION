from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/cesu'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check the username and password against the database (replace with actual database query)
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Store the user's ID in the session to keep them logged in
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
