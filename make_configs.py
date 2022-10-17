"""
A script to show how I made run 2 configs.

Hopefully this will make it a little easier to do run 3 things?
"""
import constants
from nominal_config import make_nominal_config
from run_numbers import periods
from create_dirs import create_dirs
from basic_config import make_basic_config
from matches_config import make_match_configs
from variation_config import make_variation_config
from detector_regions_config import make_detector_regions_config

create_dirs()

# make detector regions file
make_detector_regions_config()

for year in constants.YEARS:
    for period in periods(year):
        # make trigger match files
        single_match_config = make_match_configs(year, period, single=True)
        multi_match_config = make_match_configs(year, period, single=False)

        # make basic config file
        single_basic_filename = make_basic_config(
            single_match_config, year, period, single=True)
        multi_basic_filename = make_basic_config(
            multi_match_config, year, period, single=False)

        # make nominal config
        single_nominal_config = make_nominal_config(
            single=True, year=year, period=period,
            basic_filename=single_basic_filename)
        multi_nominal_config = make_nominal_config(
            single=False, year=year, period=period,
            basic_filename=multi_basic_filename)

        for variation in constants.VARIATIONS:
            # make variation file
            single_var_filename = make_variation_config(
                single_nominal_config, variation, year, period, single=True)
            multi_var_filename = make_variation_config(
                multi_nominal_config, variation, year, period, single=False)
