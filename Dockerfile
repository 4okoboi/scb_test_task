FROM python:3.12

RUN mkdir /backend

WORKDIR /backend

RUN pip install poetry

COPY pyproject.toml poetry.lock* /backend/

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . .

RUN chmod a+x docker/app.sh



# CMD ["gunicorn", "app.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
