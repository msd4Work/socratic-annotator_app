#!/bin/bash

# Pfad zum Projekt
APP_DIR="$(cd "$(dirname "$0")" && pwd)"

# Virtuelle Umgebung aktivieren
source "$APP_DIR/app_env/bin/activate"

# App starten
streamlit run "$APP_DIR/app.py"
