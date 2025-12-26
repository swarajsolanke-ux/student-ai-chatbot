
import sqlite3

def init_db(db_name="chatbot.db"):
    """Creates the database and the necessary tables."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            email TEXT,
            auth_provider TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Student Profiles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT,
            nationality TEXT,
            gpa REAL,
            budget INTEGER,
            preferred_country TEXT,
            preferred_major TEXT,
            learning_style TEXT,
            career_goal TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    print(f"Database '{db_name}' initialized with schema.")
    return conn

def seed_data(conn):
    """Inserts dummy data into the tables."""
    cursor = conn.cursor()

    # 1. Insert Dummy Users
    users = [
        ('+123456789', 'john.doe@example.com', 'google'),
        ('+987654321', 'sara.smith@example.com', 'email')
    ]
    
    cursor.executemany(
        "INSERT INTO users (phone, email, auth_provider) VALUES (?, ?, ?)", 
        users
    )

    # 2. Insert Dummy Student Profiles
    # Linking user_id 1 to John and user_id 2 to Sara
    profiles = [
        (1, 'John Doe', 'Canada', 3.8, 25000, 'Germany', 'Computer Science', 'Visual', 'Software Architect'),
        (2, 'Sara Smith', 'UK', 3.5, 15000, 'Netherlands', 'Mechanical Engineering', 'Practical', 'Robotics Engineer')
    ]

    cursor.executemany('''
        INSERT INTO student_profiles (
            user_id, full_name, nationality, gpa, budget, 
            preferred_country, preferred_major, learning_style, career_goal
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', profiles)

    conn.commit()
    print("Dummy data inserted successfully.")


def init_university_db(db_name="chatbot.db"):
    """Creates tables for Universities, Majors, and their relationships."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 1. Create Universities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS universities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT,
            tuition_fee INTEGER,
            min_gpa REAL,
            language TEXT,
            scholarship_available INTEGER, -- 1 for Yes, 0 for No
            success_weight REAL DEFAULT 1.0
        )
    ''')

    # 2. Create Majors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS majors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            difficulty TEXT,
            career_paths TEXT,
            average_cost INTEGER
        )
    ''')

    # 3. Create Junction Table (Many-to-Many)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS university_majors (
            university_id INTEGER,
            major_id INTEGER,
            FOREIGN KEY(university_id) REFERENCES universities(id),
            FOREIGN KEY(major_id) REFERENCES majors(id)
        )
    ''')

    conn.commit()
    print(f"University schema initialized in '{db_name}'.")
    return conn

def seed_university_data(conn):
    """Inserts dummy data for universities and majors."""
    cursor = conn.cursor()

    # Insert Universities
    unis = [
        ('Technical University of Munich', 'Germany', 0, 3.5, 'English', 1, 1.2),
        ('University of Amsterdam', 'Netherlands', 12000, 3.0, 'English', 1, 1.0),
        ('MIT', 'USA', 55000, 3.9, 'English', 0, 1.5)
    ]
    cursor.executemany('''
        INSERT INTO universities (name, country, tuition_fee, min_gpa, language, scholarship_available, success_weight)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', unis)

    # Insert Majors
    majors = [
        ('Computer Science', 'Hard', 'Software Engineer, Data Scientist', 15000),
        ('Mechanical Engineering', 'Hard', 'Aerospace Engineer, Robotics', 12000),
        ('Business Administration', 'Medium', 'Manager, Consultant', 20000),
        ("AI and Data Science","Medium","AI engineer , Machine learning",25000),
        ("Electrical Engineering","Hard","Design engineer",300000),
        
    ]
    cursor.executemany('''
        INSERT INTO majors (name, difficulty, career_paths, average_cost)
        VALUES (?, ?, ?, ?)
    ''', majors)

    # Link Universities to Majors (Junction Data)
    # 1: TUM -> CS (1) and MechEng (2)
    # 2: Amsterdam -> CS (1) and Business (3)
    links = [(1, 1), (1, 2), (2, 1), (2, 3), (3, 1)]
    cursor.executemany("INSERT INTO university_majors (university_id, major_id) VALUES (?, ?)", links)

    conn.commit()
    print("University and Major dummy data seeded.")


def init_operations_db(db_name="chatbot.db"):
    """Initializes the operational tables: Applications, Scholarships, AI Weights, and Documents."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 1. Create Applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            university_id INTEGER,
            status TEXT CHECK(status IN ('Pending', 'Accepted', 'Rejected', 'Under Review')),
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(university_id) REFERENCES universities(id)
        )
    ''')

    # 2. Create Scholarships table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT,
            min_gpa REAL,
            deadline DATE
        )
    ''')

    # 3. Create AI Weights table (Global settings for the recommender)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acceptance_rate_weight REAL,
            scholarship_weight REAL,
            success_history_weight REAL,
            feedback_weight REAL
        )
    ''')

    # 4. Create Documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            doc_type TEXT, -- e.g., 'Passport', 'Transcript', 'IELTS'
            file_path TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    print(f"Operational schema initialized in '{db_name}'.")
    return conn

def seed_operations_data(conn):
    """Inserts dummy data for testing the application workflow."""
    cursor = conn.cursor()

    # Seed Scholarships
    scholarships = [
        ('DAAD Scholarship', 'Germany', 3.7, '2025-10-15'),
        ('Holland Scholarship', 'Netherlands', 3.0, '2025-05-01'),
        ('Chevening Award', 'UK', 3.5, '2025-11-01')
    ]
    cursor.executemany('INSERT INTO scholarships (name, country, min_gpa, deadline) VALUES (?, ?, ?, ?)', scholarships)

    # Seed AI Weights (The "Brain" settings for your AI recommender)
    cursor.execute('''
        INSERT INTO ai_weights (acceptance_rate_weight, scholarship_weight, success_history_weight, feedback_weight)
        VALUES (0.3, 0.4, 0.2, 0.1)
    ''')

    # Seed Dummy Applications (Assuming user_id 1 and university_id 1 exist)
    applications = [
        (1, 1, 'Pending'),
        (2, 2, 'Under Review')
    ]
    cursor.executemany('INSERT INTO applications (user_id, university_id, status) VALUES (?, ?, ?)', applications)

    # Seed Dummy Documents
    docs = [
        (1, 'Transcript', '/uploads/user1/transcript.pdf'),
        (1, 'Passport', '/uploads/user1/id.jpg')
    ]
    cursor.executemany('INSERT INTO documents (user_id, doc_type, file_path) VALUES (?, ?, ?)', docs)

    conn.commit()
    print("Operational dummy data seeded successfully.")



if __name__ == "__main__":
    # Run the setup
    connection = init_db()
    seed_data(connection)
    connection.close()
    connection = init_university_db()
    seed_university_data(connection)
    connection.close()
    connection = init_operations_db()
    seed_operations_data(connection)
    connection.close()