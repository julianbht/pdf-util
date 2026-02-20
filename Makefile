.PHONY: setup venv install clean run help

VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
PDF_UTIL = $(VENV_DIR)/bin/pdf-util

help:
	@echo "Available targets:"
	@echo "  setup     - Create venv and install dependencies"
	@echo "  venv      - Create virtual environment"
	@echo "  install   - Install dependencies from pyproject.toml"
	@echo "  clean     - Remove venv and cache files"
	@echo "  run       - Run pdf-util (use ARGS='...' for arguments)"

setup: venv install

venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
		echo "✓ Virtual environment created"; \
	else \
		echo "Virtual environment already exists"; \
	fi

install: venv
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -e .
	@echo "✓ Installation complete"
	@echo ""
	@echo "Activate the virtual environment with:"
	@echo "  source $(VENV_DIR)/bin/activate"
	@echo ""
	@echo "Run the CLI with:"
	@echo "  pdf-util --help"

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)
	rm -rf *.egg-info
	rm -rf __pycache__
	rm -rf pdf_util/__pycache__
	@echo "✓ Cleanup complete"

run: venv
	@echo "Example: make run ARGS='-o output.pdf file1.pdf file2.pdf'"
	$(PDF_UTIL) $(ARGS)
