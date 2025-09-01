import datetime
import uvicorn
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg
from psycopg.rows import dict_row


app = FastAPI()


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    created_at: Optional[datetime.datetime] = datetime.datetime.now()



@app.get("/")
@app.get("/ping")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_all_posts():
    # Open a cursor to perform database operations
    with psycopg.connect("host=localhost port=5432 dbname=kodekloud_fastapi user=postgres password=postgres",
                         row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(""" select * from posts; """)
            post = cur.fetchall()
    return {"data": post}


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int, response: Response):
    with psycopg.connect("host=localhost port=5432 dbname=kodekloud_fastapi user=postgres password=postgres",
                         row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            # use a tuple instead of just the post_id.  will return an error if not
            cur.execute(""" select * from posts where id = %s; """, (post_id,))

            post = cur.fetchone()

            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")

    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    with psycopg.connect("host=localhost port=5432 dbname=kodekloud_fastapi user=postgres password=postgres",
                         row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            # don't do this, it allows sql injection
            # cur.execute(f""" insert into posts (title, content, published) values ({post.title}, {post.content}, {post.published});""")

            # parameterize the input instead
            # use RETURNING so we can return the data that was just inserted
            # https://www.postgresql.org/docs/current/dml-returning.html
            cur.execute(""" insert into posts (title, content, published) values (%s, %s, %s) RETURNING *; """,
                        (post.title, post.content, post.published))

            new_post = cur.fetchone()

    return {"data": new_post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    with psycopg.connect("host=localhost port=5432 dbname=kodekloud_fastapi user=postgres password=postgres",
                         row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            # use a tuple instead of just the post_id.  will return an error if not
            cur.execute(""" select * from posts where id = %s; """, (post_id,))

            post = cur.fetchone()

            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
            else:
                cur.execute(""" delete from posts where id = %s; """, (post_id,))
                # don't send any data back or any message when something was deleted
                return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post_id: int, post: Post):
    with psycopg.connect("host=localhost port=5432 dbname=kodekloud_fastapi user=postgres password=postgres",
                         row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            # use a tuple instead of just the post_id.  will return an error if not
            cur.execute(""" update posts set title = %s, content = %s, published = %s where id = %s RETURNING *; """,
                        (post.title, post.content, post.published, post_id))

            post = cur.fetchone()

            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
            else:
                return {"data": post}




if __name__ == "__main__":
    uvicorn.run("005_psycopg_with_api_example:app", host="0.0.0.0", port=8000, reload=True)
