from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'icct_cainta_secure_key_2026'
DB_NAME = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year_level TEXT NOT NULL,
            section_mode TEXT NOT NULL,
            module_area TEXT NOT NULL,
            assessment_type TEXT NOT NULL,
            score REAL NOT NULL,
            remarks TEXT,
            date TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_accounts (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            linked_student_name TEXT
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM user_accounts")
    if cursor.fetchone()[0] == 0:
        default_accounts = [
            ('admin_icct', 'admin123', 'admin', 'All'),
            ('educator', 'icct2026', 'educator', 'All'),
            ('student_maria', 'student123', 'student', 'Marielle Grace R. Dizon'),
            ('parent_santos', 'parent123', 'parent', 'Marielle Grace R. Dizon'),
            ('student_juan', 'student123', 'student', 'Juan Cruz'),
            ('parent_cruz', 'parent123', 'parent', 'Juan Cruz'),
            ('student_gerald', 'student123', 'student', 'Gerald Ryan Espiritu'),
            ('parent_gerald', 'parent123', 'parent', 'Gerald Ryan Espiritu'),
            ('student_bea', 'student123', 'student', 'Bea Alonzo Sison'),
            ('parent_bea', 'parent123', 'parent', 'Bea Alonzo Sison'),
            ('student_marco', 'student123', 'student', 'Marco Antonio Lim'),
            ('parent_marco', 'parent123', 'parent', 'Marco Antonio Lim'),
            ('student_sarah', 'student123', 'student', 'Sarah Jane Alcantara'),
            ('parent_sarah', 'parent123', 'parent', 'Sarah Jane Alcantara'),
            ('student_bryan', 'student123', 'student', 'Bryan Dave Navarro'),
            ('parent_bryan', 'parent123', 'parent', 'Bryan Dave Navarro'),
            ('student_nica', 'student123', 'student', 'Nica Mae Castillo'),
            ('parent_nica', 'parent123', 'parent', 'Nica Mae Castillo'),
            ('student_kevin', 'student123', 'student', 'Kevin James Morales'),
            ('parent_kevin', 'parent123', 'parent', 'Kevin James Morales'),
            ('student_erika', 'student123', 'student', 'Erika Joy Pascual'),
            ('parent_erika', 'parent123', 'parent', 'Erika Joy Pascual'),
            ('student_jasmine', 'student123', 'student', 'Jasmine Mae Torres'),
            ('parent_jasmine', 'parent123', 'parent', 'Jasmine Mae Torres'),
            ('student_renz', 'student123', 'student', 'Renz Carlo Aquino'),
            ('parent_renz', 'parent123', 'parent', 'Renz Carlo Aquino'),
            ('student_john', 'student123', 'student', 'John Paul Garcia'),
            ('parent_john', 'parent123', 'parent', 'John Paul Garcia'),
            ('student_bea_villanueva', 'student123', 'student', 'Bea Marie Villanueva'),
            ('parent_bea_villanueva', 'parent123', 'parent', 'Bea Marie Villanueva'),
            ('student_kenneth', 'student123', 'student', 'Kenneth Bautista'),
            ('parent_kenneth', 'parent123', 'parent', 'Kenneth Bautista'),
            ('student_samantha', 'student123', 'student', 'Samantha Nicole Gomez'),
            ('parent_samantha', 'parent123', 'parent', 'Samantha Nicole Gomez'),
            ('student_mark', 'student123', 'student', 'Mark Anthony Ramos'),
            ('parent_mark', 'parent123', 'parent', 'Mark Anthony Ramos'),
            ('student_angelica', 'student123', 'student', 'Angelica Santos'),
            ('parent_angelica', 'parent123', 'parent', 'Angelica Santos'),
            ('student_christian', 'student123', 'student', 'Christian Dela Cruz'),
            ('parent_christian', 'parent123', 'parent', 'Christian Dela Cruz'),
            ('student_patricia', 'student123', 'student', 'Patricia Reyes'),
            ('parent_patricia', 'parent123', 'parent', 'Patricia Reyes'),
            ('student_joshua', 'student123', 'student', 'Joshua Mendoza'),
            ('parent_joshua', 'parent123', 'parent', 'Joshua Mendoza')
        ]
        cursor.executemany(
            "INSERT INTO user_accounts (username, password, role, linked_student_name) VALUES (?, ?, ?, ?)", 
            default_accounts
        )
        
        sample_students = [
            ('Marielle Grace R. Dizon', '3rd Year', 'OLCA311N072', 'Object-Oriented Programming', 'Exam', 94.5, 'Passed with Highest Honors', '2026-10-18'),
            ('Joshua Mendoza', '1st Year', 'BSIT-1A', 'Information Management', 'Activity 1', 82.0, 'Passed', '2026-10-18'),
            ('Patricia Reyes', '1st Year', 'BSIT-1B', 'Data Structures & Algorithms', 'Pre-test 3', 78.5, 'Passed', '2026-10-17'),
            ('Christian Dela Cruz', '2nd Year', 'BSIT-2A', 'Operating Systems', 'Post-test 2', 82.0, 'Passed with Honors', '2026-10-17'),
            ('Angelica Santos', '2nd Year', 'BSIT-2B', 'Computer Networking', 'Project Prelim', 89.0, 'Passed with Honors', '2026-10-16'),
            ('Mark Anthony Ramos', '3rd Year', 'BSIT-3A', 'Advanced Database System', 'Project Midterm', 91.0, 'Excellent Performance', '2026-10-16'),
            ('Samantha Nicole Gomez', '3rd Year', 'BSIT-3B', 'Systems Integration & Architecture 1', 'Activity 4', 84.5, 'Passed', '2026-10-15'),
            ('Kenneth Bautista', '3rd Year', 'BSIT-3C', 'Social Issues and Professional Practice 2', 'Exam', 86.0, 'Passed', '2026-10-15'),
            ('Bea Marie Villanueva', '4th Year', 'BSIT-4A', 'Capstone Project 1', 'Project Final', 95.0, 'Passed with Highest Honors', '2026-10-14'),
            ('John Paul Garcia', '3rd Year', 'BSIT-3E1', 'Information Assurance & Security', 'Activity 2', 80.0, 'Passed', '2026-10-14'),
            ('Renz Carlo Aquino', '3rd Year', 'OLCA311M001', 'Object-Oriented Programming', 'Project Midterm', 88.0, 'Passed with Honors', '2026-10-18'),
            ('Jasmine Mae Torres', '1st Year', 'BSIT-1A', 'Information Management', 'Pre-test 1', 91.5, 'Excellent Performance', '2026-10-18'),
            ('Erika Joy Pascual', '2nd Year', 'BSIT-2A', 'Data Structures & Algorithms', 'Activity 2', 81.5, 'Passed', '2026-10-17'),
            ('Kevin James Morales', '3rd Year', 'BSIT-3A', 'Advanced Database System', 'Exam', 92.5, 'Passed with Honors', '2026-10-17'),
            ('Nica Mae Castillo', '4th Year', 'BSIT-4B', 'Capstone Project 2', 'Project Final', 96.0, 'Passed with Highest Honors', '2026-10-16'),
            ('Bryan Dave Navarro', '3rd Year', 'BSIT-3E2', 'Information Assurance & Security', 'Post-test 4', 83.0, 'Passed', '2026-10-16'),
            ('Sarah Jane Alcantara', '1st Year', 'BSIT-1B', 'Computer Networking', 'Activity 3', 85.5, 'Passed', '2026-10-15'),
            ('Marco Antonio Lim', '2nd Year', 'BSIT-2B', 'Operating Systems', 'Exam', 76.0, 'Passed', '2026-10-15'),
            ('Bea Alonzo Sison', '3rd Year', 'OLCA311A023', 'Systems Integration & Architecture 1', 'Project Midterm', 89.5, 'Passed with Honors', '2026-10-14'),
            ('Gerald Ryan Espiritu', '4th Year', 'BSIT-4A', 'Social Issues and Professional Practice 2', 'Activity 5', 90.0, 'Excellent Performance', '2026-10-14')
        ]
        cursor.executemany(
            "INSERT INTO students (name, year_level, section_mode, module_area, assessment_type, score, remarks, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
            sample_students
        )
        conn.commit()
    conn.close()

init_db()

@app.before_request
def require_login():
    allowed_routes = ['login', 'static']
    if 'user' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))

