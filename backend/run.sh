#!/usr/bin/env bash
# exit on error
set -o errexit

# Get the PORT from environment variable or default to 8000
PORT="${PORT:-8000}"

# Start Gunicorn with the correct host and port binding
exec gunicorn aurene_backend.wsgi:application --bind 0.0.0.0:$PORT
