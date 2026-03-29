import sqlite3
import pandas as pd

DATABASE = "database.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """Create Users, Jobs, and Recommendations tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            skills TEXT NOT NULL,
            experience INTEGER NOT NULL
        )
    ''')

    # Jobs Table — uses description instead of skills_required
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    # Recommendations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            score REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        )
    ''')

    conn.commit()
    conn.close()
    print(" Tables created successfully.")


def load_jobs_from_csv(csv_path="data.csv"):
    """Load jobs from CSV file into the Jobs table."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if jobs are already loaded
    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    if count > 0:
        print(" Jobs already loaded in database. Skipping.")
        conn.close()
        return

    # Load and insert jobs from CSV
    df = pd.read_csv(csv_path)
    df.dropna(subset=['Job Title', 'Description'], inplace=True)

    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO jobs (job_title, description)
            VALUES (?, ?)
        ''', (row['Job Title'], row['Description']))

    conn.commit()
    conn.close()
    print(f" {len(df)} jobs loaded into database.")


def add_user(name, email, skills, experience):
    """Insert a new user into the Users table."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (name, email, skills, experience)
            VALUES (?, ?, ?, ?)
        ''', (name, email, skills, experience))
        conn.commit()
        user_id = cursor.lastrowid
        print(f" User '{name}' added with ID {user_id}.")
        return user_id
    except sqlite3.IntegrityError:
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_id = cursor.fetchone()[0]
        print(f" User already exists. Using ID {user_id}.")
        return user_id
    finally:
        conn.close()


def save_recommendations(user_id, recommendations):
    """Save recommendation results to the Recommendations table."""
    conn = get_connection()
    cursor = conn.cursor()

    for rec in recommendations:
        cursor.execute('''
            INSERT INTO recommendations (user_id, job_id, score)
            VALUES (?, ?, ?)
        ''', (user_id, rec['job_id'], rec['score']))

    conn.commit()
    conn.close()
    print(f"✅ {len(recommendations)} recommendations saved for user ID {user_id}.")


def get_all_jobs():
    """Fetch all jobs from the Jobs table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jobs


def initialize_database():
    """Run this once to set up everything."""
    create_tables()
    load_jobs_from_csv()


if __name__ == "__main__":
    initialize_database()