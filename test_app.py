import sqlite3

import pytest

import app as app_module


@pytest.fixture
def client(tmp_path):
    """Fresh Flask test client with its own temp SQLite DB for each test."""
    db_path = tmp_path / "test_tasks.db"
    app_module.app.config['DATABASE'] = str(db_path)
    app_module.app.config['TESTING'] = True
    app_module.init_db()

    with app_module.app.test_client() as test_client:
        yield test_client


def get_all_tasks(db_path):
    with sqlite3.connect(db_path) as conn:
        return conn.execute('SELECT id, content, completed FROM tasks').fetchall()


def test_index_empty(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'To-Do List'.encode('utf-8') in response.data


def test_add_task(client):
    response = client.post('/add', data={'task': 'Koupit mléko'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Koupit mléko'.encode('utf-8') in response.data

    tasks = get_all_tasks(app_module.get_db_path())
    assert len(tasks) == 1
    assert tasks[0][1] == 'Koupit mléko'
    assert tasks[0][2] == 0


def test_add_task_empty_string_is_ignored(client):
    client.post('/add', data={'task': '   '}, follow_redirects=True)
    tasks = get_all_tasks(app_module.get_db_path())
    assert tasks == []


def test_add_task_missing_field_is_ignored(client):
    client.post('/add', data={}, follow_redirects=True)
    tasks = get_all_tasks(app_module.get_db_path())
    assert tasks == []


def test_add_task_too_long_is_ignored(client):
    long_task = 'x' * 201
    client.post('/add', data={'task': long_task}, follow_redirects=True)
    tasks = get_all_tasks(app_module.get_db_path())
    assert tasks == []


def test_add_task_exactly_max_length_is_saved(client):
    max_task = 'x' * 200
    client.post('/add', data={'task': max_task}, follow_redirects=True)
    tasks = get_all_tasks(app_module.get_db_path())
    assert len(tasks) == 1


def test_toggle_done(client):
    client.post('/add', data={'task': 'Uklidit pokoj'}, follow_redirects=True)
    task_id = get_all_tasks(app_module.get_db_path())[0][0]

    client.post(f'/done/{task_id}', follow_redirects=True)
    tasks = get_all_tasks(app_module.get_db_path())
    assert tasks[0][2] == 1

    # Toggling again should flip it back to not completed
    client.post(f'/done/{task_id}', follow_redirects=True)
    tasks = get_all_tasks(app_module.get_db_path())
    assert tasks[0][2] == 0


def test_done_get_method_not_allowed(client):
    client.post('/add', data={'task': 'Test'}, follow_redirects=True)
    task_id = get_all_tasks(app_module.get_db_path())[0][0]

    response = client.get(f'/done/{task_id}')
    assert response.status_code == 405


def test_done_nonexistent_task_is_noop(client):
    response = client.post('/done/9999', follow_redirects=True)
    assert response.status_code == 200
    assert get_all_tasks(app_module.get_db_path()) == []


def test_delete_task(client):
    client.post('/add', data={'task': 'Smazat mě'}, follow_redirects=True)
    task_id = get_all_tasks(app_module.get_db_path())[0][0]

    client.post(f'/delete/{task_id}', follow_redirects=True)
    assert get_all_tasks(app_module.get_db_path()) == []


def test_delete_get_method_not_allowed(client):
    client.post('/add', data={'task': 'Test'}, follow_redirects=True)
    task_id = get_all_tasks(app_module.get_db_path())[0][0]

    response = client.get(f'/delete/{task_id}')
    assert response.status_code == 405


def test_delete_nonexistent_task_is_noop(client):
    response = client.post('/delete/9999', follow_redirects=True)
    assert response.status_code == 200


def test_add_task_does_not_allow_sql_injection(client):
    malicious = "'); DROP TABLE tasks; --"
    client.post('/add', data={'task': malicious}, follow_redirects=True)

    tasks = get_all_tasks(app_module.get_db_path())
    assert len(tasks) == 1
    assert tasks[0][1] == malicious
