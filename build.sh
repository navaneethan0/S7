#!/bin/bash
# Build script for Render deployment
set -e  # Exit on error
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
# Download spaCy model (mandatory)
python -m spacy download en_core_web_sm
echo "✅ spaCy and model installed successfully"

