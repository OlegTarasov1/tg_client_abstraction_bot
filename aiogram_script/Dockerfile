FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

RUN adduser user

USER user

CMD ["python3", "main.py"]