# Papermill container for running notebooks

Run a notebook in papermill.
Intended as entrypoint to a docker container

test:

    docker run -v /tmp/notebooks:/tmp/notebooks papermill-base  --notebook 'helloworld' --parameters '{"p1":"hello", "p2":"world"}'

push:

    docker push tfds/papermill-base:1.0
