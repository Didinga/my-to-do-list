from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, content TEXT, completed INTEGER DEFAULT 0)')

@app.route('/')
def index():
    with sqlite3.connect('tasks.db') as conn:
        tasks = conn.execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        with sqlite3.connect('tasks.db') as conn:
            conn.execute('INSERT INTO tasks (content) VALUES (?)', (task,))
    return redirect('/')

@app.route('/done/<int:task_id>')
def done(task_id):
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('UPDATE tasks SET completed = 1 - completed WHERE id = ?', (task_id,))
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
