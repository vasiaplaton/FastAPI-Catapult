export $(cat .env | xargs) && \
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
uvicorn app.main:app --reload --port 8080
