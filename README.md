# PDF Util

A simple CLI tool for PDF operations built with Python and Typer.

## Features

- **Merge**: Combine multiple PDF files into a single document
- **Rotate**: Rotate pages in a PDF by 90, 180, or 270 degrees
- **Keep**: Extract and keep only specific pages from a PDF

## Installation

### Quick Setup

```bash
make setup
```

This will create a virtual environment and install all dependencies.

### Manual Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

Activate the virtual environment:

```bash
source .venv/bin/activate
```

### Merge PDFs

```bash
pdf-util merge -o output.pdf file1.pdf file2.pdf file3.pdf
```

Or use the short form:

```bash
pdf-util merge -o merged.pdf *.pdf
```

### Rotate PDF Pages

Rotate all pages by 90 degrees clockwise:

```bash
pdf-util rotate input.pdf -o output.pdf -a 90
```

Rotate specific pages (e.g., pages 1-3):

```bash
pdf-util rotate input.pdf -o output.pdf -a 180 -p "1-3"
```

Rotate individual pages (e.g., pages 1, 3, and 5):

```bash
pdf-util rotate input.pdf -o output.pdf -a 270 -p "1,3,5"
```

Rotate all pages (default angle is 90 degrees):

```bash
pdf-util rotate input.pdf -o output.pdf
```

### Keep Specific Pages

Keep only pages 1, 3, and 5:

```bash
pdf-util keep input.pdf -o output.pdf -p "1,3,5"
```

Keep a range of pages (e.g., pages 2-4):

```bash
pdf-util keep input.pdf -o output.pdf -p "2-4"
```

Mix ranges and individual pages:

```bash
pdf-util keep input.pdf -o output.pdf -p "1-3,7,10-12"
```

### Help

```bash
pdf-util --help
pdf-util rotate --help
pdf-util merge --help
pdf-util keep --help
```

## Development

### Clean up

```bash
make clean
```

### Run with Make

```bash
make run ARGS="merge -o output.pdf file1.pdf file2.pdf"
```

## Requirements

- Python 3.8+
- typer
- pypdf
