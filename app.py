from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page (displays tasks)
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add task page
@app.route('/add', methods=('GET', 'POST'))
def add_task():
    if request.method == 'POST':
        task_name = request.form['name']
        task_description = request.form['description']
        task_due = request.form['due_date']

        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (name, description, due_date) VALUES (?, ?, ?)',
                     (task_name, task_description, task_due))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_task.html')

# Delete task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)