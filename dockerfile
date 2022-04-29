FROM alpine:latest

RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev
RUN pip install --upgrade pip

WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install --ignore-installed distlib -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]