@app.route('/')
def index():
    role = session.get('role')
    linked_name = session.get('linked_student')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if role in ['student', 'parent']:
        cursor.execute("SELECT * FROM students WHERE name = ? ORDER BY id DESC", (linked_name,))
        records = cursor.fetchall()
        conn.close()
        return render_template('student_tracker.html', records=records, student_name=linked_name, role=role)
    else:
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT 5")
        recent_records = cursor.fetchall()
        conn.close()
        return render_template('index.html', total_students=total_students, recent_records=recent_records)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        username = data.get('username')
        password = data.get('password')
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT username, role, linked_student_name FROM user_accounts WHERE username = ? AND password = ?", (username, password))
        account = cursor.fetchone()
        conn.close()
        
        if account:
            session['user'] = account[0]
            session['role'] = account[1]
            session['linked_student'] = account[2]
            
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('index')})
            return redirect(url_for('index'))
        else:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/access-denied')
def access_denied():
    return render_template('access_denied.html')

@app.route('/student-tracker')
def student_tracker():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    role = session.get('role')
    linked_name = session.get('linked_student')
    
    if role in ['student', 'parent']:
        cursor.execute("SELECT * FROM students WHERE name = ? ORDER BY id DESC", (linked_name,))
        display_name = linked_name
    else:
        cursor.execute("SELECT * FROM students ORDER BY id DESC")
        display_name = "All Students"
        
    records = cursor.fetchall()
    conn.close()
    return render_template('student_tracker.html', records=records, student_name=display_name, role=role)

