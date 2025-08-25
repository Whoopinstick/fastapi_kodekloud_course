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