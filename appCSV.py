from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import joblib

# Specify the custom static URL path
custom_static_url_path = '/static'

app = Flask(__name__, static_url_path=custom_static_url_path)


app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/cesu'
db = SQLAlchemy(app)

# Load your trained model
model = joblib.load('trained_model.pkl')


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route("/", methods=["GET", "POST"])
def main():
    return redirect(url_for('login'))


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


@app.route("/clear_session", methods=["POST"])
def clear_session():
    # Clear the user's session
    session.clear()

    # Respond with a JSON indicating success
    return {"success": True}


@app.route("/admin_dashboard", methods=["GET", "POST"])
def dashboard():
     # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    return render_template("admin_dashboard.html")



@app.route("/programCSV", methods=["GET", "POST"])
def programCSV():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
     
    if request.method == "POST":
        csv_file = request.files["csv_file"]

        if csv_file:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file)

            # Check if the "Species" column exists in the DataFrame
            if "Species" in df.columns:
                # If the "Species" column is present, assume it's the target variable
                target_variable = "Species"
                # Separate features from the target variable
                X = df.drop(target_variable, axis=1)  # Features
                y = df[target_variable]  # Target

                # Use your trained model to make predictions on the features
                predictions = model.predict(X)

                # Add the predictions to the DataFrame
                df["Predictions"] = predictions

            else:
                # If the "Species" column is not present, assume all columns are features
                # Use your trained model to make predictions on the entire DataFrame
                predictions = model.predict(df)

                # Create a new column for predictions in the DataFrame
                df["Predictions"] = predictions

            # Convert the predictions to a Python list
            predictions_list = predictions.tolist()

            return render_template("programCSVresult.html", predictions=predictions_list)

    return render_template("programCSV.html")


@app.route("/programCSVresult", methods=["GET", "POST"])
def programCSVresult():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

if __name__ == "__main__":
  
    app.run(debug=True)
