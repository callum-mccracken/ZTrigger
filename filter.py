"""Module to filter ListDisk output"""
from __future__ import print_function
import os
from constants import MTPPP_ROOT

RSE = "CA-SFU-T2_LOCALGROUPDISK"
LIST_DISK_OUTPUT_DIR = os.path.join(MTPPP_ROOT, "run")
LIST_DISK_OUTPUT_FILE = os.path.join(
    LIST_DISK_OUTPUT_DIR, "CA-SFU-T2_LOCALGROUPDISK_2022-11-13_v66.3.0.txt")
TEMP_FILE_PATH = "temp.out"
FILTERED_OUTPUT_FILENAME = "filtered.txt"

def main():
    """Filter to only get the files we care about for SFs"""
    if not os.path.exists(LIST_DISK_OUTPUT_FILE):
        raise ValueError("Make sure you've provided the correct path!")

    with open(LIST_DISK_OUTPUT_FILE, "r+") as ld_output_file:
        lines = ld_output_file.readlines()

    filtered_lines = []
    for line in lines:
        # the actual line where we do the filtering
        if "Main" in line or ("Zmumu" in line and "Powheg" in line):
            line = line.replace('\n', '')
            # ensure the dataset actually exists
            cmd = "rucio list-datasets-rse " + RSE + " | grep " + line
            os.system(cmd + " > " + TEMP_FILE_PATH)
            with open(TEMP_FILE_PATH, 'r') as tmpfile:
                cmd_output = tmpfile.read()
            dataset_exists = line in str(cmd_output)
            if dataset_exists:
                print("Adding", line)
                filtered_lines.append(line)
            else:
                raise ValueError("File" + line + "does not exist!")
    # write filtered output
    out_path = os.path.join(LIST_DISK_OUTPUT_DIR, FILTERED_OUTPUT_FILENAME)
    with open(out_path, "w+") as filtered_file:
        filtered_file.writelines(filtered_lines)


if __name__ == "__main__":
    main()
