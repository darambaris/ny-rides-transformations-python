FROM python:3.13-slim

# Java for PySpark
RUN apt-get update && \
	apt-get install -y --no-install-recommends openjdk-21-jre-headless make && \
	arch="$(dpkg --print-architecture)" && \
	ln -sfn "/usr/lib/jvm/java-21-openjdk-${arch}" /usr/lib/jvm/default-java && \
	rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV SPARK_LOCAL_IP=127.0.0.1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Poetry

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./
COPY README.md ./
COPY ny_rides ./ny_rides

RUN poetry install --no-interaction --no-ansi

COPY . .

CMD ["bash"]
