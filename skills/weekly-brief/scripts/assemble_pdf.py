#!/usr/bin/env python3
"""
Assemble a multi-page PDF from HTML files using WeasyPrint and PyPDF.

This script takes multiple HTML files, converts each to PDF using WeasyPrint,
and merges them into a single multi-page PDF document.
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path


def install_package(package_name: str, pip_args: str = "") -> bool:
    """
    Install a package using pip with the specified arguments.

    Args:
        package_name: Package to install
        pip_args: Additional pip arguments (e.g., '--break-system-packages')

    Returns:
        True if installation succeeds, False otherwise
    """
    try:
        cmd = [sys.executable, "-m", "pip", "install", package_name]
        if pip_args:
            cmd.extend(pip_args.split())
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def import_with_fallback(module_name: str, package_name: str = None, pip_args: str = "") -> object:
    """
    Try to import a module, install if missing, then retry.

    Args:
        module_name: Module to import
        package_name: Package name for pip (defaults to module_name)
        pip_args: Additional pip arguments

    Returns:
        The imported module, or None if installation fails
    """
    if package_name is None:
        package_name = module_name

    try:
        return __import__(module_name)
    except ImportError:
        print(f"Package {package_name} not found. Installing...", file=sys.stderr)
        if install_package(package_name, pip_args):
            try:
                return __import__(module_name)
            except ImportError:
                return None
        return None


def render_html_to_pdf(html_file: str, working_dir: str) -> bytes:
    """
    Render an HTML file to PDF bytes using WeasyPrint.

    Args:
        html_file: Path to HTML file (relative or absolute)
        working_dir: Working directory containing HTML files

    Returns:
        PDF content as bytes

    Raises:
        Exception: If WeasyPrint is not available or rendering fails
    """
    if import_with_fallback("weasyprint", "weasyprint", "--break-system-packages") is None:
        raise RuntimeError(
            "Failed to install weasyprint. This likely means system dependencies are missing.\n"
            "On macOS, try: brew install cairo pango gdk-pixbuf libffi\n"
            "On Ubuntu/Debian, try: sudo apt-get install python3-cffi python3-brotli libcairo2 libpango-1.0-0\n"
            "On Fedora, try: sudo dnf install cairo-gobject-devel pango-devel\n"
            "Then run this script again."
        )

    file_path = os.path.join(working_dir, html_file)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"HTML file not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading HTML file {file_path}: {e}")

    try:
        from weasyprint import HTML
        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes
    except Exception as e:
        # Check if it's a missing system library error
        error_msg = str(e).lower()
        if any(lib in error_msg for lib in ['cairo', 'pango', 'gdk-pixbuf', 'ffi']):
            raise RuntimeError(
                f"WeasyPrint failed due to missing system libraries: {e}\n"
                "Please install the required system dependencies:\n"
                "  macOS: brew install cairo pango gdk-pixbuf libffi\n"
                "  Ubuntu/Debian: sudo apt-get install python3-cffi python3-brotli libcairo2 libpango-1.0-0\n"
                "  Fedora: sudo dnf install cairo-gobject-devel pango-devel"
            )
        raise RuntimeError(f"WeasyPrint rendering failed for {file_path}: {e}")


def merge_pdfs(pdf_bytes_list: list) -> bytes:
    """
    Merge multiple PDF byte objects into a single PDF.

    Args:
        pdf_bytes_list: List of PDF content as bytes

    Returns:
        Merged PDF content as bytes

    Raises:
        Exception: If pypdf is not available or merging fails
    """
    if import_with_fallback("pypdf", "pypdf", "--break-system-packages") is None:
        raise RuntimeError("Failed to install pypdf. Cannot merge PDFs.")

    try:
        # PdfWriter().append(...) is the recommended API in pypdf >= 5.0.
        # `PdfMerger` is deprecated and may be removed in a future major.
        from pypdf import PdfWriter
        from io import BytesIO

        writer = PdfWriter()

        for pdf_bytes in pdf_bytes_list:
            pdf_file = BytesIO(pdf_bytes)
            writer.append(pdf_file)

        output = BytesIO()
        writer.write(output)
        writer.close()

        return output.getvalue()
    except Exception as e:
        raise RuntimeError(f"PDF merging failed: {e}")


def main():
    """Main entry point for the PDF assembly script."""
    parser = argparse.ArgumentParser(
        description="Assemble a multi-page PDF from HTML files"
    )
    parser.add_argument(
        "--pages",
        nargs=3,
        required=True,
        metavar=("PAGE1", "PAGE2", "PAGE3"),
        help="Three HTML file names (P1, P2, P3)"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output PDF file name"
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

    # Render each HTML to PDF
    print(f"Rendering {len(args.pages)} HTML files to PDF...", file=sys.stderr)
    pdf_bytes_list = []

    for i, html_file in enumerate(args.pages, 1):
        try:
            print(f"  Converting {html_file}...", file=sys.stderr)
            pdf_bytes = render_html_to_pdf(html_file, args.working_dir)
            pdf_bytes_list.append(pdf_bytes)
            print(f"    OK ({len(pdf_bytes)} bytes)", file=sys.stderr)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Merge PDFs
    print("Merging PDFs...", file=sys.stderr)
    try:
        merged_pdf = merge_pdfs(pdf_bytes_list)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Save merged PDF
    output_path = os.path.join(args.working_dir, args.output)
    try:
        with open(output_path, 'wb') as f:
            f.write(merged_pdf)

        file_size = os.path.getsize(output_path)
        print(
            f"Success! Multi-page PDF created: {output_path} ({file_size} bytes)",
            file=sys.stderr
        )
        print(output_path)
    except IOError as e:
        print(f"Error writing output PDF: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
