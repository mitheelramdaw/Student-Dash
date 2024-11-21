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

# Streamlit app
st.title("Login Page")

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
        if check_password(username, password):
            st.success("Login Successful!")
            # Mark user as authenticated in session state
            st.session_state.authenticated = True
            # Show the dashboard after successful login
            st.session_state.page = "dashboard"  # Store the page state as 'dashboard'
        else:
            st.error("Incorrect password.")

# Display Dashboard if user is authenticated
if "authenticated" in st.session_state and st.session_state.authenticated:
    if st.session_state.page == "dashboard":
        st.title("Dashboard")
        st.write("Welcome to your dashboard!")
        # Add dashboard content here (e.g., charts, data, etc.)
else:
    st.write("Please log in.")
