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
$ gunicorn backend.app:app --workers 4 --log-level debug --bind 127.0.0.1:8000
```

```
#check the operation of the backend server
$ curl -X POST http://127.0.0.1:8000/check_allergy \
-H "Content-Type: application/json" \
-d '{
    "dish_name": "Peanut Butter Sandwich"
}'
# {"check_egg":true,"check_potato":true,"check_raw_vegetable":true,"check_white_list_dishes":false,"safe_to_eat":true}

```
![alt text](image.png)