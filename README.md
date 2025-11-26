# socratic-annotator_app

Tutor Annotation App

Ein Tool zur Annotation von Tutor–Antworten basierend auf Excel-Dialogdaten.

Dieses Repository enthält:

app.py – die Streamlit App

input_files/ – Ordner für neue Excel-Dateien

results/ – hier speichert die App deine annotierten Dateien

README.md – diese Anleitung

Installation Guide

Du kannst die App auf zwei Arten ausführen:

Mit global installiertem Python (einfach & für alle ausreichend)

Mit einer eigenen Python-virtuellen Umgebung (empfohlen)
– sauber, isoliert, keine Konflikte, leichter entfernbar

Beide Wege funktionieren auf macOS und Windows.

📥 1. Repository herunterladen
Option A — Über Github ZIP (einfach)

Klicke auf den grünen <> Code-Button.

Wähle Download ZIP.

Entpacke das ZIP in einen Ordner deiner Wahl, z. B.:

macOS:

/Users/deinname/Code/socratic-annotator_app/


Windows:

C:\Users\deinname\code\socratic-annotator_app\

🐍 2. Installation mit globalem Python

(Einfachste Methode – funktioniert überall)

Voraussetzung

Installiere Python (falls nicht vorhanden):

macOS: https://www.python.org/downloads/macos/

Windows: https://www.python.org/downloads/windows/

→ Achtung: Beim Installer „Add Python to PATH“ aktivieren!

Schritt 1: Abhängigkeiten installieren
macOS Terminal öffnen
cd /Users/deinname/Code/socratic-annotator_app
pip install -r requirements.txt

Windows PowerShell / CMD öffnen
cd C:\Users\deinname\code\socratic-annotator_app
pip install -r requirements.txt

Schritt 2: App starten
macOS
streamlit run app.py

Windows
streamlit run app.py


Fertig ✔
Der Browser öffnet sich automatisch.

🧪 3. (Empfohlen) Installation mit Virtual Environment

Ein venv isoliert deine App vollständig vom restlichen System.

Vorteile

Kein Konflikt mit System-Python oder anderen Projekten

Sauber entfernbar: einfach Ordner löschen

Reproduzierbare Umgebung

Standard in Softwareprojekten

🔧 Anleitung: Virtual Environment
macOS
1. venv erstellen
cd /Users/deinname/Code/socratic-annotator_app
python3 -m venv venv

2. aktivieren
source venv/bin/activate

3. Abhängigkeiten installieren
pip install -r requirements.txt

4. App starten
streamlit run app.py

5. venv deaktivieren
deactivate

Windows
1. venv erstellen
cd C:\Users\deinname\code\socratic-annotator_app
python -m venv venv

2. aktivieren

PowerShell:

venv\Scripts\Activate.ps1


CMD:

venv\Scripts\activate.bat

3. Abhängigkeiten installieren
pip install -r requirements.txt

4. App starten
streamlit run app.py

5. venv deaktivieren
deactivate

🗑 Entfernen / Aufräumen

Lösche einfach den gesamten Projektordner

OPTIONAL: Wenn du ein venv verwendet hast, lösche nur den Ordner venv/

Keine Registry-Einträge, keine Systemänderungen.