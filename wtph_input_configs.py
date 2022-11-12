"""Module for dealing with WTPH input configs."""
import os
import shutil

import constants as c
from run_numbers import RUN_NUMBERS


def check_formatted():
    """Check that input configs have correct naming scheme, break if not."""
    input_configs = os.listdir(c.WTPH_INPUT_CONF_DIR)
    for year in c.YEARS:
        for period in RUN_NUMBERS[year]:
            assert f"data_{year}_{period}.conf" in input_configs
            assert f"{year}_{period}_Zmumu.conf" in input_configs

def merge_two(config_path_1, config_path_2, output_path):
    """
    Merge two input config files, e.g. two data files of the same period.

    Currently this doesn't preserve info from comments, maybe implement later.
    """

    # get lines from files
    with open(config_path_1, "r", encoding="utf-8") as conf1:
        conf1_lines = conf1.readlines()
    with open(config_path_2, "r", encoding="utf-8") as conf2:
        conf2_lines = conf2.readlines()
    lines = conf1_lines + conf2_lines

    # get all lines of each type, as sets so they're unique
    inputfiles = list({l for l in lines if l.split()[0] == "Input"})
    grls = list({l for l in lines if l.split()[0] == "GRL"})
    prw_data = list({l for l in lines if l.split()[0] == "PRWDataFile"})
    prw_mc = list({l for l in lines if l.split()[0] == "PRWMCFile"})

    new_lines = [
        "############################################",
        "# This is the result of merging two files:",
        f"# {config_path_1}",
        f"# {config_path_2}",
        "############################################",
        "#InputFiles:"] + inputfiles +\
        ["#Good run Lists to be applied:"] + grls +\
        ["#Pile-up reweighting lumicalc files:"] + prw_data +\
        ["#Pile-up reweighting config files:"] + prw_mc

    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.writelines(new_lines)
    print("wrote", output_path)


def merge(config_filenames: list[str], output_path: str):
    """Merge a list of input configs."""
    if len(config_filenames) < 2:
        raise ValueError("Why are you trying to merge this list?")
    elif len(config_filenames) == 2:
        merge_two(
            os.path.join(c.WTPH_INPUT_CONF_DIR, config_filenames[0]),
            os.path.join(c.WTPH_INPUT_CONF_DIR, config_filenames[1]),
            output_path)
    else:
        merge(
            [merge(*config_filenames[0:2])] + config_filenames[2:],
            output_path)


def format_input_configs():
    """Ensure that a config exists for data or MC for all years and periods."""
    input_configs = os.listdir(c.WTPH_INPUT_CONF_DIR)
    for year in c.YEARS:
        for period in RUN_NUMBERS[year]:
            # first deal with data files
            data_filename = f"data_{year}_{period}.conf"
            data_filepath = os.path.join(c.WTPH_INPUT_CONF_DIR, data_filename)
            if data_filename not in input_configs:
                # try looking for a single file with year_period_
                data_matches = [
                    f for f in input_configs
                    if f.startswith(f"data_{year}_{period}")]
                if len(data_matches) == 0:
                    # try looking for AllYear config
                    data_matches = [
                        f for f in input_configs
                        if f.startswith(f"data_{year}_AllYear")]
                    assert len(data_matches) == 1
                    filepath = os.path.join(
                        c.WTPH_INPUT_CONF_DIR, data_matches[0])
                    shutil.copyfile(
                        filepath,
                        data_filepath)
                elif len(data_matches) == 1:
                    # if we found a single year_period file:
                    filepath = os.path.join(
                        c.WTPH_INPUT_CONF_DIR, data_matches[0])
                    shutil.copyfile(
                        filepath,
                        data_filepath)
                else:
                    # merge multiple year_period files
                    data_matches = [
                        f for f in input_configs
                        if f.startswith(f"data_{year}_{period}")]
                    # merge all the configs for that period into one
                    merge(data_matches, data_filepath)

            # same vibe with mc things
            mc_filename = f"{year}_{period}_Zmumu.conf"
            mc_filepath = os.path.join(c.WTPH_INPUT_CONF_DIR, mc_filename)
            if mc_filename not in input_configs:
                # try looking for a single file with year_period_
                mc_matches = [
                    f for f in input_configs
                    if f.startswith(f"{year}_{period}_Zmumu")]
                if len(mc_matches) == 0:
                    # try looking a year-long config
                    mc_matches = [
                        f for f in input_configs
                        if f.startswith(f"{year}_Zmumu")]
                    assert len(mc_matches) == 1
                    filepath = os.path.join(
                        c.WTPH_INPUT_CONF_DIR, mc_matches[0])
                    shutil.copyfile(
                        filepath,
                        mc_filepath)
                elif len(mc_matches) == 1:
                    # if we found a single year_period file:
                    filepath = os.path.join(
                        c.WTPH_INPUT_CONF_DIR, mc_matches[0])
                    shutil.copyfile(
                        filepath,
                        mc_filepath)
                else:
                    # merge multiple year_period files
                    mc_matches = [
                        f for f in input_configs
                        if f.startswith(f"{year}_{period}_Zmumu")]
                    # merge all the configs for that period into one
                    merge(mc_matches, mc_filepath)

    check_formatted()
