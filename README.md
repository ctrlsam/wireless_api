# Wireless API

Harvests data via Zone Director, stored and served as a REST API
>API runs on port 5000

`[GET] /api/activities`
returns activities logged

**requires** `start_time` (unix timestamp) and `end_time` (unix timestamp)

**example**: 
`127.0.0.1:5000/api/activities?start_time=1596670000&end_time=1596675579`