FROM python:3.10-bullseye

WORKDIR /app
COPY requirements-dev.txt requirements-dev.txt
RUN pip --no-cache-dir install --ignore-installed distlib -r requirements-dev.txt
RUN pip install gunicorn
RUN pip install uvicorn
COPY . .

EXPOSE 8080

CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", "wsgi:app", "-b", "0.0.0.0:8080"]
