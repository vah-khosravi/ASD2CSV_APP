import os
import csv


def merge_csv_files(csv_paths, output_csv_path):
    """
    Merge multiple 2-column spectra CSV files into one CSV.

    Expected input format for each CSV:
        wavelength_nm,<spectrum_name>
        350.0,0.123
        351.0,0.124
        ...

    Output format (wide):
        Filename,<wl1>,<wl2>,...,<wlN>
        Spectrum1.csv,val1,val2,...,valN
        Spectrum2.csv,val1,val2,...,valN
        ...

    Args:
        csv_paths (list[str]): paths to CSV files to merge (must be >= 2)
        output_csv_path (str): where to save merged_spectra.csv

    Returns:
        int: number of files merged
    """
    if not csv_paths or len(csv_paths) < 2:
        raise ValueError("Select at least 2 CSV files to merge.")

    # --- Read wavelengths from first file ---
    first = csv_paths[0]
    with open(first, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header or len(header) < 2:
            raise ValueError(f"Invalid CSV format (needs 2 columns): {first}")

        wavelengths = []
        values = []

        for row in reader:
            if len(row) < 2:
                continue
            wavelengths.append(row[0])
            values.append(row[1])

    # Prepare output header: Filename + wavelengths
    out_header = ["Filename"] + wavelengths
    merged_rows = []

    # Add first file row
    merged_rows.append([os.path.basename(first)] + values)

    # --- Read remaining files and validate wavelength alignment ---
    for path in csv_paths[1:]:
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            hdr = next(reader, None)
            if not hdr or len(hdr) < 2:
                raise ValueError(f"Invalid CSV format (needs 2 columns): {path}")

            wl_check = []
            val_list = []

            for row in reader:
                if len(row) < 2:
                    continue
                wl_check.append(row[0])
                val_list.append(row[1])

        # Validate same number + same wavelength sequence
        if wl_check != wavelengths:
            raise ValueError(
                f"Wavelength mismatch in file: {os.path.basename(path)}. "
                "All CSVs must have the same wavelength column."
            )

        merged_rows.append([os.path.basename(path)] + val_list)

    # --- Write merged output ---
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(out_header)
        writer.writerows(merged_rows)

    return len(csv_paths)
