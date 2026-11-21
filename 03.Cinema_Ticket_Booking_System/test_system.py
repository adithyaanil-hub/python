"""
test_system.py - Comprehensive Unit & Integration Tests for Cinema Ticket Booking System
"""

import os
import sys
import sqlite3
from unittest.mock import patch

# Add current dir to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database
import authentication
import movies
import shows
import bookings

# Configure an isolated test database and test receipts directory
# This guarantees that tests NEVER touch or modify the real cinema.db database
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DB = os.path.join(TEST_DIR, "test_cinema.db")
TEST_RECEIPTS = os.path.join(TEST_DIR, "test_receipts")

database.DB_NAME = TEST_DB
bookings.RECEIPTS_DIR = TEST_RECEIPTS


def test_database_initialization():
    print("\n--- Test 1: Database Initialization ---")
    database.initialize_database()
    assert os.path.exists(database.DB_NAME), "Database file does not exist!"
    
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    assert {"users", "movies", "shows", "bookings"}.issubset(tables), f"Missing tables! Found: {tables}"
    
    # Check default admin
    cursor.execute("SELECT username, role FROM users WHERE username='admin';")
    admin = cursor.fetchone()
    assert admin is not None and admin[1] == "admin", "Default admin account missing!"
    
    # Check sample movies and shows
    cursor.execute("SELECT COUNT(*) FROM movies;")
    movie_count = cursor.fetchone()[0]
    assert movie_count > 0, "No sample movies found!"
    
    cursor.execute("SELECT COUNT(*) FROM shows;")
    show_count = cursor.fetchone()[0]
    assert show_count > 0, "No sample shows found!"
    
    conn.close()
    print("PASS: Database initialized with tables, admin, movies, and shows.")


def test_authentication():
    print("\n--- Test 2: Authentication (Registration & Login) ---")
    
    # Clean up any leftover testuser from prior aborted test run
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = 'testuser'")
    conn.commit()
    conn.close()

    # 1. Register new customer
    with patch("builtins.input", side_effect=["testuser", "pass1234", "pass1234"]):
        success = authentication.register_customer()
        assert success is True, "Customer registration failed!"
        
    # 2. Duplicate registration should fail/prevent duplicate
    with patch("builtins.input", side_effect=["testuser", "cancel"]):
        success = authentication.register_customer()
        assert success is False, "Duplicate customer allowed when it shouldn't be!"
        
    # 3. Customer login
    with patch("builtins.input", side_effect=["testuser", "pass1234"]):
        session = authentication.login_user()
        assert session is not None, "Customer login failed!"
        assert session["username"] == "testuser"
        assert session["role"] == "customer"
        
    # 4. Admin login
    with patch("builtins.input", side_effect=["admin", "admin123"]):
        admin_session = authentication.login_user()
        assert admin_session is not None, "Admin login failed!"
        assert admin_session["role"] == "admin"
        
    # 5. Invalid password login
    with patch("builtins.input", side_effect=["admin", "wrongpass"]):
        fail_session = authentication.login_user()
        assert fail_session is None, "Login with wrong password succeeded unexpectedly!"
        
    print("PASS: Registration, duplicate check, and role-based login tests succeeded.")


def test_movie_crud():
    print("\n--- Test 3: Movie CRUD Operations ---")
    
    # 1. Add Movie
    with patch("builtins.input", side_effect=["Avatar 3", "Sci-Fi", "180", "English"]):
        success = movies.add_movie()
        assert success is True, "Adding movie failed!"
        
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT movie_id FROM movies WHERE movie_name='Avatar 3';")
    row = cursor.fetchone()
    assert row is not None, "Movie not inserted in database!"
    movie_id = row[0]
    conn.close()
    
    # 2. View Movies
    all_movies = movies.view_all_movies()
    assert any(m[1] == "Avatar 3" for m in all_movies), "Avatar 3 not in view_all_movies!"
    
    # 3. Update Movie
    with patch("builtins.input", side_effect=[str(movie_id), "Avatar: Fire and Ash", "", "190", ""]):
        success = movies.update_movie()
        assert success is True, "Updating movie failed!"
        
    m = movies.get_movie_by_id(movie_id)
    assert m[1] == "Avatar: Fire and Ash", f"Movie title not updated! Got: {m[1]}"
    assert m[3] == 190, f"Movie duration not updated! Got: {m[3]}"
    
    # 4. Delete Movie
    with patch("builtins.input", side_effect=[str(movie_id), "yes"]):
        success = movies.delete_movie()
        assert success is True, "Deleting movie failed!"
        
    assert movies.get_movie_by_id(movie_id) is None, "Movie still exists after deletion!"
    print("PASS: Movie CRUD operations passed completely.")


