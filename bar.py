import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import bcrypt
import random

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
    if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
        return True
    return False

# Streamlit App - Login Page
def login_page():
    username = st.text_input("Username", "")
    if username:
        user = check_username(username)
        if not user:
            st.error("Username not found. Please try again.")
    
    if username and user:
        password = st.text_input("Password", type='password')
        if password:
            if st.button("Login"):
                if check_password(username, password):
                    st.session_state.authenticated = True
                    st.session_state.page = "dashboard"
                else:
                    st.error("Incorrect password.")

# Dashboard Page
def dashboard_page():
    st.title("Dashboard")
    st.write("Welcome to your dashboard!")
    
    # Dropdown to select the program (BSc or DIT)
    program = st.selectbox("Select Program", ["Diploma in IT", "BSc in IT"])

    # Fetching data based on program selection
    df = fetch_student_data(program)

    # Displaying student data table
    st.dataframe(df)
    
    st.write("\n\n")

    
    st.markdown("---")
    
    st.write("\n\n\n")
    st.write("\n\n")
    
    # Plotting the best scores
    plot_best_scores(df, program)

# Function to fetch student data from SQLite
def fetch_student_data(program):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    if program == 'Diploma in IT':
        table_name = 'diploma_students'
    elif program == 'BSc in IT':
        table_name = 'bsc_students'

    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [description[0] for description in cursor.description]  # Get column names
    data = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(data, columns=columns)
    return df
    
    


# Plotting the best scores with unique colors for each student
def plot_best_scores(df, program):
    module_columns = [col for col in df.columns if col not in ['STUDENT_NUMBER', 'STUDENT_NAME']]
    best_scores = df[module_columns].max()

    # Create a color palette for students
    student_names = df['STUDENT_NAME'].unique()
    
    # Generate a list of unique colors based on the program (BSc or DIT)
    if program == 'Diploma in IT':
        student_colors = {name: random.choice(['#39FF14', '#00FFFF', '#1E90FF', '#FF00FF', '#00FF00', '#00BFFF']) 
                        for name in student_names}
    elif program == 'BSc in IT':
        student_colors = {name: random.choice(['#39FF14', '#00FFFF', '#1E90FF', '#FF00FF', '#00FF00', '#00BFFF']) 
                        for name in student_names}



    # Create the figure and axis with dark background
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set background color for the figure and axes
    fig.patch.set_facecolor('black')  # Set the figure background to black
    ax.set_facecolor('black')  # Set the axis background to black

    # Loop through each student to create bars with their respective color
    for idx, student in df.iterrows():
        student_name = student['STUDENT_NAME']
        color = student_colors.get(student_name, 'gray')  # Default to gray if not in mapping
        ax.bar(module_columns, student[module_columns], label=student_name, color=color)

    # Add title, labels, and legend with white text
    ax.set_title(f"Best Scores for {program} Students", color='white')
    ax.set_ylabel("Marks", color='white')
    ax.set_xlabel("Modules", color='white')

    # Customize ticks and gridlines for dark mode
    ax.tick_params(axis='both', colors='white')  # Change tick marks to white
    ax.grid(True, which='both', axis='y', color='white', linestyle='--', linewidth=0.5)  # Add gridlines

    # Create a custom legend with white text for the student names
    handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in student_colors.values()]
    labels = [student for student in student_colors.keys()]
    ax.legend(handles, labels, title="Students", title_fontsize='small', loc='upper left', bbox_to_anchor=(1.05, 1), 
              frameon=False, fontsize='small', framealpha=0.3, labelcolor='white')

    # Display the plot with dark theme
    st.pyplot(fig)

# Main app control
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard" and st.session_state.authenticated:
    dashboard_page()
