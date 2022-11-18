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
            for data_mc in ["data", "mc"]:
                assert c.WTPH_INPUT_CONF_FMT[data_mc].format(
                    year=year, period=period) in input_configs

def replace_16_20():
    """
    Replace mc16 with mc20.
    Really we should fix CreateInputConfigs,
    but changes get merged so damn slow.
    """
    for year in c.YEARS:
        for period in RUN_NUMBERS[year]:
            for data_mc in ["data", "mc"]:
                config = c.WTPH_INPUT_CONF_FMT[data_mc].format(
                    year=year, period=period)
                config_path = os.path.join(c.WTPH_INPUT_CONF_DIR, config)
                with open(config_path, "r") as config_file:
                    text = config_file.read()
                text = text.replace("mc16", "mc20")
                with open(config_path, "w") as config_file:
                    config_file.write(text)


def merge_two(config_path_1, config_path_2, output_path):
    """
    Merge two input config files, e.g. two data files of the same period.

    Currently this doesn't preserve info from comments, maybe implement later.
    """

    # get lines from files
    with open(config_path_1, "r") as conf1:
        conf1_lines = conf1.readlines()
    with open(config_path_2, "r") as conf2:
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
        "# " + config_path_1,
        "# " + config_path_2,
        "############################################",
        "#InputFiles:"] + inputfiles +\
        ["#Good run Lists to be applied:"] + grls +\
        ["#Pile-up reweighting lumicalc files:"] + prw_data +\
        ["#Pile-up reweighting config files:"] + prw_mc

    with open(output_path, "w") as outfile:
        outfile.writelines(new_lines)
    print("wrote", output_path)


def merge(config_filenames, output_path):
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
            data_filename = c.WTPH_INPUT_CONF_FMT["data"].format(
                year=year, period=period)
            data_filepath = os.path.join(c.WTPH_INPUT_CONF_DIR, data_filename)
            # we will never have files with this exact format auto-generated
            if os.path.exists(data_filepath):
                os.remove(data_filepath)
            if data_filename not in input_configs:
                # try looking for a single file with year_period_
                data_matches = [
                    f for f in input_configs
                    if f.startswith("data_{year}_{period}".format(
                        year=year, period=period))]
                if data_matches == []:
                    # try looking for AllYear config
                    data_matches = [
                        f for f in input_configs
                        if f.startswith("data_{year}_AllYear".format(
                            year=year))]
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
                        if f.startswith("data_{year}_{period}".format(
                            year=year, period=period))]
                    # merge all the configs for that period into one
                    merge(data_matches, data_filepath)

            # same vibe with mc things
            mc_filename = c.WTPH_INPUT_CONF_FMT["mc"].format(
                year=year, period=period)
            mc_filepath = os.path.join(c.WTPH_INPUT_CONF_DIR, mc_filename)
            # we will never have files with this exact format auto-generated
            if os.path.exists(mc_filepath):
                os.remove(mc_filepath)
            if mc_filename not in input_configs:
                # try looking for a single file with year_period_
                mc_matches = [
                    f for f in input_configs
                    if f.startswith("{year}_{period}_Zmumu".format(
                        year=year, period=period))]
                if mc_matches == []:
                    # try looking a year-long config
                    mc_matches = [
                        f for f in input_configs
                        if f.startswith("{year}_Zmumu".format(
                            year=year))]
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
                        if f.startswith("{year}_{period}_Zmumu".format(
                            year=year, period=period))]
                    # merge all the configs for that period into one
                    merge(mc_matches, mc_filepath)

    check_formatted()
    replace_16_20()

