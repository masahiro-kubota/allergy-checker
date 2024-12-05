I have many allergies.
Check if I can eat that dish.

```
# frontend
$ python3 -m http.server 5000 -d frontend
```

```
# backend
# change base_url in script.js to local IP
$ cp .env.sample .env
$ uv sync
$ . .venv/bin/activate
$ uvicorn backend.app_stream:app --workers 4 --log-level debug --host 127.0.0.1 --port 8000
```

```
#check the operation of the backend server
$ curl "http://127.0.0.1:8000/check_allergy_stream?dish_name=%E3%81%8A%E3%81%A7%EF%BD%8E"


```
![説明gif](images/sample.gif)