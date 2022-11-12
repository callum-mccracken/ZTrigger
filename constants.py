"""
Module for storing constants,
like the list of variation names and template file paths.
"""

import os

NTUPLE_VERSION = "v66.3.0"
USER = os.getenv("USER")

# stuff for slurm
TIME = "24:00:00"  # time limit for batch jobs
ACCOUNT = "ctb-stelzer"  # slurm account
RELEASE = "AthAnalysis,21.2.196"  # ATLAS software release you set up
MAIL_USER = "your-email-here@example.com"  # what to use for job-related emails
MAIL_TYPE = "ALL"  # how many emails do you want? BEGIN END FAIL REQUEUE ALL

# stuff for looping over
YEARS = [2015, 2016, 2017, 2018]
VARIATIONS = [
    "nominal", "dphill", "mll",
    "muneg", "mupos", "noIP", "nvtx_dw", "nvtx_up", "ptdw", "ptup",
    "isoPflowLoose_VarRad", "isoPflowTight_VarRad",
    "isoLoose_VarRad", "isoTight_VarRad"]
WORKING_POINTS = ["Medium", "Loose", "Tight", "HighPt"]
DETECTOR_REGIONS = ["All", "noCrack", "Barrel", "Endcap"]

# where we are now, relative to MuonTPPostProcessing
ZTRIGGER_DIR = "MuonTPPostProcessing/RunConf/ZTrigger/"

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
SM_VAR_CONFIG_PATH_FMT = os.path.join(
    SINGLE_MUON_DIR,
    "MuonProbes_SingleMuonTriggers_{variation}_{year}_{period}.conf")

ML_BASIC_CONFIG_PATH_FMT = os.path.join(
    MULTI_LEG_DIR, "BasicConfigZMuon_{year}_{period}.conf")
ML_MATCHES_CONFIG_PATH_FMT = os.path.join(
    MULTI_LEG_DIR, "MatchesForZmumuMuon_{year}_{period}.conf")
ML_VAR_CONFIG_PATH_FMT = os.path.join(
    MULTI_LEG_DIR,
    "MuonProbes_MultiLegTriggers_{variation}_{year}_{period}.conf")

# Useful paths
MTPPP_ROOT = os.path.realpath("../../../../../")
MTPPP_DATA_PATH = os.path.join(
    MTPPP_ROOT, "MuonTPPostProcessing/MuonTPPostProcessing/data")
# where to store output from WTPH
WTPH_OUTPUT_DIR = os.path.join(MTPPP_ROOT, "output")
# where job scripts will be written
WTPH_JOB_AREA = os.path.join(WTPH_OUTPUT_DIR, "WTPHJobFiles/")
# where you submit your batch jobs from (cannot be in /home/)
WTPH_SUBMIT_AREA = os.path.join("/scratch/", USER)
# where the input conigs are read from
WTPH_INPUT_CONF_DIR = os.path.join(
    MTPPP_DATA_PATH, "InputConfTRIUMF_"+NTUPLE_VERSION)
# which histo config to use
WTPH_2D_HISTO_CONF = os.path.join(
    MTPPP_DATA_PATH, "HistoConf/ZTrigger/SingleMuonTriggers/2D_hist.conf")
# where the run configs are stored
WTPH_RUN_CONF_DIR = os.path.join(
    MTPPP_DATA_PATH, "RunConf/ZTrigger/")
# how the input configs should be named by the time WTPH scripts are written
WTPH_INPUT_CONF_FMT = {
    "data": "data_{year}_{period}.conf",
    "mc": "{year}_{period}_Zmumu.conf"}
