"""
bookings.py - Ticket Booking, Cancellation and History
Cinema Ticket Booking System

This module handles:
1. Booking tickets with real-time seat validation and transaction consistency
2. Generating a text ticket receipt (demonstrating Python file handling)
3. Viewing personal booking history for logged-in customer
4. Cancelling an existing booking and restoring seats
5. Viewing all customer bookings for Administrator
"""

import sqlite3
import os
from database import get_connection
from shows import view_all_shows, get_show_by_id

# Directory to save receipt files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECEIPTS_DIR = os.path.join(BASE_DIR, "receipts")


def save_ticket_receipt(booking_id, username, movie_name, show_date, show_time, tickets, total_amount):
    """
    Demonstrates Python File Handling:
    Creates a formatted text file receipt for the customer's records.
    """
    try:
        if not os.path.exists(RECEIPTS_DIR):
            os.makedirs(RECEIPTS_DIR)

        filename = os.path.join(RECEIPTS_DIR, f"receipt_booking_{booking_id}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 45 + "\n")
            f.write("         CINEMA TICKET BOOKING RECEIPT\n")
            f.write("=" * 45 + "\n")
            f.write(f" Booking ID       : #{booking_id}\n")
            f.write(f" Customer Name    : {username}\n")
            f.write(f" Movie Title      : {movie_name}\n")
            f.write(f" Show Date        : {show_date}\n")
            f.write(f" Show Time        : {show_time}\n")
            f.write(f" Tickets Booked   : {tickets}\n")
            f.write(f" Total Paid       : ${total_amount:.2f}\n")
            f.write(f" Booking Status   : Confirmed\n")
            f.write("-" * 45 + "\n")
            f.write(" Thank you for booking with us! Enjoy your movie!\n")
            f.write("=" * 45 + "\n")

        return filename
    except IOError as e:
        print(f"[Warning] Could not generate receipt file: {e}")
        return None


def book_tickets(current_user):
    """
    Allows a customer to book tickets for an available show.
    Checks show existence, seat availability, calculates total,
    and updates database inside an atomic transaction.
    """
    print("\n" + "=" * 50)
    print("               BOOK MOVIE TICKETS")
    print("=" * 50)

    # Display available shows
    shows = view_all_shows()
    if not shows:
        return False

    # 1. Select Show ID
    while True:
        id_input = input("\nEnter Show ID you want to book (or 'movie' to filter by movie, 'cancel' to return): ").strip()
        if id_input.lower() == 'cancel':
            return False
        if id_input.lower() in ('movie', 'm'):
            from shows import view_shows_by_movie
            view_shows_by_movie()
            continue
        if not id_input:
            print("[Validation Error] Show ID cannot be empty.")
            continue
        try:
            show_id = int(id_input)
            show = get_show_by_id(show_id)
            if show is None:
                print(f"[Validation Error] No show found with ID #{show_id}.")
                continue

            available_seats = show[6]
            if available_seats <= 0:
                print(f"[Notice] Sorry, Show #{show_id} is completely sold out! Please choose another show.")
                continue

            break
        except ValueError:
            print("[Validation Error] Please enter a valid numerical Show ID.")

    _, movie_id, movie_name, show_date, show_time, ticket_price, available_seats = show

    print(f"\nMovie: {movie_name}")
    print(f"Date & Time: {show_date} at {show_time}")
    print(f"Ticket Price: ${ticket_price:.2f}")
    print(f"Seats Available: {available_seats}")
    print("-" * 50)

    # 2. Number of tickets
    while True:
        qty_input = input(f"How many tickets would you like to book? (Max {available_seats}, or 'cancel' to abort): ").strip()
        if qty_input.lower() == 'cancel':
            print("[Info] Booking aborted.")
            return False
        if not qty_input:
            print("[Validation Error] Quantity cannot be empty.")
            continue
        try:
            tickets_requested = int(qty_input)
            if tickets_requested <= 0:
                print("[Validation Error] Ticket quantity must be at least 1 (greater than zero).")
                continue
            if tickets_requested > available_seats:
                print(f"[Validation Error] Only {available_seats} seat(s) available. You cannot book {tickets_requested}.")
                continue
            break
        except ValueError:
            print("[Validation Error] Please enter a valid whole number for ticket count.")

    # Calculate total
    total_amount = round(tickets_requested * ticket_price, 2)

    # Confirm booking
    print("\n" + "-" * 40)
    print("          BOOKING SUMMARY")
    print("-" * 40)
    print(f" Movie        : {movie_name}")
    print(f" Show         : {show_date} ({show_time})")
    print(f" Tickets      : {tickets_requested}")
    print(f" Total Amount : ${total_amount:.2f}")
    print("-" * 40)

    confirm = input("Confirm and proceed with booking? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("[Info] Booking cancelled by customer.")
        return False

    # Execute database transaction
    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return False

    cursor = conn.cursor()

    try:
        # Re-check seats inside transaction to avoid race conditions
        cursor.execute("SELECT available_seats FROM shows WHERE show_id = ?", (show_id,))
        current_seats_row = cursor.fetchone()

        if current_seats_row is None or current_seats_row[0] < tickets_requested:
            print("\n[Error] Seats are no longer available. Booking could not be completed.")
            conn.rollback()
            return False

        # 1. Insert booking record
        cursor.execute(
            """
            INSERT INTO bookings (user_id, show_id, number_of_tickets, total_amount, booking_status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (current_user["user_id"], show_id, tickets_requested, total_amount, "Confirmed")
        )
        booking_id = cursor.lastrowid

        # 2. Update available seats
        cursor.execute(
            """
            UPDATE shows
            SET available_seats = available_seats - ?
            WHERE show_id = ?
            """,
            (tickets_requested, show_id)
        )

        # Commit transaction atomically
        conn.commit()

        print("\n" + "=" * 50)
        print("          BOOKING CONFIRMED!")
        print("=" * 50)
        print(f" Booking Reference ID: #{booking_id}")
        print(f" Movie              : {movie_name}")
        print(f" Show Time          : {show_date} at {show_time}")
        print(f" Tickets Reserved   : {tickets_requested}")
        print(f" Total Paid         : ${total_amount:.2f}")
        print(f" Status             : Confirmed")

        # Save receipt text file
        receipt_path = save_ticket_receipt(
            booking_id, current_user["username"], movie_name,
            show_date, show_time, tickets_requested, total_amount
        )
        if receipt_path:
            print(f" Receipt generated  : {os.path.basename(receipt_path)}")
        print("=" * 50)
        return True

    except sqlite3.Error as e:
        print(f"\n[Database Error] Booking failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def view_customer_bookings(current_user):
    """
    Displays the booking history for the logged-in customer.
    """
    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return []

    cursor = conn.cursor()

    try:
        query = """
            SELECT b.booking_id, m.movie_name, s.show_date, s.show_time,
                   b.number_of_tickets, b.total_amount, b.booking_status
            FROM bookings b
            JOIN shows s ON b.show_id = s.show_id
            JOIN movies m ON s.movie_id = m.movie_id
            WHERE b.user_id = ?
            ORDER BY b.booking_id DESC
        """
        cursor.execute(query, (current_user["user_id"],))
        bookings = cursor.fetchall()

        print("\n" + "=" * 80)
        print(f"               MY BOOKING HISTORY ({current_user['username']})")
        print("=" * 80)

        if not bookings:
            print(" You have not made any bookings yet.")
            print("=" * 80)
            return []

        header = f"{'Book ID':<8} | {'Movie Title':<22} | {'Date':<11} | {'Time':<9} | {'Tickets':<7} | {'Total':<8} | {'Status':<10}"
        print(header)
        print("-" * 80)

        for b in bookings:
            b_id, title, b_date, b_time, tickets, amount, status = b
            display_title = (title[:19] + "..") if len(title) > 21 else title
            amount_str = f"${amount:.2f}"
            print(f"{b_id:<8} | {display_title:<22} | {b_date:<11} | {b_time:<9} | {tickets:<7} | {amount_str:<8} | {status:<10}")

        print("=" * 80)
        return bookings

    except sqlite3.Error as e:
        print(f"\n[Database Error] Could not retrieve bookings: {e}")
        return []
    finally:
        conn.close()


def cancel_booking(current_user):
    """
    Allows a customer to cancel their own confirmed booking.
    Restores the seats to the show and sets status to 'Cancelled'.
    Prevents double-cancellation and prevents cancelling other customers' bookings.
    """
    print("\n" + "=" * 50)
    print("               CANCEL BOOKING")
    print("=" * 50)

    bookings = view_customer_bookings(current_user)
    if not bookings:
        return False

    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return False

    cursor = conn.cursor()

    try:
        while True:
            id_input = input("\nEnter Booking ID to cancel (or 'cancel' to return): ").strip()
            if id_input.lower() == 'cancel':
                return False
            if not id_input:
                print("[Validation Error] Booking ID cannot be empty.")
                continue
            try:
                booking_id = int(id_input)
            except ValueError:
                print("[Validation Error] Please enter a valid numerical Booking ID.")
                continue

            # Check if booking exists in database
            cursor.execute(
                "SELECT booking_id, user_id, booking_status FROM bookings WHERE booking_id = ?",
                (booking_id,)
            )
            any_booking = cursor.fetchone()

            if any_booking is None:
                print(f"[Validation Error] No booking found with ID #{booking_id}. Please check your Booking History above.")
                continue

            # Verify ownership: check that customer owns this booking
            if any_booking[1] != current_user["user_id"]:
                print(f"[Security Warning] Access denied: Booking #{booking_id} belongs to another customer! You can only cancel your own bookings.")
                continue

            # Prevent double-cancellation
            if any_booking[2] == 'Cancelled':
                print(f"[Notice] Booking #{booking_id} has already been cancelled previously. You cannot cancel it again.")
                continue

            # Retrieve details for confirmation
            cursor.execute(
                """
                SELECT b.booking_id, b.show_id, b.number_of_tickets, m.movie_name
                FROM bookings b
                JOIN shows s ON b.show_id = s.show_id
                JOIN movies m ON s.movie_id = m.movie_id
                WHERE b.booking_id = ?
                """,
                (booking_id,)
            )
            b_id, show_id, tickets, movie_name = cursor.fetchone()
            break

        # Confirm cancellation
        confirm = input(f"Are you sure you want to cancel booking #{booking_id} for '{movie_name}' ({tickets} tickets)? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("[Info] Cancellation aborted.")
            return False

        # Begin atomic update: cancel booking & restore seats
        cursor.execute(
            "UPDATE bookings SET booking_status = 'Cancelled' WHERE booking_id = ?",
            (booking_id,)
        )

        cursor.execute(
            "UPDATE shows SET available_seats = available_seats + ? WHERE show_id = ?",
            (tickets, show_id)
        )

        conn.commit()

        print("\n" + "-" * 50)
        print(f" SUCCESS: Booking #{booking_id} has been cancelled.")
        print(f" {tickets} seat(s) have been restored to the show inventory.")
        print("-" * 50)
        return True

    except sqlite3.Error as e:
        print(f"\n[Database Error] Cancellation failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def view_all_bookings():
    """
    Allows Administrator to view all bookings placed across all customers.
    """
    conn = get_connection()
    if conn is None:
        print("[Error] Database connection unavailable.")
        return []

    cursor = conn.cursor()

    try:
        query = """
            SELECT b.booking_id, u.username, m.movie_name, s.show_date, s.show_time,
                   b.number_of_tickets, b.total_amount, b.booking_status
            FROM bookings b
            JOIN users u ON b.user_id = u.user_id
            JOIN shows s ON b.show_id = s.show_id
            JOIN movies m ON s.movie_id = m.movie_id
            ORDER BY b.booking_id DESC
        """
        cursor.execute(query)
        bookings = cursor.fetchall()

        print("\n" + "=" * 90)
        print("                            ALL CUSTOMER BOOKINGS")
        print("=" * 90)

        if not bookings:
            print(" No customer bookings recorded yet.")
            print("=" * 90)
            return []

        header = f"{'Book ID':<8} | {'Customer':<12} | {'Movie Title':<20} | {'Date':<11} | {'Time':<9} | {'Seats':<5} | {'Total':<8} | {'Status':<10}"
        print(header)
        print("-" * 90)

        for b in bookings:
            b_id, username, title, b_date, b_time, tickets, amount, status = b
            display_title = (title[:18] + "..") if len(title) > 20 else title
            amount_str = f"${amount:.2f}"
            print(f"{b_id:<8} | {username:<12} | {display_title:<20} | {b_date:<11} | {b_time:<9} | {tickets:<5} | {amount_str:<8} | {status:<10}")

        print("=" * 90)
        return bookings

    except sqlite3.Error as e:
        print(f"\n[Database Error] Could not retrieve all bookings: {e}")
        return []
    finally:
        conn.close()
