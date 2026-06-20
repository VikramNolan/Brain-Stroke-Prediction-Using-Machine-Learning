from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib
import pandas as pd
import sqlite3
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# Load the model
try:
    dtc_loaded = joblib.load('decision_tree_model.pkl')
except FileNotFoundError:
    print("⚠️ Model file 'decision_tree_model.pkl' not found. Prediction disabled.")
    dtc_loaded = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                      (username, password, email))
            conn.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'error')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('prediction'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if 'user_id' not in session:
        flash('Please login to access the prediction page.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if dtc_loaded is None:
            flash('Model not loaded. Cannot make prediction.', 'error')
            return redirect(url_for('prediction'))

        # Get form data
        gender = float(request.form['gender'])
        age = float(request.form['age'])
        hypertension = int(request.form['hypertension'])
        heart_disease = int(request.form['heart_disease'])
        ever_married = float(request.form['ever_married'])
        work_type = float(request.form['work_type'])
        residence_type = float(request.form['residence_type'])
        avg_glucose_level = float(request.form['avg_glucose_level'])
        bmi = float(request.form['bmi'])
        smoking_status = float(request.form['smoking_status'])

        # Create DataFrame
        new_data = {
            'gender': [gender],
            'age': [age],
            'hypertension': [hypertension],
            'heart_disease': [heart_disease],
            'ever_married': [ever_married],
            'work_type': [work_type],
            'Residence_type': [residence_type],
            'avg_glucose_level': [avg_glucose_level],
            'bmi': [bmi],
            'smoking_status': [smoking_status]
        }
        new_df = pd.DataFrame(new_data)

        # Predict
        prediction = dtc_loaded.predict(new_df)[0]

        # Store in session to show on result page
        session['prediction'] = int(prediction)
        session['input_data'] = new_data  # optional: to display inputs

        return redirect(url_for('result'))

    return render_template('prediction.html')

@app.route('/result')
def result():
    if 'user_id' not in session:
        flash('Please login to view results.', 'error')
        return redirect(url_for('login'))

    prediction = session.get('prediction')
    if prediction is None:
        flash('No prediction found. Please submit the form first.', 'error')
        return redirect(url_for('prediction'))

    result_text = "Stroke" if prediction == 1 else "No Stroke"
    return render_template('result.html', result=result_text)

if __name__ == '__main__':
    app.run(debug=True)