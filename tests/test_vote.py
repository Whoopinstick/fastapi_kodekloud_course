import pytest
from app.schemas import PostVote, Vote

@pytest.fixture()
def test_vote(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": 1, "dir": 1})
    assert response.status_code == 201


def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": 2, "dir": 1})
    assert response.json() == "Successfully added vote"
    assert response.status_code == 201


def test_vote_on_post_twice(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/vote/", json={"post_id": 1, "dir": 1})
    response_data = response.json()
    print(response.status_code)
    print(response_data)

    assert response.status_code == 409


def test_remove_vote_from_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/vote/", json={"post_id": 1, "dir": 0})
    response_data = response.json()
    print(response.status_code)
    print(response_data)

    assert  response.status_code == 201
    assert response_data == "Successfully removed vote"


def test_vote_on_post_not_exist(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": 1000, "dir": 1})
    assert response.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    response = client.post("/vote/", json={"post_id": 1, "dir": 1})
    assert response.status_code == 401
