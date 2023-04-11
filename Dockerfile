FROM python:3.10.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install vim \
    && apt-get -y install python3 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/docker-server
ADD . /srv/docker-server
WORKDIR /srv/docker-server

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY
ENV SERVER="NAVER"

COPY poetry.lock pyproject.toml /srv/docker-server/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN python manage.py makemigrations
RUN python manage.py migrate

# EXPOSE 8000
# CMD ["python", "manage.py", "runserver","0:8000"]
