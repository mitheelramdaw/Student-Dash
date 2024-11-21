import streamlit as st
import sqlite3
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
    
# Dashboard Page (Blank)
def dashboard_page():
    st.title("Dashboard")
    st.write("Welcome to your dashboard!")  # Blank or customized content can go here

# Check session state to control flow
if "authenticated" not in st.session_state:
    # If not authenticated, show the login page
    st.session_state.authenticated = False
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()  # Show login page if not authenticated
elif st.session_state.page == "dashboard" and st.session_state.authenticated:
    dashboard_page()  # Show dashboard if authenticated
