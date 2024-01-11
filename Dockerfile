FROM python:3.10

RUN mkdir /app

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip

RUN python -m pip install -r /app/requirements.txt

COPY . /app/

WORKDIR /app

ENTRYPOINT ["python", "main.py"]