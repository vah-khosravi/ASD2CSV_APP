import os
import sys
from asd_reader import ASDSpec

def convert_one(asd_path: str, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(asd_path))[0]
    out_csv = os.path.join(out_dir, f"{base}.csv")

    spec = ASDSpec(asd_path)
    spec.to_csv(out_csv)

    return out_csv

def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("  python cli_convert.py <asd_file_or_folder> <output_folder>")
        sys.exit(1)

    input_path = sys.argv[1]
    out_dir = sys.argv[2]

    if os.path.isfile(input_path):
        if not input_path.lower().endswith(".asd"):
            print("Error: input file must be .asd")
            sys.exit(1)

        out_csv = convert_one(input_path, out_dir)
        print(f"Converted 1 file -> {out_csv}")
        return

    if os.path.isdir(input_path):
        asd_files = [
            os.path.join(input_path, f)
            for f in os.listdir(input_path)
            if f.lower().endswith(".asd")
        ]

        if not asd_files:
            print("No .asd files found in folder.")
            sys.exit(1)

        for f in asd_files:
            convert_one(f, out_dir)

        print(f"Converted {len(asd_files)} file(s) -> {out_dir}")
        return

    print("Error: input path not found.")
    sys.exit(1)

if __name__ == "__main__":
    main()
