FROM python:3.9.5

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]