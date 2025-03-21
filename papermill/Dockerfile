ARG TFDS_VERSION=1.0
FROM tfds/spark-base:${TFDS_VERSION}

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN python -m ipykernel install --user
ENV S3NINJA_ENDPOINT=http://s3-ninja:8004
COPY book_runner.py /app/book_runner.py
# ENTRYPOINT []
ENTRYPOINT ["python", "/app/book_runner.py"]
