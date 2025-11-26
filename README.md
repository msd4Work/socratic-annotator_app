# Socratic Annotator – Installation Guide

Dieses Tool erlaubt dir, LLM-Antworten effizient zu annotieren.  
Die Anwendung läuft als **Streamlit-App** und kann auf zwei Arten installiert werden:

---

## 📦 1. Projekt herunterladen

1. Gehe zu GitHub → Projektseite  
2. Klicke auf **`<> Code` → `Download ZIP`**  
3. Entpacke die ZIP-Datei an einen gewünschten Ort.


Im Ordner findest du:
- app.py
- README.md
- input_files/   <--enthält ein Testfile, bitte ignorieren
- results/


---

# 🚀 Installation (2 Wege)

Du kannst die App auf zwei verschiedene Arten ausführen:

1. **Globales Python installieren**  
2. **Isolierte virtuelle Umgebung (empfohlen)**

Beide Varianten funktionieren auf macOS und Windows.

---

# 1️⃣ Variante A – Globales Python installieren (einfachste Methode)

### ✔︎ Gut geeignet für:
- Nutzer ohne Python-Erfahrung  
- Wenn du schnell starten möchtest  
- Wenn dein System bereits Python nutzt und du keine isolierte Umgebung brauchst

---

## 🧩 Schritt 1 – Python installieren

### macOS:
Download: https://www.python.org/downloads/macos/

### Windows:
Download: https://www.python.org/downloads/windows/

**Wichtig:** Beim Installieren unbedingt aktivieren:

- **Add Python to PATH** (Windows)
- Danach Terminal/PowerShell neu starten

---

## 🧩 Schritt 2 – Benötigte Pakete installieren

Öffne Terminal / PowerShell im Projektordner:

```bash
cd path/zum/Projektordner
```

```bash
pip install streamlit pandas openpyxl
```

## 🧩 Schritt 3 – App starten
streamlit run app.py

---


# 2️⃣ Variante B – Virtuelle Umgebung (empfohlen)

**✔︎ Vorteile:**

- Keine Paket-Konflikte
- Saubere, isolierte Umgebung
- Kann später vollständig gelöscht werden
- Verhindert Versionsprobleme


---

## 🧩 Schritt 1 – venv erstellen

macOS:

```bash
cd path/zum/Projektordner
python3 -m venv 
```


Windows

```bash
cd path/zum/Projektordner
python3 -m venv app_env
```


## 🧩 Schritt 2 – venv aktivieren

macOS:

```bash
source app_env/bin/activate
```


```bash
app_env\Scripts\activate
```


## 🧩 Schritt 3 – Dependencies installieren


pip install streamlit pandas openpyxl


## 🧩 Schritt 4 – App starten

```bash
streamlit run app.py
```


## 🧩 Schritt 5 – venv wieder verlassen


macOS + Windows::


```bash
deactivate
```

## 🧩 Optional – venv löschen (wenn nicht mehr benötigt)

Einfach den ganzen Ordner löschen.

