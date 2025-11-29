#!/bin/sh

# 1. Wait for Postgres to start (Simple check)
# In production, we might use a robust wait-for-it script, 
# but this is usually fine for local docker-compose.

echo "Waiting for database..."
# (Optional sleep to give Postgres a second to wake up)
sleep 3

# 2. Apply Database Migrations
# This ensures the DB tables exist every time we spin up
echo "Applying database migrations..."
python manage.py migrate

# 3. Create Superuser (Optional automation - removes need to do it manually)
# You can remove this block if you prefer creating it manually
# echo "Creating superuser..."
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell

# 4. Start the Server
echo "Starting server..."
exec "$@"