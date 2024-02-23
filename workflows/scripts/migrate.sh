#!/bin/sh
echo Creating db...
python3 scripts/create_db.py

echo Running migrations...
alembic upgrade head

echo Migrate task complete.
sleep 30