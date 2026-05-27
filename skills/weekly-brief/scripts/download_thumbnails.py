#!/usr/bin/env python3
"""
Download, resize, and base64-encode thumbnail images for the weekly brief.

This script takes a list of thumbnail URLs, downloads each image, resizes it
to fit the report's containers (max 150x188px), and outputs a JSON file
mapping each URL to its base64 data URI.

Usage:
    python3 download_thumbnails.py \
        --urls "https://example.com/thumb1.jpg" "https://example.com/thumb2.jpg" \
        --output thumbnails.json

The output JSON looks like:
    {
        "https://example.com/thumb1.jpg": "data:image/jpeg;base64,/9j/4AAQ...",
        "https://example.com/thumb2.jpg": "data:image/jpeg;base64,/9j/4BBR...",
        "https://example.com/thumb3.jpg": null  // only if download failed TWICE
    }

Each resized image is ~5-15KB in base64 (vs 500KB-1MB for full resolution).
Total output for 15 images: ~75-225KB — safe for the sandbox.
"""

import argparse
import base64
import io
import json
import os
import subprocess
import sys
import time


def ensure_packages():
    """Install Pillow and requests if not already available."""
    for package in ["Pillow", "requests"]:
        try:
            if package == "Pillow":
                __import__("PIL")
            else:
                __import__(package)
        except ImportError:
            print(f"Installing {package}...", file=sys.stderr)
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "--break-system-packages"],
                check=True, capture_output=True
            )


def download_and_resize(url, max_width=150, max_height=188, quality=60):
    """
    Download an image from URL, resize it, and return a base64 data URI.

    Args:
        url: Image URL to download
        max_width: Maximum width in pixels (default 150)
        max_height: Maximum height in pixels (default 188)
        quality: JPEG quality 1-100 (default 60)

    Returns:
        str: base64 data URI like "data:image/jpeg;base64,..."
        None: if download failed

    Raises:
        Nothing — catches all exceptions and returns None on failure.
    """
    import requests
    from PIL import Image

    try:
        # Download with timeout
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (compatible; AdologyBot/1.0)"
        })
        resp.raise_for_status()

        # Open image
        img = Image.open(io.BytesIO(resp.content))

        # Convert to RGB if necessary (handles RGBA, palette, etc.)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        # Resize preserving aspect ratio
        img.thumbnail((max_width, max_height), Image.LANCZOS)

        # Encode as JPEG
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        b64_bytes = buffer.getvalue()

        # Check size — if over 30KB, reduce quality
        if len(b64_bytes) > 30 * 1024:
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=40, optimize=True)
            b64_bytes = buffer.getvalue()

        # If STILL over 30KB, reduce dimensions by 50%
        if len(b64_bytes) > 30 * 1024:
            img.thumbnail((max_width // 2, max_height // 2), Image.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=40, optimize=True)
            b64_bytes = buffer.getvalue()

        b64_str = base64.b64encode(b64_bytes).decode("ascii")
        data_uri = f"data:image/jpeg;base64,{b64_str}"

        return data_uri

    except Exception as e:
        print(f"  Failed: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Download and resize thumbnail images for the weekly brief"
    )
    parser.add_argument(
        "--urls",
        nargs="+",
        required=True,
        help="Thumbnail URLs to download"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output JSON file path"
    )

    args = parser.parse_args()

    # Install dependencies
    ensure_packages()

    results = {}
    succeeded = 0
    failed = 0

    for i, url in enumerate(args.urls, 1):
        if not url or url == "null" or url == "None" or url == "":
            print(f"  [{i}/{len(args.urls)}] Skipping empty URL", file=sys.stderr)
            results[url] = None
            failed += 1
            continue

        print(f"  [{i}/{len(args.urls)}] Downloading: {url[:80]}...", file=sys.stderr)

        # First attempt
        data_uri = download_and_resize(url)

        # Retry once on failure
        if data_uri is None:
            print(f"  [{i}/{len(args.urls)}] Retrying...", file=sys.stderr)
            time.sleep(1)
            data_uri = download_and_resize(url)

        if data_uri is not None:
            b64_size = len(data_uri) - len("data:image/jpeg;base64,")
            print(f"  [{i}/{len(args.urls)}] OK ({b64_size} bytes base64)", file=sys.stderr)
            succeeded += 1
        else:
            print(f"  [{i}/{len(args.urls)}] FAILED after retry", file=sys.stderr)
            failed += 1

        results[url] = data_uri

    # Write output JSON
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(args.output, "w") as f:
        json.dump(results, f)

    # Summary
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"THUMBNAIL DOWNLOAD COMPLETE", file=sys.stderr)
    print(f"  Succeeded: {succeeded}/{len(args.urls)}", file=sys.stderr)
    print(f"  Failed:    {failed}/{len(args.urls)}", file=sys.stderr)
    print(f"  Output:    {args.output}", file=sys.stderr)

    output_size = os.path.getsize(args.output)
    print(f"  File size: {output_size / 1024:.1f}KB", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    if failed > 0:
        print(f"\nWARNING: {failed} thumbnails failed to download.", file=sys.stderr)
        print(f"Check the JSON output — null values indicate failures.", file=sys.stderr)
        print(f"Try alternative thumbnail URLs for failed posts.", file=sys.stderr)


if __name__ == "__main__":
    main()
