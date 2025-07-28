# fastAPI sample project

# source - https://github.com/Sanjeev-Thiyagarajan/fastapi-course

# get and post requests with fastAPI

# fastapi.params Body

# schema validation with Pydantic
#### validate the data the client is sending back
#### see the pydantic_example.py file
#### Typing library for optional fields 

# CRUD best practices
## create, read, update, delete
## POST, GET, PUT/PATCH, DELETE
### PUT send all items to update the record
### PATCH send specific items to update
### Best practices - 
#### routes are plural, like - users, posts.  not user, post
#### POST should have a route like /posts
#### @app.post("/posts")
#### GET should have 2 routes for getting 1 or all like /posts/:id  or /posts
#### @app.get("/posts/{id}")  or @app.get("/posts")
#### PUT should have a route to update 1 item like /posts/:id
#### @app.put("/posts/{id}")
#### DELETE should have route to remove 1 item like /posts/:id
#### @app.delete("/posts/{id}")

# fastapi status and HTTPException to work with the response code

# psycopg - library for postgres
#### https://www.psycopg.org/psycopg3/docs/basic/index.html

# Sqlalchemy for Object Relational Mapping / ORM
# SQLModel is FastAPI's wrapper on top of Sqlalchemy

## Pydantic models vs SQLAlchemy models
### pydantic models are schema models that define the structure of a request/response
### sqlalchemy models are responsible for defining the columns in our postgres db
### sqlalchemy models are also used for the CRUD operations in the database

# password hashing
### https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#password-hashing
### using passlib[bcrypt] library

# authentication
## jwt token authentication
#### comprised of header, payload, and secret/signature
#### jwt tokens are not encrypted.  Don't put sensitive data in the payload

#### uv add pyjwt
#### import as 'jwt', not to be confused with another library just called 'jwt' that you can install
#### kodekloud project uses old jose library for jwt, fastapi docs use this new pyjwt instead

## protected routes
#### protect routes by adding a Depends() on oath2.get_current_user in the method signature
#### requests to that route will require a header with Authorization: Bearer <theToken>
##### test an expired token by changing the expiration time to 1 minute

### postman tips
##### to make testing with postman less annoying create an environment
##### you can setup variables to apply to all the operations, like baseUrl
##### you can also set an environment variable to grab a new access_token, and save that to be used in all routes


## foreign keys
#### SQLAlchemy model post class altered to have a user_id column and a foreign key back to users.id
#### SQLAlchemy won't add the new column and foreign key since the table already existed
#### A SQL Migration tool like Alembic would be required to do it programmatically
#### manual migration
```
alter table posts add column user_id INTEGER;

update posts set user_id = 14;

ALTER TABLE IF EXISTS public.posts
    ALTER COLUMN user_id SET NOT NULL;
	
ALTER TABLE IF EXISTS public.posts
    ADD CONSTRAINT posts_users_fk FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;
```

#### Other areas of the app need to be updated to accommodate the changes
#### optional, update schemas.post to have the PostResponse show the user_id in the response_model
#### the POST router for posts to set the user_id = the current logged in user_id


## SQLAlchemy table relationships
### add relationship to the model
### then, the object in the schema to be included in the response model
### the end result for example, is that you can see the user's email in the response instead of just the user_id

## Query parameters
### add a limit, skip / offset (pagination), search to the path 
### query parameters are added to a path operation after a question mark like - 
#### /posts?limit=10
### add limit to the method signature as a variable, set a default value
### update the db query to pass in the limit like
#### posts = db.query(models.Post).limit(limit).all()


## environment variables
### pydantic has a BaseSettings class that can be used for validation, typecasting, and using environment variables
###  uv add pydantic-settings
### importing this library also imports python-dotenv
### set in this project in config.py
### example: 
#### from pydantic_settings import BaseSettings
#### class Settings(BaseSettings): 
####     database_password: str "Can set a default if needed"
####     secret_key: str
#### then initialize and access with an instance like - settings = Settings()
####  blah = settings.secret_key
