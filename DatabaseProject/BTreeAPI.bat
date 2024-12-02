curl -X POST http://127.0.0.1:5000/insert -H "Content-Type: application/json" -d "{\"time\": \"2024-12-02T12:00:00\", \"value\": 25}"
curl -X POST http://127.0.0.1:5000/insert -H "Content-Type: application/json" -d "{\"time\": \"2024-12-02T12:05:00\", \"value\": 30}"
curl -X POST http://127.0.0.1:5000/insert -H "Content-Type: application/json" -d "{\"time\": \"2024-12-02T12:10:00\", \"value\": 35}"
curl "http://127.0.0.1:5000/query?start=2024-12-02T12:00:00&end=2024-12-02T12:15:00"
