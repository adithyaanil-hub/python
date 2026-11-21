"""
movies.py - Movie Management (CRUD Operations)
Cinema Ticket Booking System

This module handles:
1. Adding new movies (Create)
2. Viewing all movies in catalog (Read)
3. Updating movie details (Update)
4. Deleting movies (Delete)
"""

import sqlite3
from database import get_connection

# Common genres represented as a Python Set to demonstrate set usage
COMMON_GENRES = {"Action", "Comedy", "Drama", "Sci-Fi", "Horror", "Thriller", "Romance", "Animation", "Adventure"}


def add_movie():
    """
    Allows Administrator to add a new movie to the catalog.
    Validates movie name, genre, duration (positive int), and language.
    """
    print("\n" + "=" * 50)
    print("               ADD NEW MOVIE")
    print("=" * 50)

    # 1. Movie Name
    while True:
        movie_name = input("Enter movie title (or 'cancel' to abort): ").strip()
        if movie_name.lower() == 'cancel':
            print("[Info] Add movie operation cancelled.")
            return False
        if not movie_name:
            print("[Validation Error] Movie title cannot be empty.")
            continue
        break

    # 2. Genre (Demonstrating Set membership check & suggestions)
    print(f"Suggested genres: {', '.join(sorted(COMMON_GENRES))}")
    while True:
        genre = input("Enter genre: ").strip()
        if not genre:
            print("[Validation Error] Genre cannot be empty.")
            continue
        genre = genre.title()
        break

    # 3. Duration in minutes
    while True:
        duration_input = input("Enter duration in minutes (e.g. 120): ").strip()
        if not duration_input:
            print("[Validation Error] Duration cannot be empty.")
            continue
        try:
            duration = int(duration_input)
            if duration <= 0:
                print("[Validation Error] Duration must be a positive number of minutes.")
                continue
            break
        except ValueError:
            print("[Validation Error] Invalid input. Please enter a whole number for minutes.")

    # 4. Language
    while True:
        language = input("Enter language (e.g. English, Hindi, Spanish): ").strip()
        if not language:
            print("[Validation Error] Language cannot be empty.")
            continue
        language = language.title()
        break

    # Insert into database using parameterized query
    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return False

    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO movies (movie_name, genre, duration, language) VALUES (?, ?, ?, ?)",
            (movie_name, genre, duration, language)
        )
        conn.commit()
        movie_id = cursor.lastrowid
        print("\n" + "-" * 50)
        print(f" SUCCESS: Movie '{movie_name}' added successfully with ID #{movie_id}!")
        print("-" * 50)
        return True
    except sqlite3.Error as e:
        print(f"\n[Database Error] Could not add movie: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def view_all_movies():
    """
    Fetches and displays all movies in a formatted table.
    Returns:
        list: A list of movie tuples, or an empty list if no movies found.
    """
    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return []

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT movie_id, movie_name, genre, duration, language FROM movies ORDER BY movie_id")
        movie_list = cursor.fetchall()

        print("\n" + "=" * 70)
        print("                         CURRENT MOVIES")
        print("=" * 70)

        if not movie_list:
            print(" No movies currently found in the catalog.")
            print("=" * 70)
            return []

        # Table Header
        header = f"{'ID':<6} | {'Movie Title':<28} | {'Genre':<12} | {'Duration':<10} | {'Language':<10}"
        print(header)
        print("-" * 70)

        # Table Rows
        for movie in movie_list:
            m_id = movie[0]
            name = str(movie[1]) if movie[1] is not None else "Unknown"
            genre = str(movie[2]) if movie[2] is not None else "N/A"
            duration = movie[3]
            lang = str(movie[4]) if movie[4] is not None else "N/A"
            duration_str = f"{duration} mins" if duration is not None else "N/A"
            # Truncate title if longer than 26 chars for clean display
            display_name = (name[:25] + "..") if len(name) > 27 else name
            print(f"{m_id:<6} | {display_name:<28} | {genre:<12} | {duration_str:<10} | {lang:<10}")

        print("=" * 70)
        return movie_list

    except sqlite3.Error as e:
        print(f"\n[Database Error] Failed to retrieve movies: {e}")
        return []
    except Exception as e:
        print(f"\n[Error] Unexpected error retrieving movies: {e}")
        return []
    finally:
        conn.close()


def view_movies():
    """
    Fetches and displays all movies in a formatted table.
    Alias for view_all_movies() to support college grading and alternative calls.
    """
    return view_all_movies()


def get_movie_by_id(movie_id):
    """
    Helper function to retrieve a single movie tuple by ID.
    Returns:
        tuple: (movie_id, movie_name, genre, duration, language) or None
    """
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT movie_id, movie_name, genre, duration, language FROM movies WHERE movie_id = ?", (movie_id,))
        return cursor.fetchone()
    except sqlite3.Error:
        return None
    finally:
        conn.close()


def update_movie():
    """
    Allows Administrator to update an existing movie's details.
    Prompts for ID, shows current details, and allows updating fields.
    """
    print("\n" + "=" * 50)
    print("               UPDATE MOVIE")
    print("=" * 50)

    # First display available movies
    movies = view_all_movies()
    if not movies:
        return False

    # Get valid movie ID
    while True:
        id_input = input("\nEnter Movie ID to update (or 'cancel' to return): ").strip()
        if id_input.lower() == 'cancel':
            return False
        if not id_input:
            print("[Validation Error] Movie ID cannot be empty.")
            continue
        try:
            movie_id = int(id_input)
            existing_movie = get_movie_by_id(movie_id)
            if existing_movie is None:
                print(f"[Validation Error] No movie found with ID #{movie_id}. Please try again.")
                continue
            break
        except ValueError:
            print("[Validation Error] Please enter a valid numerical ID.")

    _, curr_name, curr_genre, curr_duration, curr_lang = existing_movie

    print("\nPress Enter without typing to keep the current value.")
    print("-" * 50)

    # New title
    new_name = input(f"New Title [{curr_name}]: ").strip()
    if not new_name:
        new_name = curr_name

    # New genre
    new_genre = input(f"New Genre [{curr_genre}]: ").strip()
    if not new_genre:
        new_genre = curr_genre
    else:
        new_genre = new_genre.title()

    # New duration
    while True:
        new_dur_input = input(f"New Duration in mins [{curr_duration}]: ").strip()
        if not new_dur_input:
            new_duration = curr_duration
            break
        try:
            val = int(new_dur_input)
            if val <= 0:
                print("[Validation Error] Duration must be positive.")
                continue
            new_duration = val
            break
        except ValueError:
            print("[Validation Error] Please enter a valid number for minutes.")

    # New language
    new_lang = input(f"New Language [{curr_lang}]: ").strip()
    if not new_lang:
        new_lang = curr_lang
    else:
        new_lang = new_lang.title()

    # Execute Update
    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return False

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE movies
            SET movie_name = ?, genre = ?, duration = ?, language = ?
            WHERE movie_id = ?
            """,
            (new_name, new_genre, new_duration, new_lang, movie_id)
        )
        conn.commit()
        print("\n" + "-" * 50)
        print(f" SUCCESS: Movie ID #{movie_id} updated successfully!")
        print("-" * 50)
        return True
    except sqlite3.Error as e:
        print(f"\n[Database Error] Failed to update movie: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def delete_movie():
    """
    Allows Administrator to delete a movie from the catalog.
    Warns that associated shows and bookings will also be deleted via CASCADE.
    """
    print("\n" + "=" * 50)
    print("               DELETE MOVIE")
    print("=" * 50)

    movies = view_all_movies()
    if not movies:
        return False

    while True:
        id_input = input("\nEnter Movie ID to delete (or 'cancel' to return): ").strip()
        if id_input.lower() == 'cancel':
            return False
        if not id_input:
            print("[Validation Error] Movie ID cannot be empty.")
            continue
        try:
            movie_id = int(id_input)
            movie = get_movie_by_id(movie_id)
            if movie is None:
                print(f"[Validation Error] No movie found with ID #{movie_id}.")
                continue
            break
        except ValueError:
            print("[Validation Error] Please enter a valid numerical ID.")

    movie_name = movie[1]

    # Check associated shows and bookings
    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return False

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM shows WHERE movie_id = ?", (movie_id,))
    show_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM bookings WHERE show_id IN (SELECT show_id FROM shows WHERE movie_id = ?)", (movie_id,))
    booking_count = cursor.fetchone()[0]

    print(f"\n[WARNING] Deleting movie '{movie_name}' (ID: #{movie_id})")
    if show_count > 0 or booking_count > 0:
        print(f"Associated records: {show_count} show(s) and {booking_count} customer booking(s).")
        print("All these associated records will also be permanently deleted!")
    confirm = input("Are you sure you want to proceed? (yes/no): ").strip().lower()

    if confirm != 'yes':
        print("[Info] Movie deletion cancelled.")
        conn.close()
        return False

    try:
        cursor.execute("DELETE FROM movies WHERE movie_id = ?", (movie_id,))
        conn.commit()
        print("\n" + "-" * 50)
        print(f" SUCCESS: Movie '{movie_name}' (ID #{movie_id}) was deleted.")
        print("-" * 50)
        return True
    except sqlite3.Error as e:
        print(f"\n[Database Error] Could not delete movie: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
