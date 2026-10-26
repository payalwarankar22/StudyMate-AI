
from unittest.mock import patch


def register_and_login_audio(client):
    password = "TestPassword@123"
    email = "audio_test@example.com"

    client.post(
        "/auth/register",
        json={
            "name": "Audio Test User",
            "email": email,
            "password": password,
        },
    )

    response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )

    assert response.status_code == 200
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_transcribe_audio_success(client):
    headers = register_and_login_audio(client)

    with patch(
        "app.api.v1.audio.TranscriptionService.transcribe_audio",
        return_value="This is a test transcript.",
    ):
        response = client.post(
            "/audio/transcribe",
            headers=headers,
            files={
                "file": (
                    "sample.wav",
                    b"fake audio content",
                    "audio/wav",
                )
            },
        )

    assert response.status_code == 200
    assert response.json()["filename"] == "sample.wav"
    assert response.json()["transcript"] == "This is a test transcript."


def test_transcribe_audio_rejects_unsupported_extension(client):
    headers = register_and_login_audio(client)

    response = client.post(
        "/audio/transcribe",
        headers=headers,
        files={
            "file": (
                "sample.txt",
                b"not audio",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported audio file format"


def test_transcribe_audio_requires_authentication(client):
    response = client.post(
        "/audio/transcribe",
        files={
            "file": (
                "sample.wav",
                b"fake audio content",
                "audio/wav",
            )
        },
    )

    assert response.status_code in (401, 403)
