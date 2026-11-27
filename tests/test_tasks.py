from fastapi import status

# Health Check
def test_health(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}

def test_create_and_get_task(client, auth_headers):
    # Create
    create_res = client.post(
        "/tasks/",
        json={"title": "Complete homework", "priority": "high"},
        headers=auth_headers,
    )

    assert create_res.status_code == status.HTTP_201_CREATED
    task_id = create_res.json()["id"]

    get_res = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_res.status_code == status.HTTP_200_OK
    assert get_res.json()["title"] == "Complete homework"

def test_update_task(client, auth_headers):
    create_res = client.post(
        "/tasks/",
        json={"title": "Complete homework", "priority": "high"},
        headers=auth_headers,
    )

    task_id = create_res.json()["id"]

    patch_res = client.patch(
        f"/tasks/{task_id}",
        json={"is_completed": True},
        headers=auth_headers,
    )
    assert patch_res.status_code == status.HTTP_200_OK
    data = patch_res.json()
    assert data["title"] == "Complete homework"
    assert data["is_completed"] == True
    assert data["completed_at"] is not None

def test_delete_task(client, auth_headers):
    create_res = client.post(
        "/tasks/",
        json={"title": "Complete homework", "priority": "high"},
        headers=auth_headers,
    )
    task_id = create_res.json()["id"]

    del_res = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert del_res.status_code == status.HTTP_204_NO_CONTENT

    get_res = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_res.status_code == status.HTTP_404_NOT_FOUND


