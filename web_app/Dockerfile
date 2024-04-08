FROM python:3.10
ADD app.py .
ADD db.py .
ADD requirements.txt .
COPY templates ./templates
COPY static ./static
RUN apt update && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get install -y ffmpeg