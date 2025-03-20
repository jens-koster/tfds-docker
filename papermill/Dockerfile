ARG TFDS_VERSION=1.0
FROM tfds/spark-base:${TFDS_VERSION}

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN python -m ipykernel install --user

COPY book_runner.py /app/book_runner.py
# ENTRYPOINT []
ENTRYPOINT ["python", "/app/book_runner.py"]
