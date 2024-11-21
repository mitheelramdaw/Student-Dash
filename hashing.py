import sqlite3
import bcrypt

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create the users table (run once)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
''')

# Add user 'kaka' with password 'tata', hash the password
password = bcrypt.hashpw("tata".encode('utf-8'), bcrypt.gensalt())  # Hash the password 'tata'
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("kaka", password))

# Commit and close
conn.commit()
conn.close()
