![Release](https://img.shields.io/github/v/release/vah-khosravi/ASD2CSV_APP)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)
![LICENSE](https://img.shields.io/github/license/vah-khosravi/ASD2CSV_APP)
![Stars](https://img.shields.io/github/stars/vah-khosravi/ASD2CSV_APP?style=social)

# ASD2CSV

ASD2CSV is a cross-platform desktop application for converting **ASD spectrometer `.asd` files to `.csv` format** and **merging multiple CSV files into a single file** using a clean, browser-based graphical interface.

The app runs locally on your machine and opens in your default web browser.

---

## Features

- Convert one or more `.asd` files to `.csv`
- Batch conversion of entire folders
- Merge multiple `.csv` files into one combined file
- Automatic `output/` folder creation
- Clean and minimal graphical interface
- macOS and Windows installers (via GitHub Releases)

---

## Installation

### macOS (Installer)
1. Download `ASD2CSV.dmg` from the **Releases** page
2. Open it
3. Drag **ASD2CSV** into **Applications**
4. Launch the app — your browser should open automatically

### Windows (Installer)
1. Download `ASD2CSV_Setup.exe` from the **Releases** page
2. Run the installer
3. Launch ASD2CSV from the Start Menu

---

## Run from Source (CLI / Developer Mode)

This mode is for users who want to run the application directly from the source code (no `.dmg` / `.exe`).

### 1) Clone the repository
```bash
git clone https://github.com/vah-khosravi/ASD2CSV_APP.git
cd ASD2CSV_APP
```

### 2) Create and activate a virtual environment

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows (CMD)
```bat
py -m venv .venv
.venv\Scripts\activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Run the GUI app (Flask local server)
```bash
python asd2csv_app.py
```

Open in your browser:
```
http://127.0.0.1:5000
```

---

## Usage

### Convert ASD Files
1. In the app, click **Convert ASD file(s) to CSV**
2. Select one or more `.asd` files
3. Converted `.csv` files will be saved in the `output/` folder

### Merge CSV Files
1. Click **Merge CSV Files**
2. Select **two or more** `.csv` files
3. A merged file named `merged_spectra.csv` will be created in the `output/` folder

---

## Command-line (Optional)

If you prefer scripts without the browser UI:

### Convert one ASD file
```bash
python asd_reader.py Data/Spectrum00001.asd output/Spectrum00001.csv
```

### Batch convert all ASD files in a folder
```bash
python batch_convert.py Data output
```

### Merge all CSV files in a folder
```bash
python csv_merger.py output
```

---

## Project Structure

```text
ASD2CSV_APP/
├── asd2csv_app.py
├── asd_reader.py
├── csv_merger.py
├── batch_convert.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
├── assets/
│   ├── icon.png
│   ├── icon.icns
│   └── icon.ico
├── LICENSE
└── README.md
```

---

## License

This project is licensed under the **Apache License 2.0**.

See the full license text in the `LICENSE` file.

---

## Cite This Software

If you use **ASD2CSV** in academic work, publications, or research, please cite it as follows:

### APA
> Khosravi, V. (2026). *ASD2CSV: A cross-platform tool for converting ASD spectrometer files to CSV format*. GitHub. https://github.com/vah-khosravi/ASD2CSV_APP

### BibTeX
```bibtex
@software{Khosravi_ASD2CSV_2026,
  author  = {Khosravi, Vahid},
  title   = {ASD2CSV: A cross-platform tool for converting ASD spectrometer files to CSV format},
  year    = {2026},
  url     = {https://github.com/vah-khosravi/ASD2CSV_APP},
  note    = {Version 1.0.0}
}
```

## Credits

ASD file parsing and conversion logic is based on publicly available ASD binary format specifications and adapted for this application.

Developed and maintained by **Vahid**.