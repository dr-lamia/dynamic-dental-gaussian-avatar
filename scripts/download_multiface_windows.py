"""Windows-friendly MultiFace subset downloader.

This replaces the original MultiFace downloader's Unix shell dependencies
(wget, md5sum, touch, rm) with Windows curl.exe + Python standard library.

Requires only:
  - Python 3.8+
  - requests/bs4 are NOT required by this script
  - curl.exe (included with current Windows 10/11)
"""
import argparse
import hashlib
import html.parser
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
from urllib.parse import urljoin


ROOT_URL = (
    "https://fb-baas-f32eacb9-8abb-11eb-b2b8-4857dd089e15."
    "s3.amazonaws.com/MugsyDataRelease/v0.0/identities/"
)


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def run_curl(url, output_path, insecure=False):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "curl.exe",
        "--fail",
        "--location",
        "--retry", "5",
        "--retry-delay", "2",
        "--output", str(output_path),
        url,
    ]
    if insecure:
        cmd.insert(1, "--insecure")
    print("Downloading:", url)
    subprocess.run(cmd, check=True)


def fetch_text(url, insecure=False):
    cmd = [
        "curl.exe",
        "--fail",
        "--location",
        "--retry", "5",
        "--silent",
        "--show-error",
        url,
    ]
    if insecure:
        cmd.insert(1, "--insecure")
    result = subprocess.run(cmd, check=True, capture_output=True)
    return result.stdout.decode("utf-8", errors="replace")


def md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def parse_checksum_file(path):
    checksums = {}
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            checksum = parts[0]
            filename = parts[-1].lstrip("*")
            checksums[filename] = checksum
    return checksums


def should_include(file_name, cfg):
    if file_name in {"CHECKSUM", "index.html"}:
        return True

    if "unwrapped_uv" in file_name and not cfg.get("texture", False):
        return False
    if "tracked_mesh" in file_name and not cfg.get("mesh", False):
        return False
    if "images" in file_name and not cfg.get("image", False):
        return False
    if "audio" in file_name and not cfg.get("audio", False):
        return False
    if "metadata" in file_name and not cfg.get("metadata", False):
        return False

    if "metadata" in file_name or "audio" in file_name:
        return True

    expressions = cfg.get("expression", [])
    return any(exp in file_name for exp in expressions)


def extract_tar(path, dest_dir):
    path = Path(path)
    print("Extracting:", path.name)
    with tarfile.open(path, "r:*") as tf:
        tf.extractall(dest_dir)


def download_entity(entity, cfg, dest, insecure=False, keep_tar=False):
    entity_root = urljoin(ROOT_URL, entity + "/")
    index_url = urljoin(entity_root, "index.html")
    html = fetch_text(index_url, insecure=insecure)

    parser = LinkParser()
    parser.feed(html)

    selected = []
    for href in parser.links:
        file_name = href.rstrip("/").split("/")[-1]
        if not file_name:
            continue
        if should_include(file_name, cfg):
            selected.append((file_name, urljoin(index_url, href)))

    if not selected:
        raise RuntimeError(
            "No files matched the config. Check entity/expression names."
        )

    entity_dest = Path(dest)
    entity_dest.mkdir(parents=True, exist_ok=True)

    checksum_path = None
    downloaded = []

    for file_name, url in selected:
        out = entity_dest / (entity + file_name)
        if out.exists() and out.stat().st_size > 0:
            print("Already exists, skipping:", out.name)
        else:
            run_curl(url, out, insecure=insecure)
        downloaded.append(out)
        if "CHECKSUM" in file_name:
            checksum_path = out

    checksums = {}
    if checksum_path and checksum_path.exists():
        checksums = parse_checksum_file(checksum_path)

    for path in downloaded:
        if path == checksum_path or path.suffix.lower() != ".tar":
            continue

        # Try exact tar filename and the server-side filename without entity prefix.
        candidate_names = [path.name, path.name[len(entity):] if path.name.startswith(entity) else path.name]
        expected = None
        for name in candidate_names:
            if name in checksums:
                expected = checksums[name]
                break

        if expected:
            actual = md5_file(path)
            if actual.lower() != expected.lower():
                raise RuntimeError(
                    "Checksum failed for {}\nexpected {}\nactual   {}".format(
                        path.name, expected, actual
                    )
                )
            print("Checksum OK:", path.name)

        extract_tar(path, entity_dest)
        if not keep_tar:
            path.unlink()
            print("Removed archive:", path.name)

    print("Completed entity:", entity)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dest", required=True)
    p.add_argument("--download_config", required=True)
    p.add_argument(
        "--insecure",
        action="store_true",
        help=(
            "Disable TLS certificate verification in curl. Use only if your "
            "institutional network intercepts HTTPS and the system trust store "
            "cannot be fixed."
        ),
    )
    p.add_argument("--keep-tar", action="store_true")
    args = p.parse_args()

    if shutil.which("curl.exe") is None:
        raise SystemExit("curl.exe was not found. It is included with current Windows 10/11.")

    with open(args.download_config, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    for entity in cfg["entity"]:
        download_entity(
            entity=entity,
            cfg=cfg,
            dest=args.dest,
            insecure=args.insecure,
            keep_tar=args.keep_tar,
        )


if __name__ == "__main__":
    main()
