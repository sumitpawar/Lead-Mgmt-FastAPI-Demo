bash
#!/bin/bash

cd app/

PORT=8000

echo "Starting FastAPI server on port $PORT..."
nohup uvicorn main:app --host 0.0.0.0 --port $PORT &
echo "FastAPI server started on port $PORT"