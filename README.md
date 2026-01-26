# ASD2CSV

[![Release](https://img.shields.io/github/v/release/YOUR_USERNAME/YOUR_REPO)](https://github.com/YOUR_USERNAME/YOUR_REPO/releases)


ASD2CSV is a cross-platform desktop application for converting **ASD spectrometer `.asd` files to `.csv` format** and **merging multiple CSV spectra into a single file** using a clean, browser-based graphical interface.

The app runs locally on your machine and opens automatically in your default web browser.

---

## Features

- Convert one or more `.asd` files to `.csv`
- Batch conversion of entire folders
- Merge multiple `.csv` files into one combined file
- Automatic output folder creation
- Clean and minimal graphical interface
- macOS and Windows installers

---

## Installation

### macOS
1. Download `ASD2CSV.dmg` from the **Releases** page
2. Open it
3. Drag **ASD2CSV** into **Applications**
4. Launch the app — your browser will open automatically

### Windows
1. Download `ASD2CSV_Setup.exe` from the **Releases** page
2. Run the installer
3. Launch ASD2CSV from the Start Menu

---

## Usage

### Convert ASD Files
1. Click **Convert ASD file(s) to CSV**
2. Select one or more `.asd` files
3. Converted `.csv` files will be saved in the `output/` folder

### Merge CSV Files
1. Click **Merge CSV Files**
2. Select two or more `.csv` files
3. A merged file named `merged_spectra.csv` will be created in the `output/` folder

---

## Development Setup

### Requirements
- Python 3.9+
- pip

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate    # Windows

pip install -r requirements.txt
python asd2csv_app.py
```

---

## Project Structure

```text
asd2csv_app/
├── asd2csv_app.py
├── asd_reader.py
├── csv_merger.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
├── assets/
│   └── icon.png
├── LICENSE
└── README.md
```

---

## License

This project is licensed under the **Apache License 2.0**.

You may:
- Use the software commercially
- Modify and distribute the source code
- Include it in proprietary or open-source projects

You must:
- Include the original license in redistributions
- State significant changes made to the code

See the full license text in the [`LICENSE`](LICENSE) file.

---

## Credits

ASD file parsing and conversion logic is based on publicly available ASD binary format specifications and adapted for this application.

Developed and maintained by **Vahid Khosravi**.
