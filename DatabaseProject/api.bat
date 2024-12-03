curl -X GET http://127.0.0.1:5000/list
curl -X POST http://127.0.0.1:5000/list -H "Content-Type: application/json" -d "{\"id\": 4, \"value\": \"Date\"}"
curl -X GET http://127.0.0.1:5000/list

