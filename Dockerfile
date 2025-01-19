FROM python:3.12-slim

WORKDIR /appчё

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./tests /app/tests

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]