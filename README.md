# PDF Util

A simple CLI tool for PDF operations built with Python and Typer.

## Features

- **Merge**: Combine multiple PDF files into a single document

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
pdf-util -o output.pdf file1.pdf file2.pdf file3.pdf
```

Or use the short form:

```bash
pdf-util -o merged.pdf *.pdf
```

### Help

```bash
pdf-util --help
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
