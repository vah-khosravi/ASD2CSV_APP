import os
import sys
import pandas as pd

def merge_csv(input_folder, output_file):
    csv_files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(".csv") and f != os.path.basename(output_file)
    ]

    if len(csv_files) < 2:
        print("Need at least 2 CSV files to merge.")
        return

    merged_data = []
    wavelengths = None

    for file in csv_files:
        path = os.path.join(input_folder, file)
        df = pd.read_csv(path)

        if wavelengths is None:
            wavelengths = df.iloc[:, 0].values
            header = ["Filename"] + list(wavelengths)

        reflectance = df.iloc[:, 1].values
        merged_data.append([file] + list(reflectance))

    final_df = pd.DataFrame(merged_data, columns=header)
    final_df.to_csv(output_file, index=False)

    print(f"Merged {len(csv_files)} files → {output_file}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python cli_merge.py <csv_folder> <output_csv>")
        return

    folder = sys.argv[1]
    output = sys.argv[2]

    if not os.path.isdir(folder):
        print("Folder not found")
        return

    merge_csv(folder, output)

if __name__ == "__main__":
    main()
