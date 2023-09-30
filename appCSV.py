from flask import Flask, render_template, request
import pandas as pd
import joblib


# Specify the custom static URL path
custom_static_url_path = '/static'

app = Flask(__name__, static_url_path=custom_static_url_path)

# Load your trained model
model = joblib.load('trained_model.pkl')

@app.route("/", methods=["GET", "POST"])
def dashboard():
    return render_template("admin_dashboard.html")



@app.route("/programCSV", methods=["GET", "POST"])
def programCSV():
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

if __name__ == "__main__":
  
    app.run(debug=True)
