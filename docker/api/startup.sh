#!/bin/bash
if [ "$ENV" == "prod" ]
then
    # for production
    alembic upgrade head && gunicorn --bind 0.0.0.0:$BACKEND_PORT -w 4 -k uvicorn.workers.UvicornWorker app.server:app
else
    dockerize -wait $DB_HOST -timeout 20s
    # for development
    alembic upgrade head && uvicorn app.server:app --host 0.0.0.0 --port $BACKEND_PORT --reload
fi
