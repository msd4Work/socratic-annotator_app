# Socratic Annotator – Installation Guide

Dieses Tool erlaubt dir, LLM-Antworten effizient zu annotieren.  
Die Anwendung läuft als **Streamlit-App** und kann auf zwei Arten installiert werden.

---

## 📦 1. Projekt herunterladen

1. Gehe zu GitHub → Projektseite  
2. Klicke auf **`<> Code` → `Download ZIP`**  
3. Entpacke die ZIP-Datei an einen gewünschten Ort.

Beispiel (macOS):  
`~/Documents/socratic-annotator_app`

Im Ordner findest du u. a.:

- `app.py`
- `README.md`
- `input_files/`   *(enthält Testfile – kann ignoriert werden)*
- `results/`

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

Danach Terminal/PowerShell neu starten.

---

## 🧩 Schritt 2 – Benötigte Pakete installieren

Öffne Terminal / PowerShell im Projektordner:

```bash
cd path/zum/Projektordner
```

# Beispiel:
```bash
cd ~/Documents/socratic-annotator_app
```


Installiere die benötigten Pakete:


```bash
pip install streamlit pandas openpyxl
```

## 🧩 Schritt 3 – App starten

```bash
streamlit run app.py
```

Dann sollte automatisch ein Browser mit der App geöffnet werden und
im Terminal dieses stehen (mit der URLs):


```bash
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8502
Network URL: http://192.168.254.108:8502
```


# 2️⃣ Variante B – Virtuelle Umgebung (empfohlen)

*"✔︎ Vorteile:""

- Keine Paket-Konflikte, 

- Saubere, isolierte Umgebung

- Kann komplett gelöscht werden, ohne System zu verändern

- Verhindert Versionsprobleme mit anderen Python-Projekten




## 🧩 Schritt 1 – venv erstellen

macOS:

```bash
cd path/zum/Projektordner
python3 -m venv annotator_env
```


Windows:

```bash
cd path\zum\Projektordner
python3 -m venv annotator_env
```

## 🧩 Schritt 2 – venv aktivieren

macOS:


```bash
source annotator_env/bin/activate
```

Windows (PowerShell oder CMD):

```bash
annotator_env\Scripts\activate
```

Deine Eingabeaufforderung sollte nun so aussehen:

```bash
(annotator_env) C:\Users\yourname\code\socratic-annotator_app

```



## 🧩 Schritt 3 – Dependencies installieren

```bash
pip install streamlit pandas openpyxl
```

```bash
pip install --upgrade openpyxl
```


## 🧩 Schritt 4 – App starten

```bash
streamlit run app.py
```


Dann sollte automatisch ein Browser mit der App geöffnet werden und
im Terminal dieses stehen (mit der URLs):


```bash
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8502
Network URL: http://192.168.254.108:8502
```




## 🧩 Schritt 5 – venv wieder verlassen


macOS + Windows:

```bash
deactivate
```

## 🧩 Optional – venv löschen (wenn nicht mehr benötigt)

Einfach den gesamten Ordner entfernen


---



# 📝 Manual

Wenn die App gestartet ist:

- Ausserhalb der App die Excels unter input_files/ ablegen!

- In die App gehen 
- und in der Sidebar Annotatorkürzel angeben
- Datei auswählen 
- Auf "Datei laden" klicken
- Mit „Weiter →“ die AI-Zeilen annotieren
- Ergebnisse / Zwischenergebnisse erscheinen in "results/"-Ordner

Es werden beim Annotieren jeweils eine Kopie der ausgewählten Datei gemacht und im result-ordner gespeichert.
Wenn die letzte Tutorantwort beurteilt wurde, wird der Excel-Kopie ein Kürzel und der Zeitstempel im Namen angefügt.
Unfertig annotierte Files bekommen den postfix "_in_progress" an den Namen gehängt und können fortgesetzt werden.



**Achtung, es gibt Probleme mit dem Rendering von Latex, Markdown etc.**
bei unklarheiten kann der originale Inhalt der Excel-Zellen angeschaut werden via

"🔍 Original anzeigen (Excel-Rohtext)" - Button


