import requests
import uuid
ENDPOINT = "https://todo.pixegami.io"


def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    print(f"creating task for user{user_id} with content {content}")
    payload = {
        "content": content,
        "user_id": user_id,
        "is_done": False
    }
    return payload


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    pass


def test_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    create_task_data = create_task_response.json()
    print(create_task_data)

    task_id = create_task_data["task"]["task_id"]
    get_task_response = get_task(task_id)

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]
    print(get_task_data)


def test_can_update_task():
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # update the task
    new_payload = {
        "user_id" : payload["user_id"],
        "task_id" : task_id,
        "content": "my updated content",
        "is_done" : True
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]


def test_can_list_tasks():
    # create n tasks
    N = 3
    payload = new_task_payload()
    for i in range(N):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    
    # list tasks and check that there are N items
    list_task_response = list_tasks(payload["user_id"])
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    print(data)
    tasks =  data["tasks"]
    print(len(tasks))
    assert len(tasks) == N
    # print(data)


def test_can_delete_task():
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # delete the task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    # check if task is not found
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404 