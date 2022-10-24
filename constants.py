import os

YEARS = [2015, 2016, 2017, 2018]

VARIATIONS = [
    "nominal", "dphill", "isoTight", "isoTightTrackOnly", "mll",
    "muneg", "mupos", "noIP", "nvtx_dw", "nvtx_up", "ptdw", "ptup"]

WORKING_POINTS = ["Medium", "Loose", "Tight", "HighPt"]

DETECTOR_REGIONS = ["All", "noCrack", "Barrel", "Endcap"]

# where we are now, relative to MuonTPPostProcessing
TOP_LEVEL_DIR = "MuonTPPostProcessing/RunConf/ZTrigger/"

# directory for storing single muon stuff, relative to TOP_LEVEL_DIR
SINGLE_MUON_DIR = "SingleMuonTriggers"
MULTI_LEG_DIR = "MultiLegTriggers"

# template files -- SM = Single Muon, ML = Multi Leg
DETECTOR_REGION_TEMPLATE = "templates/DetectorRegionsForZmumuReco.conf"
SM_BASIC_CONFIG_TEMPLATE = "templates/SM_BasicConfigZMuon.conf"
SM_NOMINAL_CONFIG_TEMPLATE = "templates/SM_nominal_template.conf"
SM_PRE_NOMINAL_CONFIG_TEMPLATE = "templates/SM_pre_nominal_template.conf"
SM_MATCHES_TEMPLATE = "templates/SM_MatchesForZmumuMuon.conf"
ML_BASIC_CONFIG_TEMPLATE = "templates/ML_BasicConfigZMuon.conf"
ML_NOMINAL_CONFIG_TEMPLATE = "templates/ML_nominal_template.conf"
ML_PRE_NOMINAL_CONFIG_TEMPLATE = "templates/ML_pre_nominal_template.conf"
ML_MATCHES_TEMPLATE = "templates/ML_MatchesForZmumuMuon.conf"

# spots to store output files, relative to top
DETECTOR_REGIONS_SAVE_PATH = os.path.join(
    SINGLE_MUON_DIR, os.path.basename(DETECTOR_REGION_TEMPLATE))
SM_BASIC_CONFIG_PATH_FMT = os.path.join(
    SINGLE_MUON_DIR, "BasicConfigZMuon_{year}_{period}.conf")
SM_MATCHES_CONFIG_PATH_FMT = os.path.join(
    SINGLE_MUON_DIR, "MatchesForZmumuMuon_{year}_{period}.conf")
SM_VARIATION_CONFIG_PATH_FMT = os.path.join(
    SINGLE_MUON_DIR, "MuonProbes_OC_{variation}_{year}_{period}.conf")

ML_BASIC_CONFIG_PATH_FMT = os.path.join(
    MULTI_LEG_DIR, "BasicConfigZMuon_{year}_{period}.conf")
ML_MATCHES_CONFIG_PATH_FMT = os.path.join(
    MULTI_LEG_DIR, "MatchesForZmumuMuon_{year}_{period}.conf")
ML_VARIATION_CONFIG_PATH_FMT = os.path.join(
    MULTI_LEG_DIR,
    "MuonProbes_LooseProbes_noProbeIP_{variation}_{year}_{period}.conf")
