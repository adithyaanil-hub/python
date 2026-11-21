# Cinema Ticket Booking System
**Python 3 + SQLite Database Management System**

A complete, beginner/intermediate friendly, command-line interface (CLI) Cinema Ticket Booking System built with Python and SQLite3. Demonstrates database design, SQL operations, foreign key integrity, user authentication, role-based authorization, transaction management, and input validation.

---

## 1. Project Overview

The **Cinema Ticket Booking System** allows customers to browse available movies and shows, reserve seats, view their personal booking history, and cancel tickets with automatic seat restoration. It provides administrators with a dedicated management portal to perform complete CRUD (Create, Read, Update, Delete) operations on movies and shows, as well as view all customer bookings across the entire cinema.

---

## 2. Features

### User Roles & Permissions
- **Administrator Role**:
  - Secure Admin Login.
  - **Movie Management**: Add movies, view catalog, update movie details, delete movies.
  - **Show Scheduling**: Schedule shows with date, time, ticket price, and seat capacity; view all shows; update show details; delete shows.
  - **Booking Oversight**: View all customer bookings system-wide.
  - Logout.
- **Customer Role**:
  - Account Registration with unique username verification.
  - Customer Login and Session tracking.
  - View all movies and genres.
  - View available shows (all or filtered by movie).
  - Book tickets with real-time seat validation and total calculation.
  - View personal booking history.
  - Cancel confirmed bookings with automatic seat inventory restoration.
  - Logout.

### Database & Relational Integrity
- **SQLite3 Database (`cinema.db`)** created automatically on startup.
- **Foreign Key Support** enabled via `PRAGMA foreign_keys = ON;`.
- **Atomic Transactions**: Seat deductions and restorations are executed inside database transactions (`commit()` / `rollback()`) to prevent race conditions or partial updates.
- **Cascading Deletions**: Related shows and bookings are consistently managed when parents are updated or removed.
- **Ticket Receipt Generator**: Generates formatted `.txt` receipts in the `receipts/` directory demonstrating Python file handling.

---

## 3. Database Schema

The database consists of four interconnected relational tables:

```
  +------------------+           +------------------+
  |      users       |           |      movies      |
  +------------------+           +------------------+
  | user_id (PK)     |           | movie_id (PK)    |
  | username (UNIQUE)|           | movie_name       |
  | password         |           | genre            |
  | role             |           | duration         |
  +--------+---------+           | language         |
           |                     +--------+---------+
           |                              |
           |                              | 1
           |                              |
           |                              v M
           |                     +------------------+
           |                     |      shows       |
           |                     +------------------+
           |                     | show_id (PK)     |
           |                     | movie_id (FK)    |
           |                     | show_date        |
           |                     | show_time        |
           |                     | ticket_price     |
           |                     | available_seats  |
           |                     +--------+---------+
           |                              |
           | 1                            | 1
           |                              |
           v M                            v M
  +-------------------------------------------------+
  |                    bookings                     |
  +-------------------------------------------------+
  | booking_id (PK)                                 |
  | user_id (FK -> users.user_id)                   |
  | show_id (FK -> shows.show_id)                   |
  | number_of_tickets                               |
  | total_amount                                    |
  | booking_status ('Confirmed' / 'Cancelled')      |
  +-------------------------------------------------+
```

### Table Definitions

1. **`users`**
   - `user_id`: `INTEGER PRIMARY KEY AUTOINCREMENT`
   - `username`: `TEXT UNIQUE NOT NULL`
   - `password`: `TEXT NOT NULL`
   - `role`: `TEXT NOT NULL CHECK(role IN ('admin', 'customer'))`

2. **`movies`**
   - `movie_id`: `INTEGER PRIMARY KEY AUTOINCREMENT`
   - `movie_name`: `TEXT NOT NULL`
   - `genre`: `TEXT NOT NULL`
   - `duration`: `INTEGER NOT NULL` (in minutes)
   - `language`: `TEXT NOT NULL`

3. **`shows`**
   - `show_id`: `INTEGER PRIMARY KEY AUTOINCREMENT`
   - `movie_id`: `INTEGER NOT NULL, FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE`
   - `show_date`: `TEXT NOT NULL` (Format: `YYYY-MM-DD`)
   - `show_time`: `TEXT NOT NULL` (Format: `HH:MM AM/PM`)
   - `ticket_price`: `REAL NOT NULL`
   - `available_seats`: `INTEGER NOT NULL`

4. **`bookings`**
   - `booking_id`: `INTEGER PRIMARY KEY AUTOINCREMENT`
   - `user_id`: `INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE`
   - `show_id`: `INTEGER NOT NULL, FOREIGN KEY (show_id) REFERENCES shows (show_id) ON DELETE CASCADE`
   - `number_of_tickets`: `INTEGER NOT NULL`
   - `total_amount`: `REAL NOT NULL`
   - `booking_status`: `TEXT NOT NULL CHECK(booking_status IN ('Confirmed', 'Cancelled'))`

---

## 4. Project Folder Structure

```
04_Cinema_Ticket_Booking_System/
├── main.py            # Main application loop and menu navigation
├── database.py        # Database connection, table creation, and data seeding
├── authentication.py  # User registration, login verification, and logout
├── movies.py          # Movie CRUD operations (Add, View, Update, Delete)
├── shows.py           # Show management and scheduling (Add, View, Update, Delete)
├── bookings.py        # Ticket booking, seat updates, cancellation, and receipt generation
├── receipts/          # Auto-generated ticket receipts (.txt)
├── cinema.db          # SQLite3 database file (created automatically)
└── README.md          # Project documentation and guide
```

---

## 5. Python Concepts Demonstrated

| Concept | Where & How Used |
|---|---|
| **Variables & Types** | `int`, `float`, `str`, `bool` used across pricing, seat numbers, IDs, and statuses. |
| **Functions** | Clean, modular procedural functions with descriptive parameters and return values. |
| **Conditionals** | `if / elif / else` for input validation, menu choices, and permission checks. |
| **Loops** | `while True` for interactive menus and retry prompts; `for` loops for record iteration. |
| **Lists** | Lists of query rows returned from `cursor.fetchall()`, lists of records. |
| **Tuples** | Parameterized query tuples `(movie_id,)`, database row tuples. |
| **Dictionaries** | Active user session state `{"user_id": ..., "username": ..., "role": ...}`. |
| **Sets** | Set of common genres (`COMMON_GENRES`) for validation and membership testing. |
| **SQLite3 Module** | `connect()`, `execute()`, `executemany()`, `fetchone()`, `fetchall()`, `commit()`, `rollback()`. |
| **SQL Queries** | `CREATE TABLE`, `INSERT`, `SELECT` (with multi-table `JOIN`), `UPDATE`, `DELETE`. |
| **CRUD Operations** | Complete Create, Read, Update, Delete cycles for movies and shows. |
| **Transactions** | Explicit `conn.commit()` and `conn.rollback()` ensuring seat and booking consistency. |
| **Authentication** | Username uniqueness check, credential verification, and session management. |
| **Authorization** | Separate menus and operations for Administrator vs Customer. |
| **Exception Handling** | `try-except` blocks handling `sqlite3.Error`, `ValueError`, `IOError`. |
| **File Handling** | Ticket receipts generated and saved as text files (`open(..., "w")`). |

---

## 6. How to Run the Project

### Prerequisites
- Python 3.8 or higher installed on your computer.
- No external libraries or pip packages required (uses Python built-in standard libraries).

### Step-by-Step Instructions

1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd 04_Cinema_Ticket_Booking_System
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---

## 7. Default Credentials

The database is initialized automatically with sample movies, showtimes, and a default administrator account:

| Role | Username | Password |
|---|---|---|
| **Administrator** | `admin` | `admin123` |
| **Customer** | *(Register any username via Option 1)* | *(Chosen during registration)* |

---

## 8. Menu Navigation Guide

### Main Menu
```
1. Register (New Customer)
2. Login
3. Exit
```

### Administrator Dashboard
```
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
```

### Customer Dashboard
```
1. View Movies
2. View Shows (All or by specific movie)
3. Book Tickets
4. View My Bookings
5. Cancel Booking
6. Logout
```

---

## 9. Testing & Sample Walkthrough

1. **Start Application**: Run `python main.py`. Database `cinema.db` will be created with initial sample data.
2. **Log in as Admin**:
   - Choose `2. Login`.
   - Username: `admin`, Password: `admin123`.
   - View movies (`2`), view shows (`6`), add a new movie (`1`), schedule a show (`5`), or view all customer bookings (`9`).
   - Logout (`10`).
3. **Register as Customer**:
   - Choose `1. Register`.
   - Enter a new username (e.g. `john_doe`) and password (e.g. `pass123`).
4. **Log in as Customer**:
   - Choose `2. Login` with `john_doe`.
   - Browse movies (`1`) and shows (`2`).
   - Book tickets (`3`): Select a show ID, choose quantity (e.g., 2 tickets), and confirm.
   - Check booking receipt printed in the console and saved in `receipts/`.
   - View booking history (`4`).
   - Cancel booking (`5`): Enter the booking ID to cancel and observe seats restored in show inventory.
5. **Exit**:
   - Logout (`6`), then choose `3. Exit` from the main menu.
