"""
shows.py - Movie Show Management (CRUD Operations)
Cinema Ticket Booking System

This module handles:
1. Adding new shows for movies (Create)
2. Viewing available shows with movie details (Read)
3. Viewing shows filtered by movie
4. Updating show details (time, date, ticket price, seats) (Update)
5. Deleting shows (Delete)
"""

import sqlite3
import re
from datetime import datetime
from database import get_connection
from movies import view_all_movies, get_movie_by_id


def validate_date(date_str):
    """
    Validates that a date matches YYYY-MM-DD format with real calendar validation.
    Returns: bool
    """
    if not date_str:
        return False
    try:
        # Check format and real calendar validity (handles leap years, days in month)
        parsed = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        # Ensure date is in a realistic range
        if not (2025 <= parsed.year <= 2035):
            return False
        return True
    except ValueError:
        return False


def validate_time(time_str):
    """
    Validates show time format (e.g. '06:30 PM', '10:00 AM', or '18:30').
    Returns: bool
    """
    if not time_str:
        return False
    time_str = time_str.strip().upper()
    for fmt in ("%I:%M %p", "%I:%M%p", "%H:%M"):
        try:
            datetime.strptime(time_str, fmt)
            return True
        except ValueError:
            pass
    return False


def parse_time_for_sorting(time_str):
    """
    Helper function to convert 12-hour or 24-hour time string into a comparable time object.
    """
    time_str = time_str.strip().upper()
    for fmt in ("%I:%M %p", "%I:%M%p", "%H:%M"):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            pass
    return datetime.min.time()


