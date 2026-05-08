from flask import Flask, render_template, request, redirect, session
from flask_session import Session

import pickle
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

from wordcloud import WordCloud

from preprocess import clean_text

app = Flask(__name__)

# Secret key
app.secret_key = "sentimentproject"

# Session config
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Load trained model
model = pickle.load(open("sentiment_model.pkl", "rb"))

# Load vectorizer
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------- LOGIN PAGE ---------------- #

@app.route("/")
def login():

    return render_template("login.html")


# ---------------- LOGIN HANDLER ---------------- #

@app.route("/login", methods=["POST"])
def handle_login():

    username = request.form["username"]

    password = request.form["password"]

    # Simple login
    if username == "admin" and password == "admin123":

        session["user"] = username

        return redirect("/home")

    return "Invalid Username or Password"


# ---------------- HOME PAGE ---------------- #

@app.route("/home")
def home():

    if "user" not in session:
        return redirect("/")

    return render_template("index.html")


# ---------------- SINGLE PREDICTION ---------------- #

@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect("/")

    # User input
    text = request.form["text"]

    # Clean text
    cleaned_text = clean_text(text)

    # Convert to vector
    vector_input = vectorizer.transform([cleaned_text])

    # Predict sentiment
    prediction = model.predict(vector_input)[0]

    # Emotion detection
    if prediction == "positive":
        emotion = "😊 Happy"

    elif prediction == "negative":
        emotion = "😡 Angry"

    else:
        emotion = "😐 Neutral"

    # Pie chart
    labels = ["Positive", "Negative", "Neutral"]

    sizes = [0, 0, 0]

    if prediction == "positive":
        sizes = [1, 0, 0]

    elif prediction == "negative":
        sizes = [0, 1, 0]

    else:
        sizes = [0, 0, 1]

    plt.figure(figsize=(4,4))

    plt.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%"
    )

    plt.title("Sentiment Analysis Result")

    # Save chart
    plt.savefig("static/chart.png")

    plt.close()

    # Create Word Cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(cleaned_text)

    # Save word cloud
    wordcloud.to_file("static/wordcloud.png")

    # ---------------- SAVE TO DATABASE ---------------- #

    conn = sqlite3.connect("history.db")

    cursor = conn.cursor()

    cursor.execute(

        """
        INSERT INTO history (
            review,
            prediction,
            emotion
        )

        VALUES (?, ?, ?)
        """,

        (
            text,
            prediction,
            emotion
        )

    )

    conn.commit()

    conn.close()

    # Return result
    return render_template(
        "index.html",
        prediction=prediction,
        emotion=emotion,
        chart="static/chart.png"
    )


# ---------------- CSV UPLOAD ---------------- #

@app.route("/upload", methods=["POST"])
def upload():

    if "user" not in session:
        return redirect("/")

    file = request.files["file"]

    # Read CSV
    df = pd.read_csv(file)

    results = []

    # Analyze reviews
    for review in df["review"]:

        cleaned = clean_text(review)

        vector = vectorizer.transform([cleaned])

        prediction = model.predict(vector)[0]

        results.append(
            {
                "review": review,
                "prediction": prediction
            }
        )

    return render_template(
        "index.html",
        bulk_results=results
    )


# ---------------- ABOUT PAGE ---------------- #

@app.route("/about")
def about():

    if "user" not in session:
        return redirect("/")

    return render_template("about.html")


# ---------------- HISTORY PAGE ---------------- #

@app.route("/history")
def history():

    if "user" not in session:
        return redirect("/")

    # Connect database
    conn = sqlite3.connect("history.db")

    cursor = conn.cursor()

    # Read history
    cursor.execute("SELECT * FROM history")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        history=data
    )


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)