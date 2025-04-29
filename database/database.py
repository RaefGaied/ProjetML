import sqlite3
import os
from pathlib import Path
import hashlib
from config.config import DATABASE_PATH
from datetime import datetime

def init_database():
    """Initialize the database and create necessary tables if they don't exist."""
    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create user_history table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image_path TEXT,
        prediction_result TEXT,
        prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, email, full_name):
    """Create a new user in the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO users (username, password, email, full_name)
        VALUES (?, ?, ?, ?)
        ''', (username, hash_password(password), email, full_name))
        
        conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError as e:
        return False, "Username or email already exists"
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, username, password FROM users WHERE username = ?
    ''', (username,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user and user[2] == hash_password(password):
        return True, user[0]  # Return success and user_id
    return False, None

def get_user_info(user_id):
    """Get user information by ID."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT username, email, full_name, created_at FROM users WHERE id = ?
    ''', (user_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "username": user[0],
            "email": user[1],
            "full_name": user[2],
            "created_at": user[3]
        }
    return None

def save_prediction(user_id, image_path, prediction_result):
    """Save prediction result to user history."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO user_history (user_id, image_path, prediction_result)
    VALUES (?, ?, ?)
    ''', (user_id, image_path, prediction_result))
    
    conn.commit()
    conn.close()

def get_user_history(user_id):
    """Get user's prediction history."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT image_path, prediction_result, prediction_date 
    FROM user_history 
    WHERE user_id = ? 
    ORDER BY prediction_date DESC
    ''', (user_id,))
    
    history = cursor.fetchall()
    conn.close()
    
    return [{
        "image_path": item[0],
        "prediction_result": item[1],
        "prediction_date": item[2]
    } for item in history]

def add_user(username, password, email=None, full_name=None):
    """Add a new user to the database"""
    try:
        # Ensure email is provided since it's required in the database
        if email is None or email.strip() == "":
            print("Error: Email is required but was not provided")
            return False
            
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Hash the password
        hashed_password = hash_password(password)
        
        # Debug print
        print(f"Adding user: {username}, email: {email}, full_name: {full_name}")
        
        cursor.execute('''INSERT INTO users (username, password, email, full_name)
                    VALUES (?, ?, ?, ?)''',
                 (username, hashed_password, email, full_name))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error adding user: {str(e)}")
        return False

def get_user_by_username(username):
    """Get user information by username"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'password': user[2],
                'email': user[3],
                'full_name': user[4],
                'created_at': user[5]
            }
        return None
    except Exception as e:
        print(f"Error getting user: {str(e)}")
        return None

def add_prediction(user_id, image_path, prediction_result):
    """Add a new prediction to the database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO user_history (user_id, image_path, prediction_result)
                    VALUES (?, ?, ?)''',
                 (user_id, image_path, prediction_result))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding prediction: {str(e)}")
        return False 