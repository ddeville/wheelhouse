import argparse
import json
import sys
import urllib.error
import urllib.request


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-v", "--version")
    args = parser.parse_args()

    url = get_sdist_url(args.name, args.version)

    if url is None:
        print(
            f"Couldn't find an sdist for {args.name}=={args.version} on pypi.org",
            file=sys.stderr,
        )
        sys.exit(1)

    print(url)


if __name__ == "__main__":
    main()
