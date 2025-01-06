# Makefile

# Define variables
CHROME_DEB=google-chrome-stable_129.0.6668.89-1_amd64.deb
PYTHON_REQUIRED=3.10
PY_VERSION := $(shell python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

# Specify that Make should use bash
SHELL := /bin/bash

.PHONY: all new check-chrome install-chrome check-python agents run clear run-new start-docker pack debug

# Default target
all: new


# Debug target to check PY_VERSION
debug:
	@echo "Detected Python Version: $(PY_VERSION)"

# New target: Sets up the environment and prompts for activation code
new: check-chrome check-python
	sudo apt-get install xvfb
	@echo "Setting up Python virtual environment..."
	@python3 -m venv venv || { echo "Failed to create virtual environment"; exit 1; }
	@echo "Installing dependencies..."
	@venv/bin/pip install --upgrade pip >> install_log.txt 2>&1 || { echo "Failed to upgrade pip"; exit 1; }
	@venv/bin/pip install -r requirements.txt >> install_log.txt 2>&1 || { echo "Failed to install dependencies"; exit 1; }
	@touch wallets.json proxy.txt wallets_evm.json
	@echo -e "\n\n\nVirtual environment has been created and dependencies installed."
	@echo -e "\nNow create or import SOLANA (SOL) wallets from KOZEL (https://t.me/hcmarket_bot?start=project_1)\n"
	@echo "Please enter wallets.json, wallets_evm.json and proxy.txt"
	@echo -e "Run the following command to proceed:\n↓ ↓ ↓ ↓ ↓\nmake agents"




# Check if Google Chrome is installed
check-chrome:
	@command -v google-chrome >/dev/null 2>&1 || { \
		echo "Google Chrome is not installed. Installing..."; \
		$(MAKE) install-chrome; \
	}

# Install Google Chrome on Ubuntu with logs redirected to install_log.txt
install-chrome:
	@echo "Installing Google Chrome. Logs are being saved to install_log.txt."
	@if [ ! -f "$(CHROME_DEB)" ]; then \
		echo "Downloading Google Chrome package..."; \
		wget -q wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_129.0.6668.89-1_amd64.deb || { echo "Failed to download Google Chrome. Check your internet connection."; exit 1; }; \
	fi
	@sudo apt update >> install_log.txt 2>&1 || { echo "Failed to update package list. Check install_log.txt for details."; exit 1; }
	@sudo apt install -y ./$(CHROME_DEB) >> install_log.txt 2>&1 || { echo "Failed to install Google Chrome. Check install_log.txt for details."; exit 1; }
	@rm -f $(CHROME_DEB)
	@echo "Google Chrome has been installed successfully."



# Check if the Python version is 3.10.x
check-python:
	@if [ "$(PY_VERSION)" != "$(PYTHON_REQUIRED)" ]; then \
		echo "Error: Python $(PYTHON_REQUIRED) is required. Current version is $(PY_VERSION)."; \
		exit 1; \
	else \
		echo "Python version $(PY_VERSION) detected."; \
	fi

	@sudo apt install python3.10-venv

# Agents target
agents:
	@venv/bin/python3 useragents.py && echo -e "\nNow you can run\n↓ ↓ ↓ ↓\nmake run\n\nor\n\nmake run-new"

# Run the application
run:
	@venv/bin/python3 app.py

# Clear profiles
clear:
	@rm -rf profiles/*

# Run the application with cleanup
run-new:
	@rm -rf profiles/* screenshots/* && venv/bin/python3 app.py

# Start Docker container
start-docker:
	@docker run --rm -p 127.0.0.1:4444:4444 ud-chrome-116

# Pack the project
pack:
	@rm -rf extensions/proxy_extension_mv3 || true
	@rm -rf screenshots/* || true
	@rm hyperlane.zip || true
	@find . -type d -maxdepth 3 -exec sh -c 'echo "Created by Aero25x for HiddenCode\n\nhttps://t.me/hidden_coding\nhttps://github.com/Aero25x" > "{}/author.txt"' \;
	@zip -vr phoenix.zip . -x "*.log" "__pycache__/*" "*.tmp" "node_modules/*" ".env" "tests/*" "proxy.txt" "wallets.json" "install_log.*" "proxy.txt" ".gitignore" "wallets copy.json" "profiles/*" "generate.py" "./venv/*" "activation.txt" "./venv" ".git" ".git/*" ".ropeproject" "*.csv" ".ropeproject/*"
	@find . -type f -name "author.txt" -delete
