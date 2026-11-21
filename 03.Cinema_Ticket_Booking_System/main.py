"""
main.py - Main Application and Menu Navigation
Cinema Ticket Booking System

A command-line based Cinema Ticket Booking System developed in Python and SQLite3.
Supports Administrator and Customer roles with role-based access control.
"""

import sys
import database
import authentication
import movies
import shows
import bookings


def display_welcome_banner():
    """Displays the system application banner."""
    print("=" * 60)
    print("        WELCOME TO CINEMA TICKET BOOKING SYSTEM")
    print("       Python 3 + SQLite Database Management System")
    print("=" * 60)


def admin_menu(current_user):
    """
    Administrator Dashboard Menu.
    Options:
    1. Add Movie
    2. View Movies
    3. Update Movie
    4. Delete Movie
    5. Add Show
    6. View Shows
    7. Update Show
    8. Delete Show
    9. View All Bookings
    10. Logout
    """
    while True:
        print("\n" + "=" * 45)
        print(f"      ADMINISTRATOR DASHBOARD ({current_user['username']})")
        print("=" * 45)
        print(" 1. Add Movie")
        print(" 2. View Movies")
        print(" 3. Update Movie")
        print(" 4. Delete Movie")
        print(" 5. Add Show")
        print(" 6. View Shows")
        print(" 7. Update Show")
        print(" 8. Delete Show")
        print(" 9. View All Bookings")
        print(" 10. Logout")
        print("=" * 45)

        choice = input("Enter your choice (1-10): ").strip()

        if choice == '1':
            movies.add_movie()
        elif choice == '2':
            movies.view_all_movies()
            input("\nPress Enter to return to Administrator Dashboard...")
        elif choice == '3':
            movies.update_movie()
        elif choice == '4':
            movies.delete_movie()
        elif choice == '5':
            shows.add_show()
        elif choice == '6':
            shows.view_all_shows()
            input("\nPress Enter to return to Administrator Dashboard...")
        elif choice == '7':
            shows.update_show()
        elif choice == '8':
            shows.delete_show()
        elif choice == '9':
            bookings.view_all_bookings()
            input("\nPress Enter to return to Administrator Dashboard...")
        elif choice == '10':
            authentication.logout_user(current_user)
            break
        else:
            print("\n[Input Error] Invalid selection! Please enter a number from 1 to 10.")


def customer_menu(current_user):
    """
    Customer Dashboard Menu.
    Options:
    1. View Movies
    2. View Shows
    3. Book Tickets
    4. View My Bookings
    5. Cancel Booking
    6. Logout
    """
    while True:
        print("\n" + "=" * 45)
        print(f"         CUSTOMER DASHBOARD ({current_user['username']})")
        print("=" * 45)
        print(" 1. View Movies")
        print(" 2. View Shows")
        print(" 3. Book Tickets")
        print(" 4. View My Bookings")
        print(" 5. Cancel Booking")
        print(" 6. Logout")
        print("=" * 45)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            movies.view_all_movies()
            prompt_res = input("\nPress Enter to return to Dashboard (or enter Movie ID to view its showtimes): ").strip()
            if prompt_res:
                try:
                    m_id = int(prompt_res)
                    conn = database.get_connection()
                    if conn:
                        cur = conn.cursor()
                        cur.execute("SELECT movie_name, language FROM movies WHERE movie_id = ?", (m_id,))
                        m_row = cur.fetchone()
                        if m_row:
                            cur.execute(
                                """
                                SELECT s.show_id, m.movie_name, s.show_date, s.show_time,
                                       s.ticket_price, s.available_seats
                                FROM shows s
                                JOIN movies m ON s.movie_id = m.movie_id
                                WHERE s.movie_id = ?
                                """,
                                (m_id,)
                            )
                            s_list = cur.fetchall()
                            s_list.sort(key=lambda s: (s[2], shows.parse_time_for_sorting(s[3])))
                            print("\n" + "=" * 75)
                            print(f"                SHOWS FOR: {m_row[0]} ({m_row[1]})")
                            print("=" * 75)
                            if not s_list:
                                print(f" No upcoming shows scheduled for '{m_row[0]}'.")
                            else:
                                header = f"{'Show ID':<8} | {'Date':<12} | {'Time':<10} | {'Price':<10} | {'Available Seats':<15}"
                                print(header)
                                print("-" * 75)
                                for s_row in s_list:
                                    print(f"{s_row[0]:<8} | {s_row[2]:<12} | {s_row[3]:<10} | ${s_row[4]:<9.2f} | {s_row[5]:<15}")
                            print("=" * 75)
                            input("\nPress Enter to return to Dashboard...")
                        else:
                            print(f"[Validation Error] Movie ID #{m_id} does not exist.")
                            input("\nPress Enter to return to Dashboard...")
                        conn.close()
                except ValueError:
                    pass
        elif choice == '2':
            while True:
                print("\n" + "-" * 38)
                print("              VIEW SHOWS")
                print("-" * 38)
                print(" 1. View All Scheduled Shows")
                print(" 2. View Shows for a Specific Movie")
                print(" 3. Back to Dashboard")
                print("-" * 38)
                sub_choice = input("Select option (1-3): ").strip()
                if sub_choice == '1':
                    shows.view_all_shows()
                    input("\nPress Enter to return to Dashboard...")
                    break
                elif sub_choice == '2':
                    shows.view_shows_by_movie()
                    input("\nPress Enter to return to Dashboard...")
                    break
                elif sub_choice == '3' or sub_choice.lower() == 'cancel':
                    break
                elif not sub_choice:
                    print("[Input Error] Option cannot be empty. Please enter 1, 2, or 3.")
                else:
                    print("[Input Error] Invalid option! Please enter 1, 2, or 3.")
        elif choice == '3':
            bookings.book_tickets(current_user)
        elif choice == '4':
            bookings.view_customer_bookings(current_user)
            input("\nPress Enter to return to Dashboard...")
        elif choice == '5':
            bookings.cancel_booking(current_user)
        elif choice == '6':
            authentication.logout_user(current_user)
            break
        else:
            print("\n[Input Error] Invalid selection! Please enter a number from 1 to 6.")


def main():
    """
    Main application loop.
    Options:
    1. Register (New customer)
    2. Login (Admin or Customer)
    3. Exit
    """
    # Initialize SQLite database and tables
    database.initialize_database()

    display_welcome_banner()

    while True:
        print("\n" + "=" * 40)
        print("              MAIN MENU")
        print("=" * 40)
        print(" 1. Register (New Customer)")
        print(" 2. Login")
        print(" 3. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            authentication.register_customer()
        elif choice == '2':
            user_session = authentication.login_user()
            if user_session is not None:
                # Role-based redirection
                if user_session["role"] == "admin":
                    admin_menu(user_session)
                elif user_session["role"] == "customer":
                    customer_menu(user_session)
                else:
                    print("[Security Error] Unknown role detected. Access denied.")
        elif choice == '3':
            print("\nThank you for using Cinema Ticket Booking System. Goodbye!")
            sys.exit(0)
        else:
            print("\n[Input Error] Invalid selection! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
