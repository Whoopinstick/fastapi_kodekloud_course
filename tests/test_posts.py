from typing import List
from app import schemas
from app.schemas import PostVote


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
    response_data = response.json()
    print(response.status_code)
    assert response.status_code == 404


def test_unauthorized_delete_post(client, test_posts):
    response = client.delete("/posts/1")
    # print(f"the response {response.json()}")
    # print(response.status_code)
    assert response.status_code == 401
