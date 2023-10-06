#!/bin/bash
echo Creating db...
python3 scripts/create_db.py

echo Running migrations...
alembic upgrade head

echo Seeding db...
python3 scripts/seed.py

echo Migrate task complete.
sleep 60
