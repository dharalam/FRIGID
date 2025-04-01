FROM python:3.12

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

WORKDIR /app

CMD ["python", "app_fasthtml.py"]