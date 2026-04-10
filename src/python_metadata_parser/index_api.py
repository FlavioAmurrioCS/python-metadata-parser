from __future__ import annotations

from typing import Literal
from typing import TypedDict

_ListAllProjectsResponseMeta = TypedDict(
    "_ListAllProjectsResponseMeta", {"_last-serial": int, "api-version": str}
)
_ListAllProjectsResponseProject = TypedDict(
    "_ListAllProjectsResponseProject", {"_last-serial": int, "name": str}
)

class ListAllProjectsResponse(TypedDict):
    meta: _ListAllProjectsResponseMeta
    projects: list[_ListAllProjectsResponseProject]


class GetDistributionsForProjectResponseProjectStatus(TypedDict):
    status: str


GetDistributionsForProjectResponseHash = dict[Literal["sha256"], str]
_OptionalHash = GetDistributionsForProjectResponseHash | Literal[False]
GetDistributionsForProjectResponseFile = TypedDict(
    "GetDistributionsForProjectResponseFile",
    {
        "core-metadata": _OptionalHash,
        "data-dist-info-metadata": _OptionalHash,
        "filename": str,
        "hashes": GetDistributionsForProjectResponseHash,
        "provenance": str | None,
        "requires-python": str | None,
        "size": int,
        "upload-time": str,
        "url": str,
        "yanked": bool | str,
    },
)
GetDistributionsForProjectResponse = TypedDict(
    "GetDistributionsForProjectResponse",
    {
        "alternate-locations": list[str],
        "files": list[GetDistributionsForProjectResponseFile],
        "meta": _ListAllProjectsResponseMeta,
        "name": str,
        "project-status": GetDistributionsForProjectResponseProjectStatus,
        "versions": list[str],
    },
)


# @dataclass
# class Links:
#     attrs: dict[str, str | None]
#     text: str = ""


# class LinkParser(HTMLParser):
#     def __init__(self) -> None:
#         super().__init__()
#         self.links: list[Links] = []
#         self.meta: dict[str, str] = {}
#         self.title: str = ""
#         self.serial: int = 0
#         self._in_title: bool = False

#     def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
#         if tag == "a":
#             self.links.append(Links(attrs=dict(attrs)))
#         elif tag == "meta":
#             dct = dict(attrs)
#             self.meta[dct.get("name") or ""] = dct.get("content") or ""
#         elif tag == "title":
#             self._in_title = True

#     def handle_data(self, data: str) -> None:
#         if self._in_title:
#             self.title += data
#         if self.links and data.strip():
#             self.links[-1].text = data.strip()

#     def handle_endtag(self, tag: str) -> None:
#         if tag == "title":
#             self._in_title = False
#             self.title = self.title.strip()

#     def handle_comment(self, data: str) -> None:
#         data = data.strip()
#         if data.startswith("SERIAL "):
#             with contextlib.suppress(IndexError, ValueError):
#                 self.serial = int(data.split()[1])


# def test_parser() -> None:
#     if os.path.exists("./test_results"):
#         import shutil

#         shutil.rmtree("./test_results")
#     packages = [
#         "virtualenv",
#         "pip",
#         # "numpy",
#         "requests",
#         "beautifulsoup4",
#         "pandas",
#         "flask",
#         "scipy",
#         "lambda-dev-server",
#         "env-http-auth",
#     ]

#     for package in packages:
#         json_data, text = get_test_data(package)
#         parser = LinkParser()
#         parser.feed(text)
#         parsed = html_to_dist(parser)

#         for f in json_data["files"]:
#             f.pop("upload-time", None)
#             f.pop("size", None)
#         for f in parsed["files"]:
#             f.pop("upload-time", None)
#             f.pop("size", None)
#         json_data.pop("versions", None)
#         parsed.pop("versions", None)

#         comparison = json.dumps(json_data, sort_keys=True) == json.dumps(parsed, sort_keys=True)

#         if not comparison:
#             os.makedirs("./test_results", exist_ok=True)
#             with open(f"./test_results/{package}.original.json", "w") as f:
#                 json.dump(json_data, f, sort_keys=True, indent=2)
#             with open(f"./test_results/{package}.parsed.json", "w") as f:
#                 json.dump(parsed, f, sort_keys=True, indent=2)
#             print(
#                 f"Comparison failed for ./test_results/{package}.original.json and ./test_results/{package}.parsed.json"
#             )


# def html_to_dist(
#     link_parser: LinkParser,
# ) -> GetDistributionsForProjectResponse:
#     title = link_parser.title
#     name = title.replace("Links for ", "") if title else ""

#     api_version = link_parser.meta.get("pypi:repository-version", "1.0")
#     project_status = link_parser.meta.get("pypi:project-status", "unknown")

#     serial = link_parser.serial

#     files = [extract_distribution_metadata(link) for link in link_parser.links]

#     versions: set[str] = set()
#     for link in link_parser.links:
#         version = get_version(link.text)
#         if version:
#             versions.add(version)

#     return {
#         "alternate-locations": [],
#         "files": files,
#         "meta": {
#             "_last-serial": serial,
#             "api-version": api_version,
#         },
#         "name": name,
#         "project-status": {"status": project_status},
#         "versions": sorted(versions),
#     }


# def extract_distribution_metadata(link: Links) -> GetDistributionsForProjectResponseFile:
#     href = link.attrs.get("href") or ""
#     url, _, hash_fragment = href.partition("#")
#     hash_value: _OptionalHash = False
#     if hash_fragment.startswith("sha256="):
#         hash_value = {"sha256": hash_fragment[7:]}

#     data_dist_info = link.attrs.get("data-dist-info-metadata", None)
#     data_dist_info_value: _OptionalHash = False
#     if data_dist_info:
#         data_dist_info = data_dist_info.removeprefix("sha256=")
#         data_dist_info_value = {"sha256": data_dist_info}

#     core_metadata = link.attrs.get("data-core-metadata", None)
#     core_metadata_value: _OptionalHash = False
#     if core_metadata:
#         core_metadata = core_metadata.removeprefix("sha256=")
#         core_metadata_value = {"sha256": core_metadata}

#     requires_python = link.attrs.get("data-requires-python", None)
#     if requires_python:
#         requires_python = unescape(requires_python)

#     yanked_value = link.attrs.get("data-yanked", None)
#     yanked: bool | str = False
#     if yanked_value is not None:
#         yanked = yanked_value or True

#     provenance = link.attrs.get("data-provenance", None)

#     return {
#         "filename": link.text,
#         "url": url,
#         "hashes": hash_value,
#         "requires-python": requires_python,
#         "size": 0,
#         "upload-time": "",
#         "yanked": yanked,
#         "data-dist-info-metadata": data_dist_info_value,
#         "core-metadata": core_metadata_value,
#         "provenance": provenance,
#     }


# def get_version(filename: str) -> str | None:
#     if filename.endswith(".whl"):
#         parts = filename.split("-")
#         return parts[1] if len(parts) >= 2 and parts[-1] == ".whl" else None

#     base = filename
#     for ext in (".tar.gz", ".tgz", ".zip", ".exe"):
#         if base.endswith(ext):
#             base = base[: -len(ext)]
#             break
#     parts = base.split("-")
#     return parts[1] if len(parts) >= 2 else None
