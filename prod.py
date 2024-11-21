import streamlit as st
import sqlite3
import pandas as pd
import bcrypt

# Function to check if the username exists in the database
def check_username(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to check if the password is correct
def check_password(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    stored_password = cursor.fetchone()
    conn.close()

    # If user exists and password matches
    if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
        return True
    return False

# Function to fetch column names from the table
def get_column_names(table_name):
    conn = sqlite3.connect('students.db')  # Connect to your SQLite database
    cursor = conn.cursor()

    # Query to get the column names for the given table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]  # Extracting the column names from the query result
    conn.close()

    return columns

# Function to fetch student data from SQLite
def fetch_student_data(program):
    conn = sqlite3.connect('students.db')  # Connect to your SQLite database
    cursor = conn.cursor()

    # Depending on the selected program, fetch different tables
    if program == 'Diploma in IT':
        table_name = 'diploma_students'
    elif program == 'BSc in IT':
        table_name = 'bsc_students'

    # Get the column names dynamically
    columns = get_column_names(table_name)

    # Fetch data from the respective table
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    conn.close()

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(data, columns=columns)
    return df

# Streamlit App - Login Page
def login_page():
    # Step 1: Username input
    username = st.text_input("Username", "")
    if username:
        user = check_username(username)
        if not user:
            st.error("Username not found. Please try again.")

    # Step 2: Password input
    if username and user:
        password = st.text_input("Password", type='password')
        if password:
            # Step 3: Login button
            if st.button("Login"):
                if check_password(username, password):
                    st.success("Login Successful!")
                    # Mark user as authenticated in session state
                    st.session_state.authenticated = True
                    # Redirect to Dashboard by setting the page state
                    st.session_state.page = "dashboard"
                else:
                    st.error("Incorrect password.")

# Dashboard Page (Student Data)
def dashboard_page():
    # Sidebar for navigation
    program = st.sidebar.radio("Select Program", ["Diploma in IT", "BSc in IT"])

    # Fetch student data based on program selected
    df = fetch_student_data(program)

    # Display title and table on the corresponding page
    st.title(f"Student Data for {program}")
    st.write(f"Showing student details for the {program} program.")

    # Display student data table with dynamic column headers
    st.dataframe(df, use_container_width=True)

# Check session state to control flow
if "authenticated" not in st.session_state:
    # If not authenticated, show the login page
    st.session_state.authenticated = False
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()  # Show login page if not authenticated
elif st.session_state.page == "dashboard" and st.session_state.authenticated:
    dashboard_page()  # Show dashboard if authenticated