@app.route('/students', methods=['GET', 'POST'])
def students():
    if session.get('role') not in ['admin', 'educator']:
        return redirect(url_for('access_denied'))
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form.get('name')
        year_level = request.form.get('year_level')
        
        reg_sec = request.form.get('regular_section')
        tri_code = request.form.get('trimester_code')
        spec_sec = request.form.get('special_section')
        
        section_mode = reg_sec or tri_code or spec_sec or 'N/A'
        
        module_area = request.form.get('module_area')
        assessment_type = request.form.get('assessment_type')
        score = request.form.get('score')
        remarks = request.form.get('remarks')
        date = request.form.get('date')
        
        cursor.execute('''
            INSERT INTO students (name, year_level, section_mode, module_area, assessment_type, score, remarks, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, year_level, section_mode, module_area, assessment_type, score, remarks, date))
        conn.commit()
        flash('Student record successfully saved!', 'success')
        
    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students_list = cursor.fetchall()
    conn.close()
    return render_template('students.html', students=students_list)

@app.route('/assessment')
def assessment():
    if session.get('role') not in ['admin', 'educator']:
        return redirect(url_for('access_denied'))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY date DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template('assessment.html', records=records)

@app.route('/reports')
def reports():
    if session.get('role') not in ['admin', 'educator']:
        return redirect(url_for('access_denied'))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template('reports.html', records=records)

@app.route('/curriculum')
def curriculum():
    if session.get('role') not in ['admin', 'educator']:
        return redirect(url_for('access_denied'))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT module_area, AVG(score), COUNT(*) FROM students GROUP BY module_area")
    modules = cursor.fetchall()
    conn.close()
    return render_template('curriculum.html', modules=modules)

@app.route('/portal')
def portal():
    if session.get('role') not in ['admin', 'educator']:
        return redirect(url_for('access_denied'))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT 10")
    records = cursor.fetchall()
    conn.close()
    return render_template('portal.html', records=records)

@app.route('/insights')
def insights():
    if session.get('role') not in ['admin', 'educator']:
        return redirect(url_for('access_denied'))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE score < 75 ORDER BY score ASC")
    remediation_needed = cursor.fetchall()
    conn.close()
    return render_template('insights.html', records=remediation_needed)

if __name__ == '__main__':
    app.run(debug=True, port=5000)