import shutil
from constants import DETECTOR_REGION_TEMPLATE, DETECTOR_REGIONS_SAVE_PATH

def make_detector_regions_config():
    """Just copy for now, maybe we'll edit it later?"""
    shutil.copyfile(DETECTOR_REGION_TEMPLATE, DETECTOR_REGIONS_SAVE_PATH)

