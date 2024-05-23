FROM python:3.9
RUN mkdir /back
WORKDIR /back
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD alembic upgrade head && gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000