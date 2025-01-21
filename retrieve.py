import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Literal, cast

WORKFLOWS_DIR = Path(__file__).parent / ".github" / "workflows"

PURE_TEMPLATE = """name: $$FULLNAME$$
on:
  workflow_dispatch:
jobs:
  build_wheels:
    name: Build wheel
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: 3.11
      - run: ./scripts/build_python_wheel.sh $$SDIST_URL$$
      - uses: actions/upload-artifact@v4
        with:
          name: wheel
          path: ./wheelhouse/*.whl
"""

NATIVE_TEMPLATE = """name: $$FULLNAME$$
on:
  workflow_dispatch:
jobs:
  build_wheels:
    name: Build wheel on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-24.04, ubuntu-24.04-arm, macos-13, macos-14]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: 3.11
      - run: ./scripts/build_native_wheel.sh $$SDIST_URL$$
      - uses: actions/upload-artifact@v4
        with:
          name: wheel-${{ matrix.os }}
          path: ./wheelhouse/*.whl
"""


def get_sdist_url(package: str, version: str) -> str | None:
    url = f"https://pypi.org/pypi/{package}/{version}/json"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.getcode() == 404:
            return None
        raise

    for file_info in data["urls"]:
        if file_info["packagetype"] == "sdist":
            return file_info["url"]

    return None


def ask_package_type() -> Literal["pure", "native"]:
    while True:
        resp = (
            input(
                "Is the package pure Python or does it contain native code? [pure, native]: "
            )
            .strip()
            .lower()
        )
        if resp in ["pure", "native"]:
            return cast(Literal["pure", "native"], resp)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-v", "--version")
    args = parser.parse_args()

    fullname = f"{args.name}=={args.version}"
    url = get_sdist_url(args.name, args.version)

    if url is None:
        print(
            f"Couldn't find an sdist for {fullname} on pypi.org",
            file=sys.stderr,
        )
        sys.exit(1)

    match ask_package_type():
        case "pure":
            template = PURE_TEMPLATE
        case "native":
            template = NATIVE_TEMPLATE

    contents = template.replace("$$FULLNAME$$", fullname).replace("$$URL$$", url)
    with open(WORKFLOWS_DIR / f"{fullname}.yaml", "w") as f:
        f.write(contents)


if __name__ == "__main__":
    main()
