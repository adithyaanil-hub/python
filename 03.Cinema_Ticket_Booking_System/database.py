"""
database.py - Database Connection and Table Management
Cinema Ticket Booking System

This module handles:
1. Connecting to the SQLite database (cinema.db)
2. Enabling foreign key constraints
3. Creating required tables (users, movies, shows, bookings)
4. Seeding initial data (default admin account and sample movies/shows)
"""

import sqlite3
import os

# Define database file path in the same directory as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "cinema.db")


def get_connection():
    """
    Establishes and returns a connection to the SQLite database.
    Foreign key enforcement is enabled for referential integrity.
    """
    try:
        conn = sqlite3.connect(DB_NAME, timeout=20.0)
        # SQLite does not enforce foreign keys by default, so we enable it
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA busy_timeout = 20000;")
        return conn
    except sqlite3.Error as e:
        print(f"\n[Database Error] Failed to connect to database: {e}")
        return None


def create_tables():
    """
    Creates the required four relational tables if they do not exist:
    - users: stores login credentials and roles (admin / customer)
    - movies: stores movie catalog
    - shows: stores showtime schedules and seat capacity (linked to movies)
    - bookings: stores ticket bookings (linked to users and shows)
    """
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        # Table 1: users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'customer'))
            );
        """)

        # Table 2: movies
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT NOT NULL,
                genre TEXT NOT NULL,
                duration INTEGER NOT NULL,
                language TEXT NOT NULL
            );
        """)

        # Table 3: shows
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shows (
                show_id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                show_date TEXT NOT NULL,
                show_time TEXT NOT NULL,
                ticket_price REAL NOT NULL,
                available_seats INTEGER NOT NULL,
                FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE
            );
        """)

        # Table 4: bookings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                show_id INTEGER NOT NULL,
                number_of_tickets INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                booking_status TEXT NOT NULL CHECK(booking_status IN ('Confirmed', 'Cancelled')),
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (show_id) REFERENCES shows (show_id) ON DELETE CASCADE
            );
        """)

        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"\n[Database Error] Error creating tables: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def seed_initial_data():
    """
    Seeds initial administrator credentials and sample movies/shows
    if they do not already exist.
    """
    conn = get_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        # 1. Seed default administrator account if none exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        admin_count = cursor.fetchone()[0]

        if admin_count == 0:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("admin", "admin123", "admin")
            )
            print("[Setup] Default administrator account created: (Username: admin | Password: admin123)")

        # 2. Seed sample movies if movies table is empty
        cursor.execute("SELECT COUNT(*) FROM movies")
        movie_count = cursor.fetchone()[0]

        if movie_count == 0:
            sample_movies = [
                ("Inception", "Sci-Fi", 148, "English"),
                ("Interstellar", "Sci-Fi", 169, "English"),
                ("The Dark Knight", "Action", 152, "English"),
                ("Spirited Away", "Animation", 125, "Japanese")
            ]
            cursor.executemany(
                "INSERT INTO movies (movie_name, genre, duration, language) VALUES (?, ?, ?, ?)",
                sample_movies
            )

            # 3. Seed sample shows for the newly created movies
            # Retrieve generated movie IDs
            cursor.execute("SELECT movie_id FROM movies ORDER BY movie_id")
            movie_rows = cursor.fetchall()

            sample_shows = [
                (movie_rows[0][0], "2026-12-01", "10:30 AM", 12.50, 50),
                (movie_rows[0][0], "2026-12-01", "06:30 PM", 15.00, 50),
                (movie_rows[1][0], "2026-12-01", "02:00 PM", 14.00, 45),
                (movie_rows[2][0], "2026-12-02", "07:00 PM", 15.00, 60),
                (movie_rows[3][0], "2026-12-02", "04:00 PM", 11.00, 40)
            ]
            cursor.executemany(
                "INSERT INTO shows (movie_id, show_date, show_time, ticket_price, available_seats) VALUES (?, ?, ?, ?, ?)",
                sample_shows
            )
            print("[Setup] Sample movies and show schedules added.")

        conn.commit()
    except sqlite3.Error as e:
        print(f"\n[Database Error] Error seeding data: {e}")
        conn.rollback()
    finally:
        conn.close()


def initialize_database():
    """
    Main initialization function to be called on system startup.
    Ensures tables are created and seeded.
    """
    if create_tables():
        seed_initial_data()
