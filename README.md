# 📝 My To-Do List

A simple web-based to-do list application built with **Python / Flask** and **SQLite**. Allows you to add tasks, mark them as done, and delete them — all through a clean browser interface.

---

## Features

- Add new tasks
- Mark tasks as completed / uncompleted (toggle)
- Delete tasks
- Persistent storage via SQLite (no external database needed)

---

## Tech Stack

| Layer    | Technology        |
|----------|-------------------|
| Backend  | Python, Flask     |
| Database | SQLite3           |
| Frontend | HTML (Jinja2 templates) |

---

## Project Structure

```
my-to-do-list/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates (Jinja2)
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Didinga/my-to-do-list.git
cd my-to-do-list

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The app will be available at `http://127.0.0.1:5000`.

> The SQLite database (`tasks.db`) is created automatically on first run.

---

## API Routes

| Method | Route               | Description            |
|--------|---------------------|------------------------|
| GET    | `/`                 | List all tasks         |
| POST   | `/add`              | Add a new task         |
| GET    | `/done/<task_id>`   | Toggle task completion |
| GET    | `/delete/<task_id>` | Delete a task          |

---

## Planned Improvements

- [ ] Unit tests
- [ ] Docker support
- [ ] CI/CD pipeline
- [ ] Migrate to FastAPI
- [ ] Switch to PostgreSQL

---

## Author

**Didi** — [github.com/Didinga](https://github.com/Didinga)
