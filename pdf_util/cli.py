"""PDF Utility CLI."""

from pathlib import Path
from typing import List

import typer
from pypdf import PdfReader, PdfWriter

app = typer.Typer(help="PDF Utility CLI Tool")


@app.command()
def merge(
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output PDF file path",
    ),
    files: List[Path] = typer.Argument(
        ...,
        help="PDF files to merge (in order)",
        exists=True,
        dir_okay=False,
    ),
) -> None:
    """Merge multiple PDF files into one."""
    if len(files) < 2:
        typer.echo("Error: At least 2 PDF files are required for merging", err=True)
        raise typer.Exit(1)

    # Validate all files are PDFs
    for file in files:
        if file.suffix.lower() != ".pdf":
            typer.echo(f"Error: {file} is not a PDF file", err=True)
            raise typer.Exit(1)

    try:
        writer = PdfWriter()

        typer.echo(f"Merging {len(files)} PDF files...")
        for file in files:
            typer.echo(f"  Adding: {file}")
            reader = PdfReader(str(file))
            for page in reader.pages:
                writer.add_page(page)

        typer.echo(f"Writing merged PDF to: {output}")
        with open(output, "wb") as f:
            writer.write(f)

        typer.secho("✓ Successfully merged PDFs!", fg=typer.colors.GREEN, bold=True)

    except Exception as e:
        typer.echo(f"Error merging PDFs: {e}", err=True)
        raise typer.Exit(1)


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
