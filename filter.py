"""Module to filter ListDisk output"""
from __future__ import print_function
import os
from constants import MTPPP_ROOT

RSE = "CA-SFU-T2_LOCALGROUPDISK"
LIST_DISK_OUTPUT_DIR = os.path.join(MTPPP_ROOT, "run")
LIST_DISK_OUTPUT_FILE = os.path.join(
    LIST_DISK_OUTPUT_DIR, "CA-SFU-T2_LOCALGROUPDISK_2022-11-13_v66.3.0.txt")

def main():
    """Filter to only get the files we care about for SFs"""
    if not os.path.exists(LIST_DISK_OUTPUT_FILE):
        raise ValueError("Make sure you've provided the correct path!")

    with open(LIST_DISK_OUTPUT_FILE, "r+") as ld_output_file:
        lines = ld_output_file.readlines()

    filtered_lines = []
    for line in lines:
        if "Main" in line or ("Zmumu" in line and "Powheg" in line):
            filtered_lines.append(line)
            cmd = "rucio list-datasets-rse " + RSE + " | grep " + line
            cmd_output = os.popen(cmd).read()
            print(cmd_output)
            if line in cmd_output:
                print("Adding", line)
            else:
                raise ValueError("Files do not exist!")

    out_path = os.path.join(LIST_DISK_OUTPUT_DIR, "filtered.txt")
    with open(out_path, "w+") as filtered_file:
        filtered_file.writelines(filtered_lines)


if __name__ == "__main__":
    main()
