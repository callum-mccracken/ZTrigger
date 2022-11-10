"""Module for creating basic config files."""
import os
import constants as c

def make_basic_config(match_filename, year, period, single: bool):
    """Make a basic config file."""
    # get the right template
    if single:
        basic_template_file_path = c.SM_BASIC_CONFIG_TEMPLATE
    else:
        basic_template_file_path = c.ML_BASIC_CONFIG_TEMPLATE

    # get its text
    with open(basic_template_file_path, "r", encoding="utf-8") as basic_file:
        basic_template_text = basic_file.read()

    # input detector regions file path
    basic_template_text = basic_template_text.replace(
        "DETECTOR_REGIONS_FILE_HERE",
        os.path.join(c.TOP_LEVEL_DIR, c.DETECTOR_REGIONS_SAVE_PATH))

    # use given matches file
    basic_file_text = basic_template_text.replace(
        "MATCHES_FILE_HERE",
        os.path.join(c.TOP_LEVEL_DIR, match_filename))

    # get filename and save
    fmt = c.SM_BASIC_CONFIG_PATH_FMT if single else c.ML_BASIC_CONFIG_PATH_FMT
    basic_filename = fmt.format(year=year, period=period)
    with open(basic_filename, "w", encoding="utf-8") as basic_file:
        basic_file.write(basic_file_text)
    return basic_filename
