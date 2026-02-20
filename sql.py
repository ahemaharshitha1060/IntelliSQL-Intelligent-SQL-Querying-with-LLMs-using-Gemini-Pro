"""
sql.py

Creates a SQLite database for demonstration and populates it with sample data.
"""

import sqlite3


def create_database(db_path: str = "data.db"):
    """Create a SQLite database and a Students table, then insert sample records."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # define table schema
    table = (
        """
        CREATE TABLE IF NOT EXISTS Students (
            NAME TEXT,
            CLASS TEXT,
            Marks INTEGER,
            Company TEXT
        )
        """
    )
    cursor.execute(table)

    # sample data - adjust or extend as needed
    sample_students = [
        ("Sijo", "BTech", 75, "JSW"),
        ("Rahul", "MCom", 82, "INFOSYS"),
        ("Anita", "BSc", 90, "TCS"),
        ("Priya", "MCom", 88, "ACCENTURE"),
        ("Karan", "BTech", 66, "WIPRO"),
    ]

    # insert records if table is empty
    cursor.execute("SELECT COUNT(*) FROM Students")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.executemany(
            "INSERT INTO Students VALUES (?, ?, ?, ?)" , sample_students
        )
        print(f"Inserted {len(sample_students)} sample records into Students table.")
    else:
        print("Students table already contains data; skipping inserts.")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database creation complete. data.db is ready.")
