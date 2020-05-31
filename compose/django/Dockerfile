FROM python:3

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./compose/django/entrypoint /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/django/start /start
RUN chmod +x /start

COPY . /app

WORKDIR /app

ENTRYPOINT ["/entrypoint"]