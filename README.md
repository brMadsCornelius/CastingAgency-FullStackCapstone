# LIVE url: http://castingagency-fullstackcapstone.onrender.com

:computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer::computer:

:movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera::movie_camera:

# Casting Agency API

This project is the final project in the Fullstack Developer nanodegree capstone project!

This project uses the Flask framework to implement a Casting Agency service together with a Postgres database.

Backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

Frontend are yet to be developed for the future. To reach the deadline in the Udacity course it was not developed at due date.

## Getting Started

### Pre-requisites for local development 
Developers using this project should already have Python3 installed.

#### Backend

##### Step 1: Set up and Populate the Database

1. With Postgres running, create a `castingagency` database together with a test database (psql in this example):

```psql
CREATE DATABASE castingagency;
CREATE DATABASE castingagency_test;
```

**Step 2: Install dependencies and start the server**

It is recommended to use a virutal enviroment (venv) to comply with the pythonic standards.

From the main folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the setup.sh bash to setup all environment variables (change username/password to your own!):
```bash
source setup.sh
```

Or simply copy/paste the export commands to your terminal.

Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. Development has been done using WSL2.

Now simply start the flask application:

```bash
flask run
```

The application will run on `http://127.0.0.1:5000/`

#### Frontend

Not developed yet.

## Roles and permissions

The application has 3 roles. Underlying an overview can be seen showing all the associated permissions for each role:

- Casting Assistant: 
  - get:actors
  - get:movies

- Casting Director:
  - Same as Casting Assistant and
  - delete:actors
  - patch:actors
  - post:actors
  - patch:movies

- Executive Director:
  - Same as Casting Director and
  - post:movies
  - delete:movies


The tokens for each role can be seen in setup.sh (valid from 24h since 15:00 29/07/2024)

## API Reference

### Getting Started
- Authentication: This version of the application uses Auth0 where the token for each user can be seen in the setup.sh file.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable 
- 401: Authorization fail. A proper error message will be shown like "token not found", "token expired" etc.
- 403: Permission not found. The token used does not have the needed permissions to access this ressource.
- 

### Endpoints 

Overview:

- GET /
- GET /actors
- GET /movies
- POST /actors
- POST /movies
- DELETE /actors/<int>:id
- DELETE /movies/<int>:id

- PATCH /actors/<int>:id
- PATCH /movies/<int>:id
- 

#### GET /
- General:
    - Returns a static json. Can be used as a health check.
    - Needs no Auth.
- Sample: `curl http://127.0.0.1:5000/`

``` json
{
    "message": "Casting Agency Website - this page requires no authentication",
    "success": true
}
```

#### GET /actors

- General:
  - Returns a list of all actors
  - Requires auth as assistant, director or executive
- Sample: `curl http://127.0.0.1:5000/actors`

``` {
{
    "actors": [
        {
            "age": 35,
            "gender": "Female",
            "id": 2,
            "name": "Mads Andersen"
        },
        {
            "age": 58,
            "gender": "Male",
            "id": 3,
            "name": "Lars Poulsen"
        },
        {
            "age": 42,
            "gender": "Male",
            "id": 4,
            "name": "Test Person"
        }
    ],
    "success": true
}
```

#### GET /movies

- General:
  - Returns a list of all actors
  - Requires auth as assistant, director or executive
- `curl http://127.0.0.1:5000/movies`

```
{
    "movies": [
        {
            "genre": "Adventure",
            "id": 2,
            "release_date": "Fri, 15 Aug 2025 00:00:00 GMT",
            "title": "Updated Movie Title"
        },
        {
            "genre": "Fantasy",
            "id": 3,
            "release_date": "Fri, 15 Aug 2025 00:00:00 GMT",
            "title": "Harry Potter 8"
        },
        {
            "genre": "Action",
            "id": 4,
            "release_date": "Thu, 15 Aug 2024 00:00:00 GMT",
            "title": "Transformers 42"
        }
    ],
    "success": true
}
```

#### POST /actors

- General:
    - Creates a new actor using the submitted json. Returns the actor added and success flag.
    - Requires auth as director or executive
- `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name":"Tina Poulsen","age":41,"gender":"Female"}'`
```
{
    "age": 41,
    "gender": "Female",
    "name": "Tina Poulsen",
    "success": true
}
```
#### POST /movies

- General:
  - Creates a new movie using the submitted json. Returns the movieadded and success flag.
  - Requires auth as executive
- `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{"title":"Transformers 42","release_date":"2024-08-15","genre":"Action"}'`

```
{
    "genre": "Action",
    "id": 26,
    "release_date": "2024-08-15",
    "success": true,
    "title": "Transformers 42"
}
```

#### DELETE /actors/{actor_id}

- General:
  - Deletes an actor with a specific id in database.
  - Requires auth as director or executive
- Sample: `curl -X DELETE http://127.0.0.1:5000/actors/3`

``` {
{
    "deleted": 3,
    "success": true
}
```

- #### DELETE /movies/{movie_id}

  - General:
    - Deletes a movie with a specific id in database.
    - Requires auth as executive
  - Sample:  `curl -X DELETE http://127.0.0.1:5000/movies/2`

```
{
    "deleted": 2,
    "success": true
}
```

#### PATCH /actors/{actor_id}

- General:
  - Updates an actor with a specific id in database.
  - Requires auth as director or executive
- Sample: `curl -X PATCH http://127.0.0.1:5000/actors/2 -H "Content-Type: application/json" -d '{"name": "Updated Actor Name", "age": 35, "gender": "Female"}'`

``` {
{
    "actor": {
        "age": 35,
        "gender": "Female",
        "id": 2,
        "name": "Updated Actor Name"
    },
    "success": true
}
```

#### PATCH /movies/{movie_id}

- General:
  - Updates a movie with a specific id in database.
  - Requires auth as director or executive
- Sample: `curl -X PATCH http://127.0.0.1:5000/movies/3 -H "Content-Type: application/json" -d '{"title": "Updated Movie Title", "release_date": "2025-08-15", "genre": "Adventure"}`

``` {
{
    "movie": {
        "genre": "Adventure",
        "id": 3,
        "release_date": "Fri, 15 Aug 2025 00:00:00 GMT",
        "title": "Updated Movie Title"
    },
    "success": true
}
```

## Authors

Mads Cornelius Andersen

## Acknowledgements 
Udacity for creating a good full stack developer course :).