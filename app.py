from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'temporary_key'  # Replace with a strong secret key

# Database Connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='clonedb.cpgiuyek40pg.us-east-1.rds.amazonaws.com',
        user='admin',
        password='RadhaKrishna&34',
        database='clone_db'
    )
    return connection

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id']= username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    course_urls = [
        'https://clonebucket-1.s3.us-east-1.amazonaws.com/Python_Code%2B1.pdf',
        'https://clonebucket-1.s3.us-east-1.amazonaws.com/PYTHON%2Bprogramming%2Bcode.pdf'
    ]
    return render_template('dashboard.html', course_urls=course_urls)

# Home Route (Landing Page)
@app.route('/')
def home():
    return render_template('home.html')

# Logout
@app.route('/logout')
def logout():
    #session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
