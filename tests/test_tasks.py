import pytest

TASK = {
    "header": "string",
    "text": "string",
    "completion_date": "2022-06-26"
}


def test_create_task_pos_one_task(client):
    response = client.post("/tasks/create/", json=TASK)
    assert response.status_code == 200
    assert response.json() == {
        "completion_date": "2022-06-26",
        "id": 1,
        "text": "string",
        "is_completed": False,
        "header": "string"
    }


def test_create_task_neg_without_field(client):
    incorrect_task = {
        "header": "str",
        "completion_date": "2022-06-26"
    }
    response = client.post("/tasks/create/", json=incorrect_task)

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"


def test_create_task_neg_not_valid_date(client):
    incorrect_task = {
        'header': "str",
        'text': "",
        'completion_date': 'not_a_date'
    }
    response = client.post("/tasks/create/", json=incorrect_task)

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "invalid date format"


def test_get_task_by_id_pos(client):
    client.post("/tasks/create/", json=TASK)
    response = client.get(f"/tasks/get/1")
    assert response.status_code == 200
    assert response.json() == {
        "header": "string",
        "text": "string",
        "completion_date": "2022-06-26",
        "id": 1,
        "is_completed": False
    }


def test_get_task_by_id_neg(client):
    response = client.get(f"/tasks/get/88005553535")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task with id = 88005553535, not found!"
    }


def test_get_task_by_id_wrong_id(client):
    response = client.get("/task/get/2,5")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_get_tasks_pos(client):
    response1 = client.post("/tasks/create/", json=TASK)
    response2 = client.post("/tasks/create/", json=TASK)
    get_response = client.get("/tasks/")

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert get_response.json() == [
        {"completion_date": "2022-06-26",
         "id": 1,
         "text": "string",
         "is_completed": False,
         "header": "string"},
        {"completion_date": "2022-06-26",
         "id": 2,
         "text": "string",
         "is_completed": False,
         "header": "string"}]


def test_get_tasks_empty_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_complete_task_pos(client):
    client.post("/tasks/create/", json=TASK)
    response = client.patch("/tasks/complete/1", json={'is_completed': True})
    get_response = client.get("/task/get/1")
    assert response.status_code == 200
    assert response.json() == "Task with id = 1, field 'is_completed' = True"
    assert get_response.json()["is_completed"] == True


def test_complete_task_not_found(client):
    response = client.patch("/tasks/complete/1", json={'is_completed': True})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with id = 35, not found!"}


def test_complete_task_without_field(client):
    client.post("/tasks/create/", json=TASK)
    response = client.patch("/tasks/complete/1", json={'task_id': 1})
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "field required"


def test_delete_task_pos(client):
    client.post("/tasks/create/", json=TASK)
    response = client.delete('/tasks/delete/1')
    assert response.status_code == 200
    assert response.json() == {"OK": True}


def test_delete_task_not_found(client):
    response = client.delete('/tasks/delete/1')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with id = 1, not found!"}
