POST Actor example
curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name":"Tina Poulsen","age":41,"gender":"Female"}'

POST Movie example
curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{"title":"Transformers 42","release_date":"2024-08-15","genre":"Action"}'

Delete Actor example
curl -X DELETE http://127.0.0.1:5000/actors/1

Delete Movie example
curl -X DELETE http://127.0.0.1:5000/movies/1

Patch Actor example
curl -X PATCH http://127.0.0.1:5000/actors/2 -H "Content-Type: application/json" -d '{"name": "Updated Actor Name", "age": 35, "gender": "Female"}'

Patch Movie example
curl -X PATCH http://127.0.0.1:5000/movies/2 -H "Content-Type: application/json" -d '{"title": "Updated Movie Title", "release_date": "2025-08-15", "genre": "Adventure"}'