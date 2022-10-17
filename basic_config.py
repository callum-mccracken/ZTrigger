import os
from constants import\
    DETECTOR_REGIONS_SAVE_PATH, SM_BASIC_CONFIG_PATH_FMT,\
    ML_BASIC_CONFIG_TEMPLATE, SM_BASIC_CONFIG_TEMPLATE, TOP_LEVEL_DIR,\
    ML_BASIC_CONFIG_PATH_FMT

def make_basic_config(match_filename, year, period, single: bool):
    # get the right template
    if single:
        basic_template_file_path = SM_BASIC_CONFIG_TEMPLATE
    else:
        basic_template_file_path = ML_BASIC_CONFIG_TEMPLATE

    # get its text
    with open(basic_template_file_path, "r", encoding="utf-8") as basic_file:
        basic_template_text = basic_file.read()

    # input detector regions file path
    basic_template_text = basic_template_text.replace(
        "DETECTOR_REGIONS_FILE_HERE",
        os.path.join(TOP_LEVEL_DIR, DETECTOR_REGIONS_SAVE_PATH))

    # use given matches file
    basic_file_text = basic_template_text.replace(
        "MATCHES_FILE_HERE",
        os.path.join(TOP_LEVEL_DIR, match_filename))

    # get filename and save
    fmt = SM_BASIC_CONFIG_PATH_FMT if single else ML_BASIC_CONFIG_PATH_FMT
    basic_filename = fmt.format(year=year, period=period)
    with open(basic_filename, "w", encoding="utf-8") as basic_file:
        basic_file.write(basic_file_text)
    return basic_filename
