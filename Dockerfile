
FROM python:3.10.11


WORKDIR /app


COPY . /app


RUN pip install -r /app/requirements.txt

ENV SLACK_CONNECT=""
ENV INDEX=""

RUN echo 'works'


CMD ["python", "main/run.py"]

