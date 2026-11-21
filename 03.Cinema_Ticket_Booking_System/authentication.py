"""
authentication.py - User Authentication and Authorization
Cinema Ticket Booking System

This module handles:
1. Customer registration with duplicate username validation
2. User login (Admin and Customer)
3. User logout and session management
"""

import sqlite3
from database import get_connection


def register_customer():
    """
    Registers a new customer account.
    Validates that:
    - Username is not empty
    - Username is not already taken
    - Password is not empty (minimum 4 characters)
    - Passwords match on confirmation
    """
    print("\n" + "=" * 45)
    print("         CUSTOMER REGISTRATION")
    print("=" * 45)

    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return False

    cursor = conn.cursor()

    try:
        while True:
            username = input("Enter a username (or type 'cancel' to exit): ").strip()

            if username.lower() == 'cancel':
                print("[Info] Registration cancelled.")
                return False

            if not username:
                print("[Validation Error] Username cannot be empty. Please try again.")
                continue

            if len(username) < 3:
                print("[Validation Error] Username must be at least 3 characters long.")
                continue

            # Check if username already exists in database
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()

            if existing_user is not None:
                print(f"[Validation Error] The username '{username}' is already taken. Please choose another.")
                continue

            # Username is unique and valid
            break

        while True:
            password = input("Enter a password (at least 4 characters, or 'cancel' to exit): ").strip()
            if password.lower() == 'cancel':
                print("[Info] Registration cancelled.")
                return False
            if len(password) < 4:
                print("[Validation Error] Password must be at least 4 characters long.")
                continue

            confirm_password = input("Confirm your password: ").strip()
            if confirm_password.lower() == 'cancel':
                print("[Info] Registration cancelled.")
                return False
            if password != confirm_password:
                print("[Validation Error] Passwords do not match. Please try again.")
                continue

            break

        # Insert new customer record with role 'customer'
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, "customer")
        )
        conn.commit()

        print("\n" + "-" * 45)
        print(f" SUCCESS: Account for '{username}' created successfully!")
        print(" You can now log in using your credentials.")
        print("-" * 45)
        return True

    except sqlite3.IntegrityError:
        print("\n[Database Error] Username already exists.")
        conn.rollback()
        return False
    except sqlite3.Error as e:
        print(f"\n[Database Error] An error occurred during registration: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def login_user():
    """
    Authenticates an administrator or customer.
    Returns:
        dict: A dictionary containing user session information:
              {"user_id": int, "username": str, "role": str}
        None: If login fails or user cancels
    """
    print("\n" + "=" * 45)
    print("               USER LOGIN")
    print("=" * 45)

    username = input("Username (or 'cancel' to return): ").strip()
    if username.lower() == 'cancel':
        return None

    if not username:
        print("[Validation Error] Username cannot be empty.")
        return None

    password = input("Password (or 'cancel' to return): ").strip()
    if password.lower() == 'cancel':
        return None
    if not password:
        print("[Validation Error] Password cannot be empty.")
        return None

    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return None

    cursor = conn.cursor()

    try:
        # Parameterized query to prevent SQL injection
        cursor.execute(
            "SELECT user_id, username, password, role FROM users WHERE username = ?",
            (username,)
        )
        user_record = cursor.fetchone()

        if user_record is None:
            print("\n[Login Failed] Invalid username or password.")
            return None

        # Check password
        user_id, db_username, db_password, role = user_record
        if db_password != password:
            print("\n[Login Failed] Invalid username or password.")
            return None

        # Successful login - create and return session dictionary
        user_session = {
            "user_id": user_id,
            "username": db_username,
            "role": role
        }

        print("\n" + "-" * 45)
        print(f" Welcome back, {db_username}! (Role: {role.capitalize()})")
        print("-" * 45)
        return user_session

    except sqlite3.Error as e:
        print(f"\n[Database Error] Login query error: {e}")
        return None
    finally:
        conn.close()


def logout_user(current_user):
    """
    Logs out the current active user.
    """
    if current_user:
        print(f"\n[Session] Goodbye, {current_user['username']}! You have been logged out.")
    return None
