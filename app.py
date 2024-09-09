from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from config import db_config
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)  # Secure secret key for session management

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

# Route to serve the Login Page and handle login functionality
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password'] 

        try:
            # Connect to the Database
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            # Check if the user exists and password matches
            query = "SELECT * FROM clients WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()

            if user:
                # Store user info in session
                session['user_id'] = user['id']
                session['email'] = user['email']
                session['full_name'] = f"{user['first_name']} {user['last_name']}"  

                cursor.close()
                connection.close()

                # Redirect to the dashboard
                return redirect(url_for('dashboard'))

            else:
                cursor.close()
                connection.close()
                return jsonify({'error': 'Invalid Email or Password'}), 401

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Render the login page if the request method is GET
    return render_template('login.html')

# Route to serve the Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:  # If user is logged in
        full_name = session.get('full_name', 'user')
        return render_template('dashboard.html', full_name = full_name)  
    else:  # If user is not logged in
        return redirect(url_for('login'))

# Route to serve the registration form
@app.route('/')
def index():
    return render_template('register.html')

# Route to handle form submission (registration)
@app.route('/register', methods=['POST'])
def register_user():
    # Get form data
    first_name = request.form['FirstName']
    last_name = request.form['LastName']
    register_as = request.form['RegisterAs']
    company_name = request.form['CompanyName']
    email = request.form['Email']
    mobile_number = request.form['MobileNumber']
    password = request.form['Password']

    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the data into the MySQL database, with client_id and client_secret as NULL
        query = """INSERT INTO clients (first_name, last_name, register_as, company_name, email, mobile_number, password, client_id, client_secret)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, NULL)"""
        values = (first_name, last_name, register_as, company_name, email, mobile_number, password)
        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        # Return success message
        return render_template('registrationSuccess.html')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle Logout
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))  # Redirect to login page

if __name__ == '__main__':
    app.run(debug=True)
