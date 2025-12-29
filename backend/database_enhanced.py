
import sqlite3
from datetime import datetime

def create_enhanced_schema(db_name="University.db"):
    """Creates comprehensive database schema for the platform"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # ============= USER MANAGEMENT =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            auth_provider TEXT,
            is_active INTEGER DEFAULT 1,
            is_premium INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otp_verification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT,
            otp_code TEXT,
            expires_at TIMESTAMP,
            is_verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            full_name TEXT,
            nationality TEXT,
            date_of_birth DATE,
            gpa REAL,
            budget INTEGER,
            preferred_country TEXT,
            preferred_major TEXT,
            learning_style TEXT,
            career_goal TEXT,
            bio TEXT,
            profile_image TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # ============= ASSESSMENT SYSTEM =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessment_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_type TEXT CHECK(test_type IN ('personality', 'academic', 'thinking', 'learning', 'interests', 'career')),
            questions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            test_type TEXT,
            answers TEXT,
            scores TEXT,
            personality_type TEXT,
            strengths TEXT,
            weaknesses TEXT,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS major_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            major_name TEXT,
            match_score REAL,
            explanation TEXT,
            difficulty_level TEXT,
            career_paths TEXT,
            estimated_cost INTEGER,
            study_duration TEXT,
            roadmap TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # ============= UNIVERSITY SYSTEM =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS universities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT,
            city TEXT,
            tuition_fee INTEGER,
            min_gpa REAL,
            language TEXT,
            scholarship_available INTEGER DEFAULT 0,
            success_weight REAL DEFAULT 1.0,
            overview TEXT,
            duration TEXT,
            accommodation_info TEXT,
            website TEXT,
            ranking INTEGER,
            acceptance_rate REAL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS university_media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            university_id INTEGER,
            media_type TEXT CHECK(media_type IN ('image', 'video')),
            media_url TEXT,
            caption TEXT,
            display_order INTEGER DEFAULT 0,
            FOREIGN KEY(university_id) REFERENCES universities(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS majors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
            career_paths TEXT,
            average_cost INTEGER,
            description TEXT,
            required_skills TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS university_majors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            university_id INTEGER,
            major_id INTEGER,
            tuition_fee INTEGER,
            duration_years INTEGER,
            special_requirements TEXT,
            FOREIGN KEY(university_id) REFERENCES universities(id) ON DELETE CASCADE,
            FOREIGN KEY(major_id) REFERENCES majors(id) ON DELETE CASCADE,
            UNIQUE(university_id, major_id)
        )
    ''')
    
    # ============= APPLICATION SYSTEM =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            university_id INTEGER,
            major_id INTEGER,
            status TEXT CHECK(status IN ('Draft', 'Submitted', 'Under Review', 'Missing Documents', 'Conditional Offer', 'Final Offer', 'Rejected')) DEFAULT 'Draft',
            application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            admin_notes TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(university_id) REFERENCES universities(id),
            FOREIGN KEY(major_id) REFERENCES majors(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS application_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER,
            document_type TEXT,
            file_path TEXT,
            file_name TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_verified INTEGER DEFAULT 0,
            FOREIGN KEY(application_id) REFERENCES applications(id) ON DELETE CASCADE
        )
    ''')
    
    # ============= DOCUMENT MANAGEMENT =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            doc_type TEXT,
            file_path TEXT,
            file_name TEXT,
            file_size INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # ============= SCHOLARSHIP SYSTEM =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT,
            provider TEXT,
            min_gpa REAL,
            max_age INTEGER,
            nationality_requirement TEXT,
            coverage TEXT,
            amount INTEGER,
            deadline DATE,
            description TEXT,
            required_documents TEXT,
            website TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scholarship_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            scholarship_id INTEGER,
            status TEXT CHECK(status IN ('Draft', 'Submitted', 'Under Review', 'Approved', 'Rejected')) DEFAULT 'Draft',
            eligibility_score REAL,
            submitted_at TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(scholarship_id) REFERENCES scholarships(id)
        )
    ''')
    
    # ============= STUDENT SERVICES =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT CHECK(category IN ('car', 'bank', 'telecom', 'travel')),
            description TEXT,
            logo_url TEXT,
            website TEXT,
            contact_email TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partner_id INTEGER,
            title TEXT,
            description TEXT,
            discount_percentage REAL,
            terms TEXT,
            image_url TEXT,
            valid_until DATE,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY(partner_id) REFERENCES partners(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            partner_id INTEGER,
            offer_id INTEGER,
            student_name TEXT,
            student_email TEXT,
            student_phone TEXT,
            message TEXT,
            status TEXT DEFAULT 'New',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(partner_id) REFERENCES partners(id),
            FOREIGN KEY(offer_id) REFERENCES service_offers(id)
        )
    ''')
    
    # ============= PAYMENT SYSTEM =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS premium_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_name TEXT,
            description TEXT,
            price REAL,
            duration_days INTEGER,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            feature_id INTEGER,
            amount REAL,
            currency TEXT DEFAULT 'KWD',
            payment_method TEXT CHECK(payment_method IN ('KNET', 'ApplePay', 'Card')),
            transaction_id TEXT,
            status TEXT CHECK(status IN ('Pending', 'Completed', 'Failed', 'Refunded')) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(feature_id) REFERENCES premium_features(id)
        )
    ''')
    
    # ============= NOTIFICATION SYSTEM =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            message TEXT,
            type TEXT CHECK(type IN ('info', 'success', 'warning', 'error')),
            is_read INTEGER DEFAULT 0,
            link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # ============= AI CONFIGURATION =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acceptance_rate_weight REAL DEFAULT 0.3,
            scholarship_weight REAL DEFAULT 0.4,
            success_history_weight REAL DEFAULT 0.2,
            feedback_weight REAL DEFAULT 0.1,
            gpa_weight REAL DEFAULT 0.3,
            budget_weight REAL DEFAULT 0.25,
            assessment_weight REAL DEFAULT 0.45,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_success_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            university_id INTEGER,
            major_id INTEGER,
            student_gpa REAL,
            student_profile TEXT,
            admission_result TEXT CHECK(admission_result IN ('Accepted', 'Rejected')),
            scholarship_received INTEGER DEFAULT 0,
            year INTEGER,
            embedding_id TEXT,
            FOREIGN KEY(university_id) REFERENCES universities(id),
            FOREIGN KEY(major_id) REFERENCES majors(id)
        )
    ''')
    
    # ============= CHAT HISTORY =============
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id TEXT UNIQUE,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT CHECK(role IN ('user', 'assistant', 'system')),
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_applications_user ON applications(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_universities_country ON universities(country)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON chat_messages(session_id)')
    
    conn.commit()
    print(f"Enhanced database schema created successfully in '{db_name}'")
    return conn


def seed_enhanced_data(conn):
    """Seed comprehensive sample data"""
    cursor = conn.cursor()
    
    # Seed AI Weights (if not exists)
    cursor.execute('SELECT COUNT(*) FROM ai_weights')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO ai_weights 
            (acceptance_rate_weight, scholarship_weight, success_history_weight, feedback_weight, gpa_weight, budget_weight, assessment_weight)
            VALUES (0.3, 0.4, 0.2, 0.1, 0.3, 0.25, 0.45)
        ''')
    
    # Seed Majors
    majors_data = [
        ('Computer Science', 'Technology', 'Hard', 'Software Engineer, Data Scientist, AI Specialist', 15000, 'Study of computation, algorithms, and software development', 'Programming, Mathematics, Logic'),
        ('Mechanical Engineering', 'Engineering', 'Hard', 'Aerospace Engineer, Robotics Specialist, Design Engineer', 12000, 'Design and analysis of mechanical systems', 'Physics, Mathematics, CAD'),
        ('Business Administration', 'Business', 'Medium', 'Manager, Consultant, Entrepreneur', 20000, 'Principles of business management and operations', 'Communication, Leadership, Analytics'),
        ('AI and Data Science', 'Technology', 'Hard', 'AI Engineer, Machine Learning Specialist, Data Analyst', 25000, 'Artificial intelligence and data analysis', 'Programming, Statistics, Mathematics'),
        ('Electrical Engineering', 'Engineering', 'Hard', 'Electronics Designer, Power Systems Engineer', 18000, 'Study of electrical systems and electronics', 'Physics, Mathematics, Circuit Design'),
        ('Medicine', 'Health', 'Hard', 'Doctor, Surgeon, Medical Researcher', 50000, 'Medical science and healthcare', 'Biology, Chemistry, Critical Thinking'),
        ('Psychology', 'Social Science', 'Medium', 'Psychologist, Counselor, Researcher', 10000, 'Study of human behavior and mental processes', 'Empathy, Analysis, Communication'),
        ('Civil Engineering', 'Engineering', 'Hard', 'Structural Engineer, Construction Manager', 15000, 'Design and construction of infrastructure', 'Physics, Mathematics, CAD'),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO majors (name, category, difficulty, career_paths, average_cost, description, required_skills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', majors_data)
    
    # Seed Universities
    universities_data = [
        ('Technical University of Munich', 'Germany', 'Munich', 0, 3.5, 'English/German', 1, 1.3, 
         'Top technical university in Germany with excellent research facilities', '3-4 years', 
         'Student dormitories and apartments available', 'https://www.tum.de', 50, 0.15),
        ('University of Amsterdam', 'Netherlands', 'Amsterdam', 12000, 3.0, 'English', 1, 1.1,
         'Leading research university in the Netherlands', '3 years',
         'University housing and private rentals', 'https://www.uva.nl', 62, 0.25),
        ('MIT', 'USA', 'Cambridge', 55000, 3.9, 'English', 0, 1.5,
         'World-renowned institution for technology and innovation', '4 years',
         'On-campus housing guaranteed', 'https://www.mit.edu', 1, 0.04),
        ('University of Toronto', 'Canada', 'Toronto', 45000, 3.6, 'English', 1, 1.2,
         'Canada\'s top university with diverse programs', '4 years',
         'Residence halls and off-campus housing', 'https://www.utoronto.ca', 18, 0.43),
        ('ETH Zurich', 'Switzerland', 'Zurich', 1500, 3.7, 'English/German', 1, 1.4,
         'Leading science and technology university', '3 years',
         'Student housing available', 'https://ethz.ch', 6, 0.08),
        ('National University of Singapore', 'Singapore', 'Singapore', 30000, 3.5, 'English', 1, 1.2,
         'Asia\'s leading global university', '4 years',
         'University halls and apartments', 'https://www.nus.edu.sg', 11, 0.05),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO universities 
        (name, country, city, tuition_fee, min_gpa, language, scholarship_available, success_weight, 
         overview, duration, accommodation_info, website, ranking, acceptance_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', universities_data)
    
    # Link universities to majors
    cursor.execute('SELECT id FROM universities')
    uni_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute('SELECT id FROM majors')
    major_ids = [row[0] for row in cursor.fetchall()]
    
    university_major_links = []
    for uni_id in uni_ids[:3]:  # First 3 universities
        for major_id in major_ids[:4]:  # First 4 majors
            university_major_links.append((uni_id, major_id, None, 3, None))
    
    cursor.executemany('''
        INSERT OR IGNORE INTO university_majors (university_id, major_id, tuition_fee, duration_years, special_requirements)
        VALUES (?, ?, ?, ?, ?)
    ''', university_major_links)
    
    # Seed Scholarships
    scholarships_data = [
        ('DAAD Scholarship', 'Germany', 'German Academic Exchange Service', 3.7, 30, 'All nationalities', 'Full tuition + living expenses', 
         12000, '2025-10-15', 'Prestigious German scholarship for international students', 'Transcript, Recommendation Letters, Motivation Letter', 'https://www.daad.de'),
        ('Holland Scholarship', 'Netherlands', 'Dutch Ministry of Education', 3.0, 35, 'Non-EU', 'Partial tuition', 
         5000, '2025-05-01', 'Scholarship for non-EU students studying in the Netherlands', 'Acceptance Letter, Transcript', 'https://www.studyinholland.nl'),
        ('Chevening Scholarship', 'UK', 'UK Government', 3.5, 99, 'All except UK', 'Full tuition + living', 
         25000, '2025-11-01', 'UK government global scholarship program', 'IELTS, Recommendation Letters, Essay', 'https://www.chevening.org'),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO scholarships 
        (name, country, provider, min_gpa, max_age, nationality_requirement, coverage, amount, deadline, description, required_documents, website)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', scholarships_data)
    
    # Seed Premium Features
    premium_features = [
        ('Advanced AI Guidance', 'Get personalized major recommendations and detailed study roadmaps', 9.99, 30),
        ('Priority Applications', 'Fast-track your university applications with priority processing', 14.99, 60),
        ('Premium Comparisons', 'Compare unlimited universities with detailed analytics', 4.99, 30),
        ('Expert Consultation', '1-on-1 consultation with education experts', 49.99, 0),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO premium_features (feature_name, description, price, duration_days)
        VALUES (?, ?, ?, ?)
    ''', premium_features)
    
    # Seed Partner Services
    partners_data = [
        ('Student Auto', 'car', 'Special car deals for students', '/static/images/partners/cars.jpg', 'https://studentauto.com', 'offers@studentauto.com'),
        ('Campus Bank', 'bank', 'Student banking solutions with zero fees', '/static/images/partners/bank.jpg', 'https://campusbank.com', 'student@campusbank.com'),
        ('EduTel', 'telecom', 'Student mobile and data packages', '/static/images/partners/telecom.jpg', 'https://edutel.com', 'support@edutel.com'),
        ('StudyTravel', 'travel', 'Student flight deals and visa assistance', '/static/images/partners/travel.jpg', 'https://studytravel.com', 'booking@studytravel.com'),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO partners (name, category, description, logo_url, website, contact_email)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', partners_data)
    
    conn.commit()
    print("Enhanced sample data seeded successfully")


if __name__ == "__main__":
    # Create and seed database
    connection = create_enhanced_schema()
    seed_enhanced_data(connection)
    connection.close()
    print("Database setup complete!")
