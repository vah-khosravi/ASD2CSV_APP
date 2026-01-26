# asd2csv_app.py
# ASD2CSV - Browser-based desktop GUI (Flask) packaged via PyInstaller
# Outputs saved to: ~/Documents/ASD2CSV/output (macOS/Linux) or Documents\ASD2CSV\output (Windows)

import os
import shutil
import threading
import time
import webbrowser
import tempfile
from pathlib import Path

from flask import Flask, render_template, request, jsonify

from asd_reader import ASDSpec
from csv_merger import merge_csv_files


# ----------------------------
# Paths (Professional defaults)
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent

# Always save outputs to the user's Documents folder
APP_DOCS_DIR = Path.home() / "Documents" / "ASD2CSV"
OUTPUT_DIR = APP_DOCS_DIR / "output"

# Temporary uploads go to system temp (keeps Documents clean)
TEMP_DIR = Path(tempfile.gettempdir()) / "ASD2CSV_temp"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


# ----------------------------
# Flask app
# ----------------------------
app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
)


# ----------------------------
# Helpers
# ----------------------------
def _safe_clear_temp() -> None:
    """Delete all temporary uploaded files/folders."""
    if not TEMP_DIR.exists():
        return
    for p in TEMP_DIR.iterdir():
        try:
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                shutil.rmtree(p)
        except Exception:
            # Best-effort cleanup only
            pass


def _open_browser_later(url: str, delay_sec: float = 1.2) -> None:
    """Open the default browser after the server starts (PyInstaller-safe)."""
    time.sleep(delay_sec)
    try:
        webbrowser.open(url)
    except Exception:
        pass


def _sanitize_filename(name: str) -> str:
    """
    Basic filename sanitizer to reduce issues with weird names.
    Keeps letters/numbers/._- and replaces others with underscore.
    """
    safe = []
    for ch in name:
        if ch.isalnum() or ch in "._-":
            safe.append(ch)
        else:
            safe.append("_")
    out = "".join(safe).strip("._")
    return out or "file"


# ----------------------------
# Routes
# ----------------------------
@app.get("/")
def index():
    return render_template("index.html")


@app.get("/output-info")
def output_info():
    return jsonify({"output_folder": str(OUTPUT_DIR.resolve())})


@app.post("/convert")
def convert_asd_files():
    """
    Convert one or more ASD files to CSV.
    - Uploads saved temporarily to TEMP_DIR
    - ONLY CSVs are written to OUTPUT_DIR
    - TEMP_DIR is cleaned after processing
    """
    _safe_clear_temp()

    files = request.files.getlist("asd_files")
    if not files:
        return jsonify({"ok": False, "message": "No ASD files selected."}), 400

    converted = 0
    failed = 0

    for f in files:
        original_name = (f.filename or "").strip()
        if not original_name:
            failed += 1
            continue

        # Save ASD to temp (never to output)
        safe_name = _sanitize_filename(original_name)
        temp_asd_path = TEMP_DIR / safe_name
        try:
            f.save(str(temp_asd_path))
        except Exception:
            failed += 1
            continue

        # Output CSV (CSV only in Documents/ASD2CSV/output)
        out_csv_name = Path(safe_name).stem + ".csv"
        out_csv_path = OUTPUT_DIR / out_csv_name

        try:
            spec = ASDSpec(str(temp_asd_path))
            spec.to_csv(str(out_csv_path))
            converted += 1
        except Exception:
            failed += 1

    _safe_clear_temp()

    msg = f"{converted} file(s) processed successfully."
    if failed:
        msg += f" ({failed} file(s) failed.)"

    return jsonify({"ok": True, "message": msg})


@app.post("/merge")
def merge_csv():
    """
    Merge 2+ CSV files into one CSV:
      Documents/ASD2CSV/output/merged_spectra.csv

    Uploads are saved temporarily to TEMP_DIR, then deleted.
    """
    _safe_clear_temp()

    files = request.files.getlist("csv_files")
    if not files or len(files) < 2:
        return jsonify({"ok": False, "message": "Select at least 2 CSV files to merge."}), 400

    saved_paths = []
    for f in files:
        original_name = (f.filename or "").strip()
        if not original_name:
            continue

        safe_name = _sanitize_filename(original_name)
        temp_csv_path = TEMP_DIR / safe_name
        try:
            f.save(str(temp_csv_path))
            saved_paths.append(str(temp_csv_path))
        except Exception:
            # skip bad file
            pass

    if len(saved_paths) < 2:
        _safe_clear_temp()
        return jsonify({"ok": False, "message": "Select at least 2 valid CSV files to merge."}), 400

    out_merged_path = OUTPUT_DIR / "merged_spectra.csv"
    try:
        merge_csv_files(saved_paths, str(out_merged_path))
    except Exception as e:
        _safe_clear_temp()
        return jsonify({"ok": False, "message": f"Merge failed: {e}"}), 400

    _safe_clear_temp()
    return jsonify({"ok": True, "message": f"{len(saved_paths)} file(s) merged successfully."})


# ----------------------------
# Entrypoint
# ----------------------------
if __name__ == "__main__":
    # If port 5000 is used on your system, change it here:
    port = 5000
    url = f"http://127.0.0.1:{port}"

    threading.Thread(target=_open_browser_later, args=(url,), daemon=True).start()
    app.run(host="127.0.0.1", port=port, debug=False)
