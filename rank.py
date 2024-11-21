import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
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

    # Dropdown to select module for filtering
    module = st.selectbox("Select Module", df.columns[2:])  # Assuming the first two columns are student info

    # Slider for minimum score
    min_score = st.slider("Minimum Marks", min_value=0, max_value=100, value=50)

    # Filter students based on the selected module and minimum marks
    filtered_df = df[df[module] >= min_score]

    # Displaying filtered student data
    st.dataframe(filtered_df)

    # Plotting the best scores
    plot_best_scores(filtered_df, program)

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

# Plotting the best scores with unique colors for each student using Plotly
def plot_best_scores(df, program):
    module_columns = [col for col in df.columns if col not in ['STUDENT_NUMBER', 'STUDENT_NAME']]
    best_scores = df[module_columns].max()

    # Create a color palette for students (only 3 colors)
    student_names = df['STUDENT_NAME'].unique()
    color_palette = ['#FF5733', '#33FF57', '#3357FF']  # 3 distinct colors

    # Map students to these colors using modulo operation to cycle through the colors
    student_colors = {name: color_palette[i % len(color_palette)] for i, name in enumerate(student_names)}

    # Create a Plotly bar chart
    fig = go.Figure()

    # Loop through each student to create bars with their respective color
    for idx, student in df.iterrows():
        student_name = student['STUDENT_NAME']
        color = student_colors.get(student_name, 'gray')  # Default to gray if not in mapping
        fig.add_trace(go.Bar(
            x=module_columns,
            y=student[module_columns],
            name=student_name,
            marker=dict(color=color)
        ))

    # Update layout with dark background and custom legend
    fig.update_layout(
        title=f"Best Scores for {program} Students",
        title_font=dict(color='white', size=16),
        xaxis_title="Modules",
        yaxis_title="Marks",
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        legend=dict(
            title=dict(
                text="Students",
                font=dict(size=10, color='white')
            ),
            font=dict(size=8, color='white'),
            bgcolor='rgba(0, 0, 0, 0.5)',
            bordercolor='white',
            borderwidth=1
        )
    )

    # Display the plot with dark theme
    st.plotly_chart(fig)

# Main app control
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard" and st.session_state.authenticated:
    dashboard_page()