def test_show_crud_and_booking_transactions():
    print("\n--- Test 4: Show Management & Booking Transactions ---")
    
    # Get an existing movie
    all_movies = movies.view_all_movies()
    movie_id = all_movies[0][0]
    
    # 1. Add Show with 10 available seats
    with patch("builtins.input", side_effect=[str(movie_id), "2026-12-10", "08:00 PM", "15.50", "10"]):
        success = shows.add_show()
        assert success is True, "Adding show failed!"
        
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT show_id, available_seats FROM shows WHERE show_date='2026-12-10' AND show_time='08:00 PM';")
    show_row = cursor.fetchone()
    assert show_row is not None, "Show not inserted!"
    show_id, seats = show_row
    assert seats == 10, f"Expected 10 seats, found {seats}"
    conn.close()
    
    # Get user session for testuser
    user_conn = database.get_connection()
    u_cur = user_conn.cursor()
    u_cur.execute("SELECT user_id, username, role FROM users WHERE username='testuser';")
    u_row = u_cur.fetchone()
    user_session = {"user_id": u_row[0], "username": u_row[1], "role": u_row[2]}
    user_conn.close()
    
    # 2. Try overbooking (request 15 seats when only 10 available, then retry with 3)
    with patch("builtins.input", side_effect=[str(show_id), "15", "3", "yes"]):
        success = bookings.book_tickets(user_session)
        assert success is True, "Booking 3 tickets failed!"
        
    # Check seat deduction: 10 - 3 = 7 seats left
    show_data = shows.get_show_by_id(show_id)
    assert show_data[6] == 7, f"Expected 7 seats left, got {show_data[6]}"
    
    # Verify booking record in DB
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT booking_id, number_of_tickets, total_amount, booking_status FROM bookings WHERE show_id=? AND user_id=?;", (show_id, user_session["user_id"]))
    b_row = cursor.fetchone()
    assert b_row is not None, "Booking record not found!"
    booking_id, num_tickets, total_amt, b_status = b_row
    assert num_tickets == 3
    assert total_amt == 46.50  # 3 * 15.50
    assert b_status == "Confirmed"
    conn.close()
    
    # Check receipt file was generated
    receipt_file = os.path.join(bookings.RECEIPTS_DIR, f"receipt_booking_{booking_id}.txt")
    assert os.path.exists(receipt_file), f"Receipt file {receipt_file} was not created!"
    with open(receipt_file, "r") as rf:
        content = rf.read()
        assert f"#{booking_id}" in content
        assert "testuser" in content
        
    print("PASS: Ticket booking deducted seats and generated receipt text file.")
    
    # 3. View bookings
    my_bookings = bookings.view_customer_bookings(user_session)
    assert any(b[0] == booking_id for b in my_bookings), "Booking not listed in customer history!"
    
    all_b = bookings.view_all_bookings()
    assert any(b[0] == booking_id for b in all_b), "Booking not listed in admin view!"
    
    # 4. Cancel booking and check seat restoration: 7 + 3 = 10 seats
    with patch("builtins.input", side_effect=[str(booking_id), "yes"]):
        cancel_success = bookings.cancel_booking(user_session)
        assert cancel_success is True, "Cancellation failed!"
        
    # Check show seats restored
    show_data_after_cancel = shows.get_show_by_id(show_id)
    assert show_data_after_cancel[6] == 10, f"Expected 10 seats after cancellation, got {show_data_after_cancel[6]}"
    
    # 5. Prevent double cancellation (test typing booking_id, then cancel)
    with patch("builtins.input", side_effect=[str(booking_id), "cancel"]):
        double_cancel = bookings.cancel_booking(user_session)
        assert double_cancel is False, "Double cancellation allowed unexpectedly!"
        
    print("PASS: Booking cancellation restored seats and prevented double cancellation.")

    # 5b. Prevent customer from cancelling another customer's booking
    conn = database.get_connection()
    c = conn.cursor()
    # Find another existing user (e.g., admin or another customer)
    c.execute("SELECT user_id FROM users WHERE user_id != ?", (user_session["user_id"],))
    other_user_row = c.fetchone()
    other_user_id = other_user_row[0]
    
    # Create a booking for that other user
    c.execute("INSERT INTO bookings (user_id, show_id, number_of_tickets, total_amount, booking_status) VALUES (?, ?, 1, 15.50, 'Confirmed')", (other_user_id, show_id))
    foreign_booking_id = c.lastrowid
    conn.commit()
    conn.close()

    # User testuser tries to cancel foreign_booking_id
    with patch("builtins.input", side_effect=[str(foreign_booking_id), "cancel"]):
        cross_cancel = bookings.cancel_booking(user_session)
        assert cross_cancel is False, "Customer was able to cancel another customer's booking!"

    # Clean up dummy booking
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE booking_id = ?", (foreign_booking_id,))
    conn.commit()
    conn.close()
    print("PASS: Cross-customer cancellation prevention verified.")
    
    # 6. Delete show
    with patch("builtins.input", side_effect=[str(show_id), "yes"]):
        del_show_success = shows.delete_show()
        assert del_show_success is True, "Show deletion failed!"
        
    assert shows.get_show_by_id(show_id) is None, "Show still exists after deletion!"
    print("PASS: Show deletion passed.")

    # Clean up test user
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = 'testuser'")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import shutil
    # Clean up prior test artifacts if present
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    if os.path.exists(TEST_RECEIPTS):
        shutil.rmtree(TEST_RECEIPTS)

    print("========================================")
    print("STARTING CINEMA SYSTEM AUTOMATED TESTS")
    print("(Running in isolated test_cinema.db)")
    print("========================================")
    test_database_initialization()
    test_authentication()
    test_movie_crud()
    test_show_crud_and_booking_transactions()

    # Clean up test database and test receipts
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    if os.path.exists(TEST_RECEIPTS):
        shutil.rmtree(TEST_RECEIPTS)

    print("\n========================================")
    print("ALL TESTS PASSED SUCCESSFULLY! (100%)")
    print("(Real cinema.db was 100% untouched)")
    print("========================================")
