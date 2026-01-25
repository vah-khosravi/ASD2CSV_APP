import struct
import time
import os
from collections import OrderedDict


# ----------------------------
# Lookup dictionaries
# ----------------------------

DATA_TYPE_DICT = {
    0: "Raw",
    1: "Reflectance",
    2: "Radiance",
    3: "No_Units",
    4: "Irradiance",
    5: "QI",
    6: "Transmittance",
    7: "Unknown",
    8: "Absorbance"
}

TYPE_ABBREV_DICT = {
    "Raw": "Raw",
    "Reflectance": "Refl",
    "Reference": "Ref"
}

DATA_FORMAT_DICT = {
    0: "numeric",
    1: "integer",
    2: "double",
    3: "Unknown"
}

INSTRUMENT_DICT = {
    0: "Unknown",
    1: "PSII",
    2: "LSVNIR",
    3: "FSVNIR",
    4: "FSFR",
    5: "FSNIR",
    6: "CHEM",
    7: "FSFR Unattended"
}


# ----------------------------
# ASD Reader Class
# ----------------------------

class ASDSpec:
    """
    Reads a binary ASD file and converts it to spectral data
    """

    def __init__(self, asd_file_path: str):
        if not os.path.exists(asd_file_path):
            raise FileNotFoundError(f"ASD file not found: {asd_file_path}")

        self.filepath = asd_file_path
        self.filename = os.path.basename(asd_file_path)

        with open(asd_file_path, "rb") as f:
            self._read_header(f)
            self._read_spectrum(f)

    # ----------------------------
    # Internal binary readers
    # ----------------------------

    def _read_header(self, f):
        f.seek(3)
        self.comments = f.read(157).decode(errors="ignore").strip("\x00")

        f.seek(182)
        seconds = struct.unpack("<L", f.read(4))[0]
        self.acquisition_time = time.ctime(seconds)

        f.seek(186)
        self.data_type = DATA_TYPE_DICT.get(struct.unpack("<B", f.read(1))[0], "Unknown")

        f.seek(204)
        self.num_channels = struct.unpack("<h", f.read(2))[0]

        f.seek(191)
        self.wavelength_start = struct.unpack("<f", f.read(4))[0]

        f.seek(195)
        self.wavelength_step = struct.unpack("<f", f.read(4))[0]

        self.wavelengths = [
            self.wavelength_start + i * self.wavelength_step
            for i in range(self.num_channels)
        ]

        f.seek(199)
        self.data_format_code = struct.unpack("<B", f.read(1))[0]

    def _read_spectrum(self, f):
        f.seek(484)

        if self.data_format_code == 0:
            fmt = f"<{self.num_channels}f"
            byte_size = 4
        elif self.data_format_code == 1:
            fmt = f"<{self.num_channels}l"
            byte_size = 4
        elif self.data_format_code == 2:
            fmt = f"<{self.num_channels}d"
            byte_size = 8
        else:
            raise RuntimeError("Unsupported ASD data format")

        raw_bytes = f.read(self.num_channels * byte_size)
        self.values = struct.unpack(fmt, raw_bytes)

    # ----------------------------
    # Public API
    # ----------------------------

    def to_csv(self, output_csv_path: str):
        """
        Writes wavelength + spectrum values to CSV
        """

        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

        column_name = os.path.splitext(self.filename)[0]

        with open(output_csv_path, "w", encoding="utf-8") as csv_file:
            csv_file.write("wavelength_nm," + column_name + "\n")
            for wl, val in zip(self.wavelengths, self.values):
                csv_file.write(f"{wl},{val}\n")
__all__ = ["ASDSpec"]
