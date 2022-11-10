"""Module for making matches configs."""

from triggers import get_matches_text
from constants import ML_MATCHES_TEMPLATE, SM_MATCHES_TEMPLATE,\
    SM_MATCHES_CONFIG_PATH_FMT, ML_MATCHES_CONFIG_PATH_FMT

def make_match_configs(year, period, single):
    """
    Make match configs.

    year: str, e.g. 2015
    period: str, e.g. B
    single: bool, true for single muon triggers, false for multi-leg
    """
    # get the right template file
    if single:
        matches_template_path = SM_MATCHES_TEMPLATE
    else:
        matches_template_path = ML_MATCHES_TEMPLATE

    # get template file text
    with open(matches_template_path, "r", encoding="utf-8") as matches_file:
        matches_template_text = matches_file.read()

    # put trigger match blocks here
    matches_file_text = matches_template_text.replace(
        "MATCHES_HERE", get_matches_text(
            single=single, year=year, period=period))

    # write output
    fmt = SM_MATCHES_CONFIG_PATH_FMT if single else ML_MATCHES_CONFIG_PATH_FMT
    matches_filename = fmt.format(year=year, period=period)
    with open(matches_filename, "w", encoding="utf-8") as match_file:
        match_file.write(matches_file_text)
    return matches_filename
