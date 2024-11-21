import streamlit as st
import sqlite3
import pandas as pd

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

# Streamlit page configuration
st.set_page_config(page_title="Student Dashboard", layout="wide")

# Sidebar for navigation
program = st.sidebar.radio("Select Program", ["Diploma in IT", "BSc in IT"])

# Fetch student data based on program selected
df = fetch_student_data(program)

# Display title and table on the corresponding page
st.title(f"Student Data for {program}")
st.write(f"Showing student details for the {program} program.")

# Display student data table with dynamic column headers, use full container width
st.dataframe(df, use_container_width=True)  # Automatically expand the table to the full width
