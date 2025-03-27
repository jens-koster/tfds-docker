"""
Run a notebook in papermill.
Intended as entrypoint to a docker container
some useful commands, full documentation in the readme.
python3 book_runner.py --notebook helloworld --parameters '{"p1":"hello", "p2":"world"}'
docker compose run book-runner --notebook 'helloworld' --parameters '{"p1":"hello", "p2":"world"}'
docker compose run --remove-orphans --rm -it --entrypoint /bin/bash book-runner

"""

import argparse
import datetime as dt
import json
import os

import boto3
import papermill as pm
import requests


# we temorarily use the scrape keys function to get the keys for s3 ninja

import requests


def convert_config(items):
    return {item["name"]: item["value"] for item in items}


def get_s3_config():

    tfds_config_url = os.environ.get("TFDS_CONFIG_URL")
    print(f"using tsdf-config: {tfds_config_url}")
    if not tfds_config_url:
        raise EnvironmentError("Environment variable TFDS_CONFIG_URL is not set")

    response = requests.get(f"{tfds_config_url}/s3")
    return convert_config(response.json()["items"])


def execute_notebook(notebook, parameters):
    cfg = get_s3_config()

    s3_client = boto3.client(
        service_name="s3",
        aws_access_key_id=cfg["access_key"],
        aws_secret_access_key=cfg["secret_key"],
        endpoint_url=cfg["url"],
    )

    tmp_dir = f"/tmp/book_runner/{notebook}"
    os.makedirs(tmp_dir, exist_ok=True)

    input_bucket = "notebooks"
    input_object_name = f"{notebook}.ipynb"
    input_local_file = f"{tmp_dir}/{notebook}.ipynb"

    output_bucket = "output-notebooks"
    output_local_file = (
        f"{tmp_dir}/{notebook}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.ipynb"
    )
    output_prefix = f"{notebook}/"
    output_object_name = (
        f"{notebook}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.ipynb"
    )

    print(f"Downloading {input_bucket}, {input_object_name} to {input_local_file}")
    s3_client.download_file(input_bucket, input_object_name, input_local_file)

    print(f"Executing papermill: {input_local_file} -> {output_local_file}")
    pm.execute_notebook(
        input_path=input_local_file,
        output_path=output_local_file,
        parameters=parameters,
    )

    print(
        f"Uploading {output_local_file} to bucket {output_bucket} as {output_prefix}{output_object_name}"
    )
    with open(output_local_file, "rb") as f:
        s3_client.upload_fileobj(
            f, output_bucket, f"{output_prefix}{output_object_name}"
        )

    print("Notebook executed")


def get_endpoint():
    endpoint = os.environ.get("S3NINJA_ENDPOINT")
    if endpoint is None:
        endpoint = "http://127.0.0.1:8004"
    return endpoint


def main():

    parser = argparse.ArgumentParser(
        description="Run a Jupyter notebook with papermill."
    )

    # notebook
    parser.add_argument(
        "--notebook",
        type=str,
        required=True,
        help="Notebok filename excluding the .ipynb extension",
    )
    # parameters
    parser.add_argument(
        "--parameters",
        type=str,
        required=True,
        help=(
            "JSON string of parameters to pass to the notebook, "
            "use doublequotes on value and key"
        ),
    )

    args = parser.parse_args()
    # Parse the parameters
    notebook = args.notebook
    print(f"Running notebook {notebook}")

    try:
        print(f"Parameters: {args.parameters}")
        parameters = json.loads(args.parameters)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON string for parameters")

    execute_notebook(notbook=notebook, parameters=parameters)


if False:
    os.environ["TFDS_CONFIG_URL"] = "http://127.0.0.1:8005/api/configs"
    execute_notebook(notebook="helloworld", parameters={"p1": "hello", "p2": "world"})
