
def register_and_login(client, email="notes_test@example.com"):
    password = "TestPassword@123"

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Notes Test User",
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_note(client):
    headers = register_and_login(client)

    response = client.post(
        "/notes/",
        headers=headers,
        json={"title": "Test Note", "content": "This is a test note."},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Note"
    assert response.json()["content"] == "This is a test note."
    assert "id" in response.json()


def test_get_my_notes(client):
    headers = register_and_login(client)

    client.post(
        "/notes/",
        headers=headers,
        json={"title": "My Note", "content": "My note content."},
    )

    response = client.get("/notes/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "My Note"


def test_get_note_by_id(client):
    headers = register_and_login(client)

    create_response = client.post(
        "/notes/",
        headers=headers,
        json={"title": "Find Me", "content": "Find this note."},
    )
    note_id = create_response.json()["id"]

    response = client.get(f"/notes/{note_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["title"] == "Find Me"


def test_update_note(client):
    headers = register_and_login(client)

    create_response = client.post(
        "/notes/",
        headers=headers,
        json={"title": "Old Title", "content": "Old content."},
    )
    note_id = create_response.json()["id"]

    response = client.put(
        f"/notes/{note_id}",
        headers=headers,
        json={"title": "Updated Title", "content": "Updated content."},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["content"] == "Updated content."


def test_delete_note(client):
    headers = register_and_login(client)

    create_response = client.post(
        "/notes/",
        headers=headers,
        json={"title": "Delete Me", "content": "Temporary note."},
    )
    note_id = create_response.json()["id"]

    response = client.delete(f"/notes/{note_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Note deleted successfully"

    get_response = client.get(f"/notes/{note_id}", headers=headers)
    assert get_response.status_code == 404


def test_note_endpoints_require_authentication(client):
    response = client.get("/notes/")
    assert response.status_code in (401, 403)


def test_user_cannot_access_another_users_note(client):
    user1_headers = register_and_login(client, "user1_notes@example.com")
    user2_headers = register_and_login(client, "user2_notes@example.com")

    create_response = client.post(
        "/notes/",
        headers=user1_headers,
        json={"title": "Private Note", "content": "Only user 1 should access this."},
    )
    note_id = create_response.json()["id"]

    response = client.get(f"/notes/{note_id}", headers=user2_headers)
    assert response.status_code == 404



def test_summarize_note(client, monkeypatch):
    headers = register_and_login(
        client, "summarize_test@example.com"
    )

    create_response = client.post(
        "/notes/",
        headers=headers,
        json={
            "title": "AI Study Note",
            "content": "Machine learning enables computers to learn from data.",
        },
    )
    assert create_response.status_code == 200

    note_id = create_response.json()["id"]

    def mock_summarize_note(self, note_content):
        assert note_content == (
            "Machine learning enables computers to learn from data."
        )
        return "Machine learning helps computers learn from data."

    monkeypatch.setattr(
        "app.api.v1.notes.SummarizationService.summarize_note",
        mock_summarize_note,
    )

    response = client.post(
        f"/notes/{note_id}/summarize",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == {
        "note_id": note_id,
        "summary": "Machine learning helps computers learn from data.",
    }
