import os
import shutil
from constants import SINGLE_MUON_DIR, MULTI_LEG_DIR

def create_dirs():
    """Get directories ready for config files."""
    for directory in [SINGLE_MUON_DIR, MULTI_LEG_DIR]:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.mkdir(directory)

