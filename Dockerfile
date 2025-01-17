FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV NAME=World

CMD ["streamlit", "run", "./dashboard/app.py"]