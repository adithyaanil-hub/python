import sqlite3

conn = sqlite3.connect("task.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tname VARCHAR(20),
        tdes TEXT
    )
""")


def addtask():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()

    name = input("Enter task name: ")
    des = input("Enter task description: ")

    cursor.execute("""
        INSERT INTO tasks(tname, tdes)
        VALUES(?, ?)
    """, (name, des))

    conn.commit()
    print("Task added 😊")
    conn.close()


def viewtasks():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tasks
    """)

    data = cursor.fetchall()

    if data:
        print("tasks found")
        for i in data:
            print(f"{i[0]}---{i[1]}---{i[2]}")
    else:
        print("No tasks found")


def searchtask():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    t_id = int(input("enter task id:--"))
    cursor.execute('''
       SELECT * FROM tasks WHERE id= ?
       ''', (t_id,))
    data = cursor.fetchone()
    if data:
        print("data found")
        print(data[1])


def edittasks():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    t_id = int(input("enter task id:"))
    name = input("enter new task name:-")
    des = input("enter new task des:-")
    cursor.execute('''
    UPDATE tasks SET tname=?,tdes=?WHERE id=?
    ''', (name, des, t_id))
    conn.commit()
    print("Task updated")


def deletetask():
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()
    t_id = int(input("enter task id---"))
    cursor.execute('''
    DELETE FROM tasks WHERE id=?
    ''', (t_id,))
    ch = input("Are you sure you want to delete this task... y/n ?--")
    if ch == "y":
        conn.commit()
        print("task deleted")
    else:
        print("cancelled")


def main():
    print("Welcome to Task Management System")

    while True:
        ch = int(input(
            "Enter your choice\n"
            "1. Add task\n"
            "2. View task\n"
            "3. Search task\n"
            "4. Update task\n"
            "5. Delete task\n"
            "6. Exit\n"
        ))

        if ch == 1:
            addtask()
            pass
        elif ch == 2:
            viewtasks()
        elif ch == 3:
            searchtask()
        elif ch == 4:
            edittasks()
        elif ch == 5:
            deletetask()
        elif ch == 6:
            break


main()

conn.close()
