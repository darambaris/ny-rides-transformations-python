FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

CMD ["bash"]