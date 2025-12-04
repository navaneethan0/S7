#!/bin/bash
# Build script for Render deployment
set -e  # Exit on error
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python -m spacy download en_core_web_sm || echo "Warning: spaCy model download failed, but continuing..."

