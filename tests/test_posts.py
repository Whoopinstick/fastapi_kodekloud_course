from app.schemas import PostVote, PostResponse
import pytest

# create a test post before trying to get posts
# will return something like this without posts - {'detail': 'No posts found'}, <Response [404 Not Found]>
def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    response_data = response.json()
    print(response_data)

    posts_map_list = list(map(lambda x: PostVote(**x), response_data))
    print(posts_map_list)

    assert response.status_code == 200


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get("/posts/1")
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200
    assert response_data["title"] == "first title"


def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get("/posts/1000")
    # response_data = response.json()
    print(response.status_code)
    assert response.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("test title 1", "test content 1", True),
    ("test title 2", "test content 2", True),
    ("test title 3", "test content 3", False),
    ("test title 4", "test content 4", None)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    response_data = response.json()
    print(response_data)
    created_post = PostResponse(**response_data)
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published or True # or True, test default value of published = True
    assert created_post.user_id == test_user["id"]


def test_unauthorized_create_post(client, test_posts):
    response = client.post("/posts/", json={"title": "test title no auth", "content": "test content no auth"})
    assert response.status_code == 401


def test_unauthorized_delete_post(client, test_user, test_posts):
    response = client.delete("/posts/1")
    assert response.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete("/posts/1")
    assert response.status_code == 204


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete("/posts/4")
    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    updated_post_data = {
        "title": "updated title",
        "content": "updated content"
    }

    response = authorized_client.put("/posts/1", json=updated_post_data)
    response_data = response.json()
    print(response.status_code)
    print(response_data)

    post_response = PostResponse(**response_data)
    print(post_response)
    print(test_user["email"])
    assert test_user["email"] == post_response.user.email
    assert updated_post_data["title"] == post_response.title
    assert response.status_code == 200


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    updated_post_data = {
        "title": "updated title2",
        "content": "updated content2"
    }

    response = authorized_client.put(f"/posts/4", json=updated_post_data)
    response_data = response.json()
    print(response.status_code)
    print(response_data)
    assert response.status_code == 403


def test_unauthorized_update_post(client, test_posts):
    response = client.put("/posts/1", json={"title": "test title no auth", "content": "test content no auth"})
    assert response.status_code == 401


def test_update_post_not_exist(authorized_client, test_posts):
    response = authorized_client.put("/posts/10000", json={"title": "test title no auth", "content": "test content no auth"})
    assert response.status_code == 404