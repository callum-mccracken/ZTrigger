"""
Run WriteTagProbeHistos, the nice way :)
"""
from __future__ import print_function
import getpass
import os
import constants as c
from run_numbers import RUN_NUMBERS
from wtph_input_configs import format_input_configs

NTUPV = c.NTUPLE_VERSION  # to make lines shorter later

# ensure that input configs have the propper naming scheme
format_input_configs()

# assuming run configs were generated with these modules,
# they must already have the right naming scheme

# First, some paths and such:
if not os.path.exists(c.WTPH_OUTPUT_DIR):
    os.mkdir(c.WTPH_OUTPUT_DIR)
if not os.path.exists(c.WTPH_JOB_AREA):
    os.mkdir(c.WTPH_JOB_AREA)

INPUT_CONFIGS = os.listdir(c.WTPH_INPUT_CONF_DIR)

# job parameters like time limit and slurm account are set in constants module

# Do we really need these? I don't think so!
# mc_campaigns = {
#     2018: 'mc16e',
#     2017: 'mc16d',
#     2016: 'mc16a',
#     2015: 'mc16a',  # yes this is supposed to be the same as 2016
# }

# name of bash script that will submit all batch jobs
SUBMIT_FILE = os.path.join(c.WTPH_JOB_AREA, "submitAllWTPH.sh")
if os.path.exists(SUBMIT_FILE):
    os.remove(SUBMIT_FILE)

PW = getpass.getpass("Please enter your grid password:")
CWD = os.getcwd()

# setup stuff for individual scripts
HEADER = "#!/bin/bash\n"
SETUP = 'lsetup "rucio SL7Python2"\n' +\
    "echo " + PW + " | voms-proxy-init -voms atlas\n" +\
    "cd " + os.path.join(c.MTPPP_ROOT, "build") + "\n" +\
    "asetup\n" +\
    "source */setup.sh\n" +\
    "mkdir -p " + c.WTPH_OUTPUT_DIR + "\n" +\
    "cd " + os.path.join(c.MTPPP_ROOT, "run") + "\n"

# stuff we'll write into the master script to run at the end
MAIN_FILE_LINES = []

# For each year, systematic, and period, make a script to run WTPH
for year in c.YEARS:
    for syst in c.VARIATIONS:
        for prd in RUN_NUMBERS[year]:
            for trigs in ["SingleMuonTriggers", "MultiLegTriggers"]:
                # find run configs
                run_configs = os.listdir(
                    os.path.join(c.WTPH_RUN_CONF_DIR, trigs))
                run_config = "MuonProbes_" + trigs + \
                    "_{syst}_{year}_{prd}.conf".format(
                        syst=syst, year=year, prd=prd)
                assert run_config in run_configs
                run_conf_dir = os.path.join(c.WTPH_RUN_CONF_DIR, trigs)
                run_config = os.path.join(run_conf_dir, run_config)

                for data_mc in ["data", "mc"]:
                    # find input configs, guaranteed to exist from earlier code
                    input_file = os.path.join(
                        c.WTPH_INPUT_CONF_DIR,
                        c.WTPH_INPUT_CONF_FMT[data_mc].format(
                            year=year, period=prd))

                    # output file we'll write to
                    output_file = os.path.join(
                        c.WTPH_OUTPUT_DIR,
                        data_mc + str(year) + "_" + prd + "_" +\
                        syst + "_" + NTUPV + "_" + trigs + ".root")

                    # write the bash scripts that runs WTPH
                    job_file = os.path.join(
                        c.WTPH_JOB_AREA,
                        "{data_mc}{year}-{prd}-{syst}-{trigs}.sh".format(
                            data_mc=data_mc, year=year, prd=prd, syst=syst,
                            trigs=trigs))
                    with open(job_file, "w") as jfile:
                        jfile.write(
                            HEADER + SETUP + "WriteTagProbeHistos" +
                            " -i "+ input_file +\
                            " -h " + c.WTPH_2D_HISTO_CONF +\
                            " -r " + run_config +\
                            " -o " + output_file)

                    # make the ATLAS-formatted job files as required for Cedar
                    atlfile = os.path.join(
                        c.WTPH_JOB_AREA,
                        "atlas-{data_mc}{year}-{prd}-{syst}-{trigs}.sh".format(
                            data_mc=data_mc, year=year, prd=prd, syst=syst,
                            trigs=trigs))

                    MAIN_FILE_LINES += [
                        # batchScript = command to make the atlas-format file
                        'batchScript "source ' + job_file + '" -O '+ atlfile,
                        "echo 'Submitting " + atlfile + "'",
                        "cd " + c.WTPH_SUBMIT_AREA,
                        "sbatch" +\
                        " --account " + c.ACCOUNT +\
                        " --time " + c.TIME +\
                        " --mail-user " + c.MAIL_USER +\
                        " --mail-type " + c.MAIL_TYPE + " "+ atlfile,
                        "cd " + CWD]

with open(SUBMIT_FILE, "w") as subfile:
    subfile.write("\n".join(MAIN_FILE_LINES))

print("To run all jobs: source " + SUBMIT_FILE)
