.DEFAULT_GOAL := help

# Set python
export PYTHONPATH=.
python = python

.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  - PRODUCTION - "
	@echo "  install 		Install the dependencies for deployment"
	@echo "  run_bot		Start the TG bot"
	@echo " "
	@echo "  - DEVELOPMENT -"
	@echo "  lint			Reformat code"
	@echo "  install_dev	Install the dependencies for development"


# ================================================================================================
# Dependencies
# ================================================================================================

.PHONY: install
install:
	$(python) -m pip install -r requirements/prod.txt

.PHONY: install_dev
install_dev:
	$(python) -m pip install -r requirements/dev.txt


# ================================================================================================
# Lint
# ================================================================================================

.PHONY:	black
black:
	$(python) -m black --line-length 80 .

.PHONY: isort
isort:
	$(python) -m isort .

.PHONY: flake
flake:
	$(python) -m flake8 .

.PHONY: lint
lint: black isort flake


# ================================================================================================
# Start
# ================================================================================================

.env:
	# Check if .env file exists
	@echo "ERROR: You need to specify TOKENS in .env file. Read README.md for more info."
	exit 1

.PHONY: run_bot
run_bot: .env
	@echo "Running bot..."
	$(python) src/bot.py