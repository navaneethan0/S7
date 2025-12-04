#!/bin/bash
# Build script for Render deployment
set -e

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Try to install spaCy (optional - app works without it)
# Skip if it takes too long or fails (building from source on Python 3.13 is very slow)
pip install spacy || echo "Warning: spaCy installation skipped - app will work without enhanced NLP features"

# Try to download spaCy model (non-critical)
python -m spacy download en_core_web_sm 2>/dev/null || echo "Warning: spaCy model download skipped"

