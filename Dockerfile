FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE server.settings

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD ./ /app

CMD ["python", "manage.py", "runasgiserver", "0.0.0.0:8000"]