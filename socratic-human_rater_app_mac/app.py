import os
from pathlib import Path
from datetime import datetime
import shutil

import pandas as pd
import streamlit as st
import re
import math






# ---------------------------------------
# TEXT-NORMALISIERUNG (STATE MACHINE)
# ---------------------------------------

import re

# -------------------------
# Hilfsfunktionen
# -------------------------

def cleanup_table_row(line: str) -> str:
    """
    Entfernt Excel-Artefakte und Ghost-Characters aus Tabellenzeilen:
    - schneidet alles nach dem letzten Pipe ab (z.B. |_x000D_)
    - entfernt Zero-width-chars / BOM
    - trimmt trailing whitespace
    """
    if not isinstance(line, str):
        return line

    raw = line
    if "|" in raw:
        before, _, _ = raw.rpartition("|")
        cleaned = before + "|"

        cleaned = cleaned.replace("\u200b", "")
        cleaned = cleaned.replace("\ufeff", "")
        cleaned = cleaned.replace("\u2060", "")

        cleaned = cleaned.rstrip(" \t")
        return cleaned

    return raw


def is_table_row(line: str) -> bool:
    """Erkennt eine Markdown-Tabellenzeile."""
    line = line.strip()
    return line.startswith("|") and line.count("|") >= 2


def is_header(line: str) -> bool:
    """Erkennt Markdown-Header mit #."""
    return re.match(r"^#{1,6}\s+", line) is not None


def convert_latex_blocks(line: str) -> str:
    """\[...\] → $$ ... $$ (ohne Tabellen zu zerstören)."""
    if "\\[" in line and "\\]" in line:
        inner = re.sub(r".*?\\\[(.*?)\\\].*", r"\1", line, flags=re.DOTALL).strip()
        return f"$$\n{inner}\n$$"
    return line


def convert_latex_inline(line: str) -> str:
    """Repariert \( ... \) und entfernt Excel-Artefakte um die Klammern."""
    line = re.sub(r"_*\s*\\\(\s*", r"\\(", line)
    line = re.sub(r"\s*\\\)\s*_*\s*", r"\\)", line)
    return line


def convert_plain_formula(line: str) -> str:
    """Standalone-LaTeX auf ganzer Zeile → $$...$$ (außer in Tabellen)."""
    if "|" in line:
        return line

    if re.search(r"\\(frac|sum|text|bar|sqrt|Cov|sigma|mu|alpha)", line):
        stripped = line.strip()
        # Wenn die Zeile *nur* aus Formel besteht, als Block setzen
        return f"$$\n{stripped}\n$$"
    return line


def repair_umlauts(line: str) -> str:
    """Kaputte Excel-Umlaute (a\\n¨) reparieren."""
    line = re.sub(r"a\s*\n\s*¨", "ä", line)
    line = re.sub(r"o\s*\n\s*¨", "ö", line)
    line = re.sub(r"u\s*\n\s*¨", "ü", line)
    line = re.sub(r"A\s*\n\s*¨", "Ä", line)
    line = re.sub(r"O\s*\n\s*¨", "Ö", line)
    line = re.sub(r"U\s*\n\s*¨", "Ü", line)
    return line


# -------------------------
# PHASE 1 – Excel Cleanup
# -------------------------

def phase1_excel_cleanup(txt: str) -> str:
    """Entfernt Excel-Artefakte, ohne Markdown/Tabellen zu zerstören."""
    if txt is None:
        return ""
    txt = str(txt)

    # Steuerzeichen killen (außer newline)
    txt = re.sub(r"[\x00-\x08\x0B-\x1F]", "", txt)

    # Zeilenumbrüche normalisieren
    txt = txt.replace("\r\n", "\n").replace("\r", "\n")

    # Excel _x000D_ / x000D Varianten → newline
    txt = re.sub(r"_?x000D_?", "\n", txt)

    # Unicode line separators
    txt = txt.replace("\u2028", "\n").replace("\u2029", "\n")

    # Non-breaking spaces etc. entfernen
    txt = txt.replace("\u00A0", " ").replace("\u200B", "").replace("\ufeff", "")

    # Tabellenzeilen schon hier säubern (abschneiden nach letztem "|")
    lines = txt.split("\n")
    lines = [cleanup_table_row(ln) for ln in lines]
    txt = "\n".join(lines)

    return txt


# -------------------------
# PHASE 2 – Struktur-Fix (State Machine)
# -------------------------

# -------------------------
# PHASE 2 – Struktur-Fix (State Machine)
# -------------------------

def phase2_structure_fix(txt: str) -> str:
    """Repariert Header, Tabellen, Formeln und Leerzeilen kontextabhängig."""
    lines = txt.split("\n")
    out = []

    in_table = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

        # -----------------------------------
        # LEERE ZEILEN
        # -----------------------------------
        if stripped == "":
            if in_table:
                # Excel-Leerzeilen zwischen Tabellenzeilen → ignorieren
                continue
            if len(out) == 0 or out[-1] == "":
                continue
            out.append("")
            continue

        # -----------------------------------
        # HEADER
        # -----------------------------------
        if is_header(stripped):
            out.append(stripped)
            # Nur Leerzeile, wenn danach keine Tabelle folgt
            if not is_table_row(next_line):
                out.append("")
            continue

        # -----------------------------------
        # TABELLENZEILE
        # -----------------------------------
        if is_table_row(stripped):
            # Tabellenstart
            if not in_table:
                if len(out) > 0 and out[-1] != "" and not is_header(out[-1]):
                    out.append("")  # Leerzeile VOR Tabelle
                in_table = True

            out.append(stripped)
            continue

        # -----------------------------------
        # TABELLENENDE
        # -----------------------------------
        if in_table and not is_table_row(stripped):
            out.append("")      # genau EINE Leerzeile nach Tabelle
            in_table = False
            # Danach: weiter mit normaler Verarbeitung (kein continue)

        # -----------------------------------
        # FORMELN
        # -----------------------------------
        if "\\[" in stripped and "\\]" in stripped:
            out.append(convert_latex_blocks(stripped))
            continue

        # Inline-LaTeX reparieren
        stripped = convert_latex_inline(stripped)

        # Standalone LaTeX zu $$...$$
        stripped = convert_plain_formula(stripped)

        # Umlaute
        stripped = repair_umlauts(stripped)

        # Normale Zeile hinzufügen
        out.append(stripped)

    return "\n".join(out)



# -------------------------
# PHASE 3 – Final Cleanup
# -------------------------

def phase3_final_cleanup(txt: str) -> str:
    """Letzte Schönheitskorrekturen."""
    # Maximal zwei Leerzeilen hintereinander
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip()


# -------------------------
# MASTER-Funktion
# -------------------------

def normalize_text(txt: str) -> str:
    """Hauptpipeline für sicheren Markdown-Import aus Excel."""
    if txt is None:
        return ""

    t1 = phase1_excel_cleanup(txt)
    t2 = phase2_structure_fix(t1)
    t3 = phase3_final_cleanup(t2)
    return t3




# ---------------------------------------
# CONFIG
# ---------------------------------------

st.set_page_config(page_title="Tutor Annotation", layout="wide")

APP_DIR = Path(__file__).resolve().parent
INPUT_DIR_DEFAULT = APP_DIR / "input_files"
RESULTS_DIR = APP_DIR / "results"

INPUT_DIR_DEFAULT.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------
# CLEAN MESSAGE TEXT
# ---------------------------------------

def clean_message_column(df: pd.DataFrame) -> pd.DataFrame:
    if "message" not in df.columns:
        return df

    # ORIGINALTEXT SICHERN (unverändert!)
    df["message_raw"] = df["message"].astype(str)

    # Normalisierte Version erzeugen
    df["message"] = df["message"].astype(str).apply(normalize_text)

    return df


# ---------------------------------------
# ANNOTATION SPALTEN
# ---------------------------------------

def ensure_annotation_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "CommentIsSuitableTutor": "isCommentSuitable",
        "CommentIsCorrectTutor": "isCommentCorrect",
    }
    df = df.rename(columns=rename_map)

    for col in ["IsSuitableTutor", "IsCorrectTutor", "isCommentSuitable", "isCommentCorrect"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").replace("nan", "")

    df = clean_message_column(df)
    return df


# ---------------------------------------
# AI INDICES
# ---------------------------------------

def compute_ai_indices(df: pd.DataFrame):
    if "role" not in df.columns:
        return []
    return df.index[df["role"] == "ai"].tolist()


# ---------------------------------------
# PROGRESS
# ---------------------------------------

def get_position_progress(current_pos: int, ai_indices):
    total = len(ai_indices)
    if total == 0:
        return 0, 0, 0.0
    completed = current_pos + 1
    return completed, total, completed / total


# ---------------------------------------
# OUTPUT FILE
# ---------------------------------------

def create_output_file(raw_file: str, annotator: str):
    raw_stem = Path(raw_file).stem
    now = datetime.now().strftime("%Y%m%d-%H%M")
    new_name = f"{raw_stem}__{annotator}__{now}_inprogress.xlsx"
    return RESULTS_DIR / new_name, raw_stem


# ---------------------------------------
# SAVE
# ---------------------------------------

def save_df():
    if "df" in st.session_state and "file_path" in st.session_state:
        st.session_state.df.to_excel(st.session_state.file_path, index=False)


# ---------------------------------------
# AUTO DONE
# ---------------------------------------

def mark_done_if_finished(current_pos: int):
    total = len(st.session_state.ai_indices)
    if total == 0:
        return

    if current_pos >= total - 1:
        p = Path(st.session_state.file_path)
        stem = st.session_state.original_stem
        ann = st.session_state.annotator or "anon"
        now = datetime.now().strftime("%Y%m%d-%H%M")
        new_name = f"{stem}__{ann}__{now}_done.xlsx"
        new_p = RESULTS_DIR / new_name
        if p.exists():
            p.rename(new_p)
            st.session_state.file_path = str(new_p)
            st.success("Ende erreicht – Datei gespeichert.")


# ---------------------------------------
# SESSION INIT
# ---------------------------------------

default_session = {
    "df": None,
    "ai_indices": [],
    "current_ai_pos": 0,
    "file_path": None,
    "original_stem": None,
    "annotator": ""
}
for k, v in default_session.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ---------------------------------------
# SIDEBAR: DATEIEN UND EINSTELLUNGEN
# ---------------------------------------

st.sidebar.header("Einstellungen")

annot = st.sidebar.text_input("Annotator-Kürzel", value=st.session_state.annotator)
st.session_state.annotator = annot.strip()

choose_other_dir = st.sidebar.checkbox("Anderes Input-Verzeichnis wählen")

if choose_other_dir:
    input_dir = Path(st.sidebar.text_input("Pfad:", value=str(INPUT_DIR_DEFAULT)))
else:
    input_dir = INPUT_DIR_DEFAULT

input_dir.mkdir(exist_ok=True)
st.sidebar.write(f"Input-Verzeichnis: **{input_dir}**")

mode = st.sidebar.radio("Modus", ["Neue Excel annotieren", "Fortsetzen"])

excel_new = [f for f in os.listdir(input_dir) if f.lower().endswith(".xlsx")]
excel_inprogress = [p.name for p in RESULTS_DIR.glob("*_inprogress.xlsx")]

selected_file = st.sidebar.selectbox(
    "Datei:",
    excel_new if mode == "Neue Excel annotieren" else excel_inprogress
)

if st.sidebar.button("Datei laden"):
    if not annot:
        st.sidebar.error("Annotator fehlt.")
        st.stop()

    if not selected_file:
        st.sidebar.error("Keine Datei ausgewählt.")
        st.stop()

    if mode == "Neue Excel annotieren":
        raw_path = input_dir / selected_file
        out_path, stem = create_output_file(selected_file, annot)
        shutil.copy2(raw_path, out_path)
        df = pd.read_excel(out_path)
        df = ensure_annotation_columns(df)

        st.session_state.file_path = str(out_path)
        st.session_state.original_stem = stem

    else:
        p = RESULTS_DIR / selected_file
        df = pd.read_excel(p)
        df = ensure_annotation_columns(df)

        name_parts = Path(selected_file).stem.split("__")
        st.session_state.original_stem = name_parts[0] if name_parts else Path(selected_file).stem
        st.session_state.file_path = str(p)

    st.session_state.df = df
    st.session_state.ai_indices = compute_ai_indices(df)
    st.session_state.current_ai_pos = 0
    st.rerun()


# --------------------------
# SIDEBAR: NAVIGATION PANEL
# --------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Aktuelles File")

if st.session_state.file_path:
    st.sidebar.write(f"**{Path(st.session_state.file_path).name}**")
else:
    st.sidebar.info("Kein File geladen.")

# Fortschritt
current_pos = st.session_state.current_ai_pos
completed, total, prog = get_position_progress(current_pos, st.session_state.ai_indices)

if total > 0:
    st.sidebar.progress(prog)
    st.sidebar.write(f"**{completed} / {total} annotiert**")

    st.sidebar.markdown("### Navigation")

    col_sb_prev, col_sb_next = st.sidebar.columns(2)

    with col_sb_prev:
        if st.sidebar.button("← Zurück", key="sb_prev"):
            if current_pos > 0:
                st.toast("Zurück zur vorherigen AI-Antwort", icon="⬅️")
                st.session_state.current_ai_pos = current_pos - 1
                st.rerun()

    with col_sb_next:
        if st.sidebar.button("Weiter →", key="sb_next"):
            if current_pos < total - 1:
                st.toast("Weiter zur nächsten AI-Antwort", icon="➡️")
                st.session_state.current_ai_pos = current_pos + 1
                st.rerun()
            else:
                mark_done_if_finished(current_pos)

else:
    st.sidebar.info("Noch keine AI-Zeilen geladen.")


# ---------------------------------------
# MAIN AREA
# ---------------------------------------

st.title("Tutor-Dialog Annotation (AI-Rolle)")

if st.session_state.df is None:
    st.info("Bitte Datei wählen und laden.")
    st.stop()

df = st.session_state.df
ai_indices = st.session_state.ai_indices

if not ai_indices:
    st.error("Keine role=='ai' gefunden.")
    st.stop()

current_idx = ai_indices[current_pos]

# ---------------------------------------
# Dialogkontext (immer geöffnet, ohne doppelte AI-Zeile)
# ---------------------------------------

st.subheader("Dialogkontext")

N_CONTEXT = 10  # Anzahl vorheriger Zeilen
start_idx = 0
end_idx = current_idx - 1

with st.expander("Dialog bis zur aktuellen AI-Antwort anzeigen", expanded=True):
    if start_idx <= end_idx:
        for i in range(start_idx, end_idx + 1):
            row = df.iloc[i]
            role = str(row.get("role", "")).lower()
            msg = str(row.get("message", ""))

            with st.chat_message("assistant" if role == "ai" else "user"):
                st.markdown(msg)
    else:
        st.info("Keine vorherigen Nachrichten vorhanden.")

# ---------------------------------------
# Aktuelle AI-Antwort anzeigen (nur 1x)
# ---------------------------------------

st.markdown("### 🟨 Diese Antwort wird gerade annotiert")
st.info(df.loc[current_idx, "message"])

# ---------------------------------------
# ORIGINAL EXCEL-TEXT ANZEIGEN
# ---------------------------------------

if "message_raw" in df.columns:
    with st.expander("🔍 Original anzeigen (Excel-Rohtext)"):
        raw = df.loc[current_idx, "message_raw"]
        st.code(str(raw), language="markdown")


# ---------------------------------------
# ANNOTATION
# ---------------------------------------

st.markdown("## Annotation")

options = ["j", "n", "Clear"]

# Suitable?
st.markdown("**1. Ist diese Antwort als Tutor geeignet?**")
raw_s = str(df.loc[current_idx, "IsSuitableTutor"]).strip()
idx_s = {"j": 0, "n": 1}.get(raw_s, 2)

sel_s = st.radio(
    "IsSuitableTutor",
    options,
    index=idx_s,
    horizontal=True,
    label_visibility="collapsed",
    key=f"suit_{current_idx}"
)
val_s = "" if sel_s == "Clear" else sel_s
df.at[current_idx, "IsSuitableTutor"] = val_s

if val_s == "n":
    comment_s = st.text_area(
        "Kommentar zu Eignung (nur wenn 'n')",
        value=str(df.loc[current_idx, "isCommentSuitable"]),
        height=80,
        key=f"suit_comment_{current_idx}"
    )
    df.at[current_idx, "isCommentSuitable"] = comment_s
else:
    df.at[current_idx, "isCommentSuitable"] = ""

st.markdown("---")

# Correct?
st.markdown("**2. Ist die Antwort inhaltlich korrekt?**")
raw_c = str(df.loc[current_idx, "IsCorrectTutor"]).strip()
idx_c = {"j": 0, "n": 1}.get(raw_c, 2)

sel_c = st.radio(
    "IsCorrectTutor",
    options,
    index=idx_c,
    horizontal=True,
    label_visibility="collapsed",
    key=f"corr_{current_idx}"
)
val_c = "" if sel_c == "Clear" else sel_c
df.at[current_idx, "IsCorrectTutor"] = val_c

if val_c == "n":
    comment_c = st.text_area(
        "Kommentar zu Korrektheit (nur wenn 'n')",
        value=str(df.loc[current_idx, "isCommentCorrect"]),
        height=80,
        key=f"corr_comment_{current_idx}"
    )
    df.at[current_idx, "isCommentCorrect"] = comment_c
else:
    df.at[current_idx, "isCommentCorrect"] = ""

# Save
st.session_state.df = df
save_df()
