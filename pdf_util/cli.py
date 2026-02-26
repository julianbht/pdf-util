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


@app.command()
def rotate(
    input_file: Path = typer.Argument(
        ...,
        help="Input PDF file",
        exists=True,
        dir_okay=False,
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output PDF file path",
    ),
    angle: int = typer.Option(
        90,
        "--angle",
        "-a",
        help="Rotation angle (90, 180, or 270 degrees clockwise)",
    ),
    pages: str = typer.Option(
        None,
        "--pages",
        "-p",
        help="Pages to rotate (e.g., '1', '1-3', '1,3,5', or 'all' for all pages). Default: all",
    ),
) -> None:
    """Rotate pages in a PDF file."""
    if input_file.suffix.lower() != ".pdf":
        typer.echo(f"Error: {input_file} is not a PDF file", err=True)
        raise typer.Exit(1)

    if angle not in [90, 180, 270]:
        typer.echo("Error: Angle must be 90, 180, or 270 degrees", err=True)
        raise typer.Exit(1)

    try:
        reader = PdfReader(str(input_file))
        writer = PdfWriter()
        total_pages = len(reader.pages)

        # Parse pages argument
        pages_to_rotate = set()
        if pages is None or pages.lower() == "all":
            pages_to_rotate = set(range(total_pages))
        else:
            # Parse page ranges and individual pages
            for part in pages.split(","):
                part = part.strip()
                if "-" in part:
                    # Handle range (e.g., "1-3")
                    start, end = part.split("-")
                    start_idx = int(start.strip()) - 1  # Convert to 0-indexed
                    end_idx = int(end.strip()) - 1
                    if start_idx < 0 or end_idx >= total_pages:
                        typer.echo(
                            f"Error: Page range {part} is out of bounds (1-{total_pages})",
                            err=True,
                        )
                        raise typer.Exit(1)
                    pages_to_rotate.update(range(start_idx, end_idx + 1))
                else:
                    # Handle single page
                    page_num = int(part) - 1  # Convert to 0-indexed
                    if page_num < 0 or page_num >= total_pages:
                        typer.echo(
                            f"Error: Page {part} is out of bounds (1-{total_pages})",
                            err=True,
                        )
                        raise typer.Exit(1)
                    pages_to_rotate.add(page_num)

        typer.echo(
            f"Rotating {len(pages_to_rotate)} page(s) by {angle} degrees in {input_file.name}..."
        )

        # Process pages
        for i, page in enumerate(reader.pages):
            if i in pages_to_rotate:
                page.rotate(angle)
                typer.echo(f"  Rotated page {i + 1}")
            writer.add_page(page)

        typer.echo(f"Writing rotated PDF to: {output}")
        with open(output, "wb") as f:
            writer.write(f)

        typer.secho("✓ Successfully rotated PDF!", fg=typer.colors.GREEN, bold=True)

    except ValueError as e:
        typer.echo(f"Error parsing page numbers: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error rotating PDF: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def keep(
    input_file: Path = typer.Argument(
        ...,
        help="Input PDF file",
        exists=True,
        dir_okay=False,
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output PDF file path",
    ),
    pages: str = typer.Option(
        ...,
        "--pages",
        "-p",
        help="Pages to keep (e.g., '1', '1-3', '1,3,5')",
    ),
) -> None:
    """Keep only specific pages from a PDF, removing the rest."""
    if input_file.suffix.lower() != ".pdf":
        typer.echo(f"Error: {input_file} is not a PDF file", err=True)
        raise typer.Exit(1)

    try:
        reader = PdfReader(str(input_file))
        writer = PdfWriter()
        total_pages = len(reader.pages)

        # Parse pages argument
        pages_to_keep: set[int] = set()
        for part in pages.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-")
                start_idx = int(start.strip()) - 1
                end_idx = int(end.strip()) - 1
                if start_idx < 0 or end_idx >= total_pages:
                    typer.echo(
                        f"Error: Page range {part} is out of bounds (1-{total_pages})",
                        err=True,
                    )
                    raise typer.Exit(1)
                pages_to_keep.update(range(start_idx, end_idx + 1))
            else:
                page_num = int(part) - 1
                if page_num < 0 or page_num >= total_pages:
                    typer.echo(
                        f"Error: Page {part} is out of bounds (1-{total_pages})",
                        err=True,
                    )
                    raise typer.Exit(1)
                pages_to_keep.add(page_num)

        if not pages_to_keep:
            typer.echo("Error: No pages specified to keep", err=True)
            raise typer.Exit(1)

        typer.echo(
            f"Keeping {len(pages_to_keep)} of {total_pages} page(s) from {input_file.name}..."
        )

        for i in sorted(pages_to_keep):
            writer.add_page(reader.pages[i])
            typer.echo(f"  Keeping page {i + 1}")

        typer.echo(f"Writing to: {output}")
        with open(output, "wb") as f:
            writer.write(f)

        typer.secho("✓ Successfully extracted pages!", fg=typer.colors.GREEN, bold=True)

    except ValueError as e:
        typer.echo(f"Error parsing page numbers: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error extracting pages: {e}", err=True)
        raise typer.Exit(1)


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
