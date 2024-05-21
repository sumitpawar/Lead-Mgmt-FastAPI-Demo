#!/bin/bash

cd app/

PORT=8000

echo "Stopping FastAPI server on port $PORT..."
PID=$(lsof -t -i:$PORT)
if [ -z "$PID" ]; then
  echo "No FastAPI server found running on port $PORT"
else
  kill $PID
  echo "FastAPI server stopped on port $PORT"
fi