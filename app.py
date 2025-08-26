from flask import Flask, render_template, request, redirect , url_for
from db_config import get_db_connection
import pyodbc

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]
        gender = request.form["gender"]
        department = request.form["department"]
        enrollment_year = request.form["enrollment_year"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Students (name, email, age, gender, department, enrollment_year)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (name, email, age, gender, department, enrollment_year))
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("add_student.html")





@app.route('/add_mood', methods=['GET', 'POST'])
def add_mood():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        student_id = request.form['student_id']
        mood = request.form['mood']
        notes = request.form['notes']

        cursor.execute("INSERT INTO MoodEntries (student_id, entry_date, mood, notes) VALUES (?, GETDATE(), ?, ?)", 
                       student_id, mood, notes)
        conn.commit()
        conn.close()
        return redirect('/')

    # GET: Fetch all students
    cursor.execute("SELECT student_id, name FROM Students")
    students = cursor.fetchall()
    conn.close()
    return render_template('add_mood.html', students=students)



@app.route('/view_mood')
def view_moods():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, entry_date, mood, notes FROM MoodEntries")
    moods = cursor.fetchall()
    conn.close()
    return render_template('view_mood.html', moods=moods)


@app.route('/clear_data', methods=['POST'])
def clear_data():
    DB_CONFIG = "Driver={ODBC Driver 17 for SQL Server};Server=DESKTOP-24OKL7J\MSSQLSERVER01;Database=Tracker;Trusted_Connection=yes;"
    try:
        with pyodbc.connect(DB_CONFIG) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM MoodEntries")  
            conn.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}"
    
    
@app.route('/clear_students', methods=['POST'])
def clear_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Students")
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}"


if __name__ == '__main__':
    app.run(debug=True)
