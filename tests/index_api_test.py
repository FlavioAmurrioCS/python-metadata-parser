# flake8: noqa: S108
import json
import os

import httpx
import pytest
from pydantic import TypeAdapter

from python_metadata_parser.index_api import GetDistributionsForProjectResponse
from python_metadata_parser.index_api import ListAllProjectsResponse

# Create an adapter for the TypedDict
adapter = TypeAdapter(GetDistributionsForProjectResponse)


def get_test_data(package: str) -> tuple[GetDistributionsForProjectResponse, str]:
    os.makedirs("/tmp/test_files", exist_ok=True)
    file_path_json = f"/tmp/test_files/{package}.json"
    if not os.path.exists(file_path_json):
        response = httpx.get(
            f"https://pypi.org/simple/{package}/",
            headers={"Accept": "application/vnd.pypi.simple.v1+json"},
        )
        with open(file_path_json, "w") as f:
            f.write(response.text)
    file_path_html = f"/tmp/test_files/{package}.html"
    if not os.path.exists(file_path_html):
        response = httpx.get(
            f"https://pypi.org/simple/{package}/",
            headers={"Accept": "application/vnd.pypi.simple.v1+html"},
        )
        with open(file_path_html, "w") as f:
            f.write(response.text)

    with open(file_path_json) as f:
        json_data = json.load(f)
    with open(file_path_html) as f:
        return json_data, f.read()


packages = [
    "virtualenv",
    "pip",
    # "numpy",
    "requests",
    "beautifulsoup4",
    "pandas",
    "flask",
    "scipy",
    "lambda-dev-server",
    "env-http-auth",
]


@pytest.mark.parametrize("package", packages)
def test_types(package: str) -> None:
    json_data, _text = get_test_data(package)
    adapter.validate_python(json_data)

def get_all_packages_data() -> ListAllProjectsResponse:
    os.makedirs("/tmp/test_files", exist_ok=True)
    file_path_json = "/tmp/test_files/all_packages.json"
    if not os.path.exists(file_path_json):
        response = httpx.get(
            "https://pypi.org/simple/",
            headers={"Accept": "application/vnd.pypi.simple.v1+json"},
        )
        with open(file_path_json, "w") as f:
            f.write(response.text)

    with open(file_path_json) as f:
        json_data:ListAllProjectsResponse = json.load(f)
        return json_data

def test_all_packages_types() -> None:
    json_data = get_all_packages_data()
    TypeAdapter(ListAllProjectsResponse).validate_python(json_data)
