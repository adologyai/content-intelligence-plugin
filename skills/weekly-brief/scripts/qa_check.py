#!/usr/bin/env python3
"""
QA validation script for HTML files before PDF assembly.

This script validates HTML files for the competitive intelligence PDF to ensure
all content is properly generated and no placeholders remain.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any


# Expected image counts per page
# P1: 6 scoreboard + 1 spotlight = 7 thumbnails (resized base64 via download_thumbnails.py)
# P2: No thumbnails
# P3: 5 trend cards + 3 coaching cards = 8 thumbnails (resized base64 via download_thumbnails.py)
EXPECTED_IMAGES = {
    "P1": 7,
    "P2": 0,
    "P3": 8,
}

# Base64 image pattern
BASE64_IMAGE_PATTERN = re.compile(
    r'<img[^>]*src="data:image/[^;]+;base64,([^"]+)"[^>]*>'
)

# URL pattern
URL_PATTERN = re.compile(r'<a[^>]*href="([^"]*)"[^>]*>')

# Placeholder pattern
PLACEHOLDER_PATTERN = re.compile(r'{{|}}')

# Engagement metric patterns
# Match either:
#   - a number with K/M suffix (optionally with a decimal): 12K, 1.2M, 800K
#   - a number with at least one thousands separator: 1,234 or 12,345,678
# Plain integers (font sizes like "11pt", years like "2024", structural digits
# like <th>1</th>) are intentionally NOT matched.
ENGAGEMENT_PATTERN = re.compile(r'\b\d+(?:\.\d+)?[KM]\b|\b\d{1,3}(?:,\d{3})+\b')

# Page CSS pattern
PAGE_CSS_PATTERN = re.compile(r'@page\s*{\s*size:\s*8\.5in\s+11in')

# Page-key extractor — anchored to a `^P[1-3]_` prefix so files named
# `Pickle1.html` or `Project1.html` do NOT inherit P1's image/size budget.
PAGE_KEY_RE = re.compile(r'^(P[123])_', re.IGNORECASE)


def page_key_from(filename: str) -> str | None:
    """Return 'P1' / 'P2' / 'P3' if `filename` starts with that prefix + '_', else None."""
    basename = os.path.basename(filename)
    match = PAGE_KEY_RE.match(basename)
    return match.group(1).upper() if match else None


class QAValidator:
    """Validator for HTML files."""

    def __init__(self, working_dir: str):
        """Initialize validator with working directory."""
        self.working_dir = working_dir
        self.results = {
            "files": {},
            "overall_status": "PASS",
            "issue_count": 0,
        }

    def check_placeholders(self, html_content: str, filename: str) -> Dict[str, Any]:
        """
        Check for leftover template placeholders.

        Returns:
            Dict with 'status' (PASS/FAIL), 'issues' (list of found placeholders)
        """
        issues = []
        lines = html_content.split("\n")

        for line_num, line in enumerate(lines, 1):
            matches = PLACEHOLDER_PATTERN.finditer(line)
            for match in matches:
                context_start = max(0, match.start() - 30)
                context_end = min(len(line), match.end() + 30)
                context = line[context_start:context_end].strip()
                issues.append(
                    {
                        "line": line_num,
                        "match": match.group(),
                        "context": context,
                    }
                )

        return {
            "status": "FAIL" if issues else "PASS",
            "count": len(issues),
            "issues": issues,
        }

    def check_images(self, html_content: str, filename: str) -> Dict[str, Any]:
        """
        Check for real base64 images (not tiny placeholders).

        Returns:
            Dict with 'status' (PASS/WARN/FAIL), image count, and validation details
        """
        # Extract page number from filename (anchored, not substring)
        page_key = page_key_from(filename)

        expected_count = EXPECTED_IMAGES.get(page_key, -1)

        matches = BASE64_IMAGE_PATTERN.findall(html_content)
        found_count = len(matches)

        issues = []
        tiny_images = 0

        for match in matches:
            if len(match) < 100:
                tiny_images += 1
                issues.append(
                    {
                        "type": "tiny_placeholder",
                        "base64_length": len(match),
                        "context": f"Base64 string is only {len(match)} chars (expected 100+)",
                    }
                )

        status = "PASS"
        if tiny_images > 0:
            status = "WARN"

        # SKILL.md declares "Thumbnails are MANDATORY". A page that's missing
        # any expected image is a FAIL, not a WARN. Extra images (found_count
        # > expected_count) stay at WARN — it's a soft mismatch, not a contract
        # violation.
        if expected_count > 0 and found_count < expected_count:
            status = "FAIL"
            issues.append(
                {
                    "type": "count_mismatch",
                    "expected": expected_count,
                    "found": found_count,
                }
            )
        elif expected_count >= 0 and found_count != expected_count:
            status = "WARN" if status != "FAIL" else status
            issues.append(
                {
                    "type": "count_mismatch",
                    "expected": expected_count,
                    "found": found_count,
                }
            )

        return {
            "status": status,
            "found_count": found_count,
            "expected_count": expected_count,
            "tiny_images": tiny_images,
            "issues": issues,
        }

    def check_urls(self, html_content: str, filename: str) -> Dict[str, Any]:
        """
        Check that URLs are real (not # or empty).

        Returns:
            Dict with 'status', URL counts, and issues
        """
        matches = URL_PATTERN.findall(html_content)
        total_links = len(matches)

        real_links = []
        invalid_links = []

        for href in matches:
            if href.startswith("http://") or href.startswith("https://"):
                real_links.append(href)
            elif href == "#" or href == "":
                invalid_links.append(href if href else "(empty)")
            else:
                # Relative or other URLs - treat as warnings
                invalid_links.append(href)

        status = "PASS"
        if invalid_links:
            status = "WARN"

        return {
            "status": status,
            "total_links": total_links,
            "real_links": len(real_links),
            "invalid_links": len(invalid_links),
            "invalid_list": invalid_links[:5],  # Show first 5
        }

    def check_engagement_metrics(self, html_content: str, filename: str) -> Dict[str, Any]:
        """
        Check for presence of engagement numbers.

        Returns:
            Dict with 'status' and whether metrics are found
        """
        matches = ENGAGEMENT_PATTERN.findall(html_content)

        status = "PASS"
        if len(matches) < 5:  # Expect at least some metrics
            status = "WARN"

        return {
            "status": status,
            "metrics_found": len(matches),
            "sample_metrics": matches[:5] if matches else [],
        }

    def check_page_css(self, html_content: str, filename: str) -> Dict[str, Any]:
        """
        Check for @page CSS declaration.

        Returns:
            Dict with 'status' and CSS details
        """
        has_page_css = bool(PAGE_CSS_PATTERN.search(html_content))

        return {
            "status": "PASS" if has_page_css else "FAIL",
            "has_page_css": has_page_css,
        }

    def check_file_size(self, html_content: str, filename: str) -> Dict[str, Any]:
        """
        Check that the HTML file is within size budget.
        P1: max 100KB, P2/P3: max 50KB.
        Files over budget likely have embedded base64 images.
        """
        size_bytes = len(html_content.encode('utf-8'))
        size_kb = size_bytes / 1024

        page_key = page_key_from(filename)
        if page_key == "P1":
            max_kb = 200  # Has 7 resized thumbnails (~5-15KB each)
        elif page_key == "P2":
            max_kb = 50   # No images
        elif page_key == "P3":
            max_kb = 200  # Has 8 resized thumbnails (~5-15KB each)
        else:
            max_kb = 200

        over_budget = size_kb > max_kb
        status = "FAIL" if over_budget else "PASS"

        result = {
            "status": status,
            "size_kb": round(size_kb, 1),
            "max_kb": max_kb,
        }
        if over_budget:
            result["issue"] = (
                f"File is {size_kb:.0f}KB (max {max_kb}KB). "
                "This likely means base64 images were embedded. "
                "Remove them and use CSS placeholders instead."
            )
        return result

    def validate_file(self, filename: str) -> Dict[str, Any]:
        """
        Run all validation checks on an HTML file.

        Returns:
            Dict with all check results
        """
        file_path = os.path.join(self.working_dir, filename)

        # Read HTML file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            return {
                "file": filename,
                "error": f"File not found: {file_path}",
                "status": "FAIL",
            }
        except IOError as e:
            return {
                "file": filename,
                "error": f"Error reading file: {e}",
                "status": "FAIL",
            }

        # Run all checks
        results = {
            "file": filename,
            "file_size": len(html_content),
            "checks": {
                "file_size_budget": self.check_file_size(html_content, filename),
                "placeholders": self.check_placeholders(html_content, filename),
                "images": self.check_images(html_content, filename),
                "urls": self.check_urls(html_content, filename),
                "engagement": self.check_engagement_metrics(html_content, filename),
                "page_css": self.check_page_css(html_content, filename),
            },
        }

        # Determine overall file status
        critical_issues = [
            results["checks"]["placeholders"]["status"] == "FAIL",
            results["checks"]["page_css"]["status"] == "FAIL",
            results["checks"]["file_size_budget"]["status"] == "FAIL",
            results["checks"]["images"]["status"] == "FAIL",
        ]

        if any(critical_issues):
            results["status"] = "FAIL"
        else:
            warnings = [
                check["status"] == "WARN"
                for check in results["checks"].values()
            ]
            results["status"] = "WARN" if any(warnings) else "PASS"

        return results

    def validate_all(self, filenames: List[str]) -> None:
        """Validate all files and update results."""
        for filename in filenames:
            result = self.validate_file(filename)
            self.results["files"][filename] = result

            if result.get("status") == "FAIL":
                self.results["overall_status"] = "FAIL"
            elif (
                result.get("status") == "WARN"
                and self.results["overall_status"] != "FAIL"
            ):
                self.results["overall_status"] = "WARN"

    def print_report(self) -> None:
        """Print a formatted validation report."""
        print("\n" + "=" * 70)
        print("HTML QA VALIDATION REPORT")
        print("=" * 70 + "\n")

        for filename, result in self.results["files"].items():
            print(f"File: {filename}")
            print(f"Status: {result.get('status', 'N/A')}")

            if "error" in result:
                print(f"Error: {result['error']}\n")
                continue

            print(f"Size: {result['file_size']} bytes\n")

            # File size budget check
            sz_check = result["checks"]["file_size_budget"]
            print(f"  File Size Budget: {sz_check['status']}", end="")
            print(f" ({sz_check['size_kb']}KB / {sz_check['max_kb']}KB max)")
            if sz_check.get("issue"):
                print(f"    {sz_check['issue']}")

            # Placeholders check
            ph_check = result["checks"]["placeholders"]
            print(f"  Placeholders: {ph_check['status']}", end="")
            if ph_check["issues"]:
                print(f" ({ph_check['count']} found)")
                for issue in ph_check["issues"][:3]:
                    print(
                        f"    Line {issue['line']}: {issue['match']}"
                        f" in '{issue['context'][:40]}...'"
                    )
            else:
                print(" (clean)")

            # Images check
            img_check = result["checks"]["images"]
            print(f"  Images: {img_check['status']}", end="")
            if img_check["expected_count"] >= 0:
                print(f" (found {img_check['found_count']}, expected {img_check['expected_count']})")
            else:
                print(f" (found {img_check['found_count']})")
            if img_check["tiny_images"] > 0:
                print(f"    WARNING: {img_check['tiny_images']} tiny placeholder images detected")

            # URLs check
            url_check = result["checks"]["urls"]
            print(f"  URLs: {url_check['status']}", end="")
            print(f" (real: {url_check['real_links']}, invalid: {url_check['invalid_links']})")
            if url_check["invalid_list"]:
                print(f"    Invalid URLs: {url_check['invalid_list']}")

            # Engagement check
            eng_check = result["checks"]["engagement"]
            print(f"  Engagement metrics: {eng_check['status']}", end="")
            print(f" ({eng_check['metrics_found']} found)")

            # Page CSS check
            css_check = result["checks"]["page_css"]
            print(f"  Page CSS: {css_check['status']}")

            print()

        print("=" * 70)
        print(f"OVERALL STATUS: {self.results['overall_status']}")
        print("=" * 70 + "\n")


def main():
    """Main entry point for the QA check script."""
    parser = argparse.ArgumentParser(
        description="Validate HTML files before PDF assembly"
    )
    parser.add_argument(
        "--pages",
        nargs="+",
        required=True,
        help="HTML file names to validate"
    )
    parser.add_argument(
        "--working-dir",
        required=True,
        help="Directory containing HTML files"
    )

    args = parser.parse_args()

    # Validate working directory
    if not os.path.isdir(args.working_dir):
        print(f"Error: Working directory not found: {args.working_dir}", file=sys.stderr)
        sys.exit(1)

    # Run validation
    validator = QAValidator(args.working_dir)
    validator.validate_all(args.pages)
    validator.print_report()

    # Exit with appropriate code
    if validator.results["overall_status"] == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