def add_show():
    """
    Allows Administrator to schedule a new show for an existing movie.
    """
    print("\n" + "=" * 50)
    print("               ADD NEW SHOW")
    print("=" * 50)

    # First check and show available movies
    movies = view_all_movies()
    if not movies:
        print("\n[Notice] Please add at least one movie first before scheduling shows.")
        return False

    # 1. Movie ID
    while True:
        movie_input = input("\nEnter Movie ID for the show (or 'cancel' to abort): ").strip()
        if movie_input.lower() == 'cancel':
            return False
        if not movie_input:
            print("[Validation Error] Movie ID cannot be empty.")
            continue
        try:
            movie_id = int(movie_input)
            movie = get_movie_by_id(movie_id)
            if movie is None:
                print(f"[Validation Error] Movie ID #{movie_id} does not exist.")
                continue
            print(f"-> Selected: {movie[1]} ({movie[4]})")
            break
        except ValueError:
            print("[Validation Error] Please enter a valid numerical ID.")

    # 2. Show Date
    while True:
        show_date = input("Enter Show Date (YYYY-MM-DD, e.g. 2026-12-05): ").strip()
        if not show_date:
            print("[Validation Error] Date cannot be empty.")
            continue
        if not validate_date(show_date):
            print("[Validation Error] Invalid format or date. Please use YYYY-MM-DD.")
            continue
        break

    # 3. Show Time
    while True:
        show_time = input("Enter Show Time (e.g. 06:30 PM or 18:30): ").strip()
        if not show_time:
            print("[Validation Error] Time cannot be empty.")
            continue
        if not validate_time(show_time):
            print("[Validation Error] Invalid time format. Examples: '07:30 PM', '10:00 AM', '19:00'")
            continue
        show_time = show_time.upper()
        break

    # 4. Ticket Price
    while True:
        price_input = input("Enter Ticket Price (e.g. 12.50): $").strip()
        if not price_input:
            print("[Validation Error] Ticket price cannot be empty.")
            continue
        try:
            ticket_price = float(price_input)
            if ticket_price <= 0:
                print("[Validation Error] Ticket price must be greater than 0.")
                continue
            ticket_price = round(ticket_price, 2)
            break
        except ValueError:
            print("[Validation Error] Please enter a valid number for ticket price.")

    # 5. Available Seats
    while True:
        seats_input = input("Enter Total Available Seats (e.g. 50): ").strip()
        if not seats_input:
            print("[Validation Error] Seats cannot be empty.")
            continue
        try:
            available_seats = int(seats_input)
            if available_seats <= 0:
                print("[Validation Error] Seats must be a positive number.")
                continue
            break
        except ValueError:
            print("[Validation Error] Please enter a valid whole number for seats.")

    # Insert into database
    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return False

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO shows (movie_id, show_date, show_time, ticket_price, available_seats)
            VALUES (?, ?, ?, ?, ?)
            """,
            (movie_id, show_date, show_time, ticket_price, available_seats)
        )
        conn.commit()
        show_id = cursor.lastrowid
        print("\n" + "-" * 50)
        print(f" SUCCESS: Show #{show_id} scheduled for '{movie[1]}' on {show_date} at {show_time}!")
        print("-" * 50)
        return True
    except sqlite3.Error as e:
        print(f"\n[Database Error] Failed to schedule show: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def view_all_shows():
    """
    Fetches and displays all scheduled shows joined with movie titles.
    Returns:
        list: List of show tuples.
    """
    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return []

    cursor = conn.cursor()

    try:
        query = """
            SELECT s.show_id, m.movie_name, m.language, s.show_date, s.show_time,
                   s.ticket_price, s.available_seats
            FROM shows s
            JOIN movies m ON s.movie_id = m.movie_id
        """
        cursor.execute(query)
        shows = cursor.fetchall()

        # Sort chronologically by date and real time
        shows.sort(key=lambda s: (s[3], parse_time_for_sorting(s[4])))

        print("\n" + "=" * 80)
        print("                            AVAILABLE SHOWS")
        print("=" * 80)

        if not shows:
            print(" No shows currently scheduled.")
            print("=" * 80)
            return []

        header = f"{'Show ID':<8} | {'Movie Title':<24} | {'Date':<12} | {'Time':<10} | {'Price':<8} | {'Seats':<6}"
        print(header)
        print("-" * 80)

        for show in shows:
            s_id, title, lang, s_date, s_time, price, seats = show
            display_title = (title[:21] + "..") if len(title) > 23 else title
            price_str = f"${price:.2f}"
            seats_str = f"{seats} left"
            print(f"{s_id:<8} | {display_title:<24} | {s_date:<12} | {s_time:<10} | {price_str:<8} | {seats_str:<6}")

        print("=" * 80)
        return shows

    except sqlite3.Error as e:
        print(f"\n[Database Error] Could not load shows: {e}")
        return []
    except Exception as e:
        print(f"\n[Error] Unexpected error loading shows: {e}")
        return []
    finally:
        conn.close()


def view_shows():
    """
    Fetches and displays all shows in a formatted table.
    Alias for view_all_shows() to support college grading and alternative calls.
    """
    return view_all_shows()


def view_shows_by_movie():
    """
    Displays shows for a specific movie chosen by the user.
    """
    movies = view_all_movies()
    if not movies:
        return

    while True:
        id_input = input("\nEnter Movie ID to see its shows (or 'cancel' to return): ").strip()
        if id_input.lower() == 'cancel':
            return []
        if not id_input:
            print("[Validation Error] Movie ID cannot be empty.")
            continue
        try:
            movie_id = int(id_input)
            movie = get_movie_by_id(movie_id)
            if movie is None:
                print(f"[Validation Error] Movie ID #{movie_id} does not exist.")
                continue
            break
        except ValueError:
            print("[Validation Error] Please enter a valid numerical ID.")

    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor()

    try:
        query = """
            SELECT s.show_id, m.movie_name, s.show_date, s.show_time,
                   s.ticket_price, s.available_seats
            FROM shows s
            JOIN movies m ON s.movie_id = m.movie_id
            WHERE s.movie_id = ?
        """
        cursor.execute(query, (movie_id,))
        shows = cursor.fetchall()

        # Sort chronologically by date and real time
        shows.sort(key=lambda s: (s[2], parse_time_for_sorting(s[3])))

        print("\n" + "=" * 75)
        print(f"                SHOWS FOR: {movie[1]} ({movie[4]})")
        print("=" * 75)

        if not shows:
            print(f" No upcoming shows scheduled for '{movie[1]}'.")
            print("=" * 75)
            return []

        header = f"{'Show ID':<8} | {'Date':<12} | {'Time':<10} | {'Price':<10} | {'Available Seats':<15}"
        print(header)
        print("-" * 75)

        for show in shows:
            s_id, _, s_date, s_time, price, seats = show
            print(f"{s_id:<8} | {s_date:<12} | {s_time:<10} | ${price:<9.2f} | {seats:<15}")

        print("=" * 75)
        return shows

    except sqlite3.Error as e:
        print(f"\n[Database Error] Error fetching shows: {e}")
        return []
    finally:
        conn.close()


def get_show_by_id(show_id):
    """
    Retrieves full details for a single show by its ID.
    Returns: tuple or None
    """
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        query = """
            SELECT s.show_id, s.movie_id, m.movie_name, s.show_date, s.show_time,
                   s.ticket_price, s.available_seats
            FROM shows s
            JOIN movies m ON s.movie_id = m.movie_id
            WHERE s.show_id = ?
        """
        cursor.execute(query, (show_id,))
        return cursor.fetchone()
    except sqlite3.Error:
        return None
    finally:
        conn.close()


def update_show():
    """
    Allows Administrator to update show date, time, price, or seats.
    """
    print("\n" + "=" * 50)
    print("               UPDATE SHOW DETAILS")
    print("=" * 50)

    shows = view_all_shows()
    if not shows:
        return False

    while True:
        id_input = input("\nEnter Show ID to update (or 'cancel' to return): ").strip()
        if id_input.lower() == 'cancel':
            return False
        try:
            show_id = int(id_input)
            show = get_show_by_id(show_id)
            if show is None:
                print(f"[Validation Error] No show found with ID #{show_id}.")
                continue
            break
        except ValueError:
            print("[Validation Error] Please enter a valid numerical ID.")

    _, movie_id, movie_name, curr_date, curr_time, curr_price, curr_seats = show

    print(f"\nUpdating Show #{show_id} for '{movie_name}'")
    print("Press Enter without typing to keep the current value.")
    print("-" * 50)

    # Date
    while True:
        new_date = input(f"New Date (YYYY-MM-DD) [{curr_date}]: ").strip()
        if not new_date:
            new_date = curr_date
            break
        if not validate_date(new_date):
            print("[Validation Error] Invalid date format. Use YYYY-MM-DD.")
            continue
        break

    # Time
    while True:
        new_time = input(f"New Time [{curr_time}]: ").strip()
        if not new_time:
            new_time = curr_time
            break
        if not validate_time(new_time):
            print("[Validation Error] Invalid time format.")
            continue
        new_time = new_time.upper()
        break

    # Price
    while True:
        new_price_input = input(f"New Price [${curr_price:.2f}]: ").strip()
        if not new_price_input:
            new_price = curr_price
            break
        try:
            val = float(new_price_input)
            if val <= 0:
                print("[Validation Error] Price must be positive.")
                continue
            new_price = round(val, 2)
            break
        except ValueError:
            print("[Validation Error] Please enter a valid number for price.")

    # Seats
    while True:
        new_seats_input = input(f"New Available Seats [{curr_seats}]: ").strip()
        if not new_seats_input:
            new_seats = curr_seats
            break
        try:
            val = int(new_seats_input)
            if val < 0:
                print("[Validation Error] Seats cannot be negative.")
                continue
            new_seats = val
            break
        except ValueError:
            print("[Validation Error] Please enter a whole number for seats.")

    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return False

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE shows
            SET show_date = ?, show_time = ?, ticket_price = ?, available_seats = ?
            WHERE show_id = ?
            """,
            (new_date, new_time, new_price, new_seats, show_id)
        )
        conn.commit()
        print("\n" + "-" * 50)
        print(f" SUCCESS: Show #{show_id} updated successfully!")
        print("-" * 50)
        return True
    except sqlite3.Error as e:
        print(f"\n[Database Error] Failed to update show: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def delete_show():
    """
    Allows Administrator to delete a show.
    """
    print("\n" + "=" * 50)
    print("               DELETE SHOW")
    print("=" * 50)

    shows = view_all_shows()
    if not shows:
        return False

    while True:
        id_input = input("\nEnter Show ID to delete (or 'cancel' to return): ").strip()
        if id_input.lower() == 'cancel':
            return False
        if not id_input:
            print("[Validation Error] Show ID cannot be empty.")
            continue
        try:
            show_id = int(id_input)
            show = get_show_by_id(show_id)
            if show is None:
                print(f"[Validation Error] No show found with ID #{show_id}.")
                continue
            break
        except ValueError:
            print("[Validation Error] Please enter a valid numerical ID.")

    _, _, movie_name, s_date, s_time, _, _ = show

    # Check for linked customer bookings
    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return False

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM bookings WHERE show_id = ?", (show_id,))
    booking_count = cursor.fetchone()[0]

    print(f"\n[WARNING] Deleting Show #{show_id} ('{movie_name}' on {s_date} at {s_time})")
    if booking_count > 0:
        print(f"There are {booking_count} customer booking(s) associated with this show.")
        print("Deleting this show will also remove these bookings!")
    confirm = input("Confirm deletion? (yes/no): ").strip().lower()

    if confirm != 'yes':
        print("[Info] Show deletion cancelled.")
        conn.close()
        return False

    try:
        cursor.execute("DELETE FROM shows WHERE show_id = ?", (show_id,))
        conn.commit()
        print("\n" + "-" * 50)
        print(f" SUCCESS: Show #{show_id} was deleted.")
        print("-" * 50)
        return True
    except sqlite3.Error as e:
        print(f"\n[Database Error] Could not delete show: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
