#!/bin/sh

python3 -m http.server 5000 -d frontend &
HTTP_SERVER_PID=$! 
uvicorn backend.app_stream:app --workers 4 --log-level debug --host 127.0.0.1 --port 8000 &
UVICORN_PID=$!

trap "kill $HTTP_SERVER_PID $UVICORN_PID" INT

wait