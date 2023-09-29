FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/
RUN pip3 install poetry
COPY poetry.lock pyproject.toml /usr/src/
RUN poetry install
CMD ["poetry", "run","python", "manage.py", "spectacular", "--color", "--file", "schema.yml"]
CMD ["poetry", "run","python", "manage.py", "runserver", "0.0.0.0:8000"]