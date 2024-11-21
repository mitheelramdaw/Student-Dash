import sqlite3

# Function to create the tables if they don't exist
def create_tables():
    conn = sqlite3.connect('students.db')  # Connect to your SQLite database
    cursor = conn.cursor()

    # Create table for Diploma in IT students if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diploma_students (
        STUDENT_NUMBER TEXT PRIMARY KEY,
        STUDENT_NAME TEXT,
        SEM500 INT,
        MIS500 INT,
        QT600 INT,
        HCI500 INT,
        ITPM600 INT,
        ELECTIVE INT
    )
    ''')

    # Create table for BSc in IT students if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bsc_students (
        STUDENT_NUMBER TEXT PRIMARY KEY,
        STUDENT_NAME TEXT,
        PROG732 INT,
        CYBER700 INT,
        SEM700 INT,
        HCI700 INT,
        AI700 INT,
        ELECTIVE INT
    )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Tables created successfully!")

# Function to add missing columns if they don't exist
def add_missing_columns():
    conn = sqlite3.connect('students.db')  # Connect to your SQLite database
    cursor = conn.cursor()

    # Check and add ELECTIVE column to diploma_students table if not exists
    cursor.execute('''
    PRAGMA table_info(diploma_students)
    ''')
    columns = [column[1] for column in cursor.fetchall()]
    if 'ELECTIVE' not in columns:
        cursor.execute('''
        ALTER TABLE diploma_students ADD COLUMN ELECTIVE INT
        ''')

    # Check and add ELECTIVE column to bsc_students table if not exists
    cursor.execute('''
    PRAGMA table_info(bsc_students)
    ''')
    columns = [column[1] for column in cursor.fetchall()]
    if 'ELECTIVE' not in columns:
        cursor.execute('''
        ALTER TABLE bsc_students ADD COLUMN ELECTIVE INT
        ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Missing columns added successfully!")

# Function to insert student data into a table
def insert_data():
    conn = sqlite3.connect('students.db')  # Connect to your SQLite database
    cursor = conn.cursor()

    # Sample data for Diploma in IT students
    diploma_students = [
        (403281267, 'Ryan Chitate', 94, 88, 81, 90, 79, 97),
        (403235277, 'Hayden Pillay', 85, 79, 91, 97, 77, 84),
        (403281237, 'Malik Hassan', 78, 81, 97, 86, 89, 82)
    ]
    
    # Insert data into diploma_students table
    cursor.executemany('''
        INSERT INTO diploma_students (STUDENT_NUMBER, STUDENT_NAME, SEM500, MIS500, QT600, HCI500, ITPM600, ELECTIVE)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', diploma_students)

    # Sample data for BSc in IT students
    bsc_students = [
        (402231236, 'Mitheel Ramdaw', 93, 95, 92, 98, 97, 90),
        (402251566, 'Tawana Kombora', 92, 91, 88, 80, 77, 95),
        (402431226, 'Mikabo Ramdaw', 84, 90, 81, 97, 78, 80)
    ]
    
    # Insert data into bsc_students table
    cursor.executemany('''
        INSERT INTO bsc_students (STUDENT_NUMBER, STUDENT_NAME, PROG732, CYBER700, SEM700, HCI700, AI700, ELECTIVE)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', bsc_students)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Data inserted successfully!")

# Create the tables and ensure the ELECTIVE column is present
create_tables()

# Add the missing columns (if any)
add_missing_columns()

# Call the function to insert data
insert_data()
