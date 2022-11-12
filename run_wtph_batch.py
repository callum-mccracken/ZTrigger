"""
Run WriteTagProbeHistos, the nice way :)
"""
import os
import getpass
import constants as c
from run_numbers import RUN_NUMBERS
from wtph_input_configs import format_input_configs

ntupv = c.NTUPLE_VERSION

# ensure that input configs have the propper naming scheme
format_input_configs()

# assuming run configs were generated with these modules,
# they must already have the right naming scheme

# First, some paths and such:
if not os.path.exists(c.WTPH_OUTPUT_DIR):
    os.mkdir(c.WTPH_OUTPUT_DIR)
if not os.path.exists(c.WTPH_JOB_AREA):
    os.mkdir(c.WTPH_JOB_AREA)

input_configs = os.listdir(c.WTPH_INPUT_CONF_DIR)

# job parameters like time limit and slurm account are set in constants module

# Do we really need these? I don't think so!
# mc_campaigns = {
#     2018: 'mc16e',
#     2017: 'mc16d',
#     2016: 'mc16a',
#     2015: 'mc16a',  # yes this is supposed to be the same as 2016
# }

# name of bash script that will submit all batch jobs
submit_file = os.path.join(c.WTPH_JOB_AREA, "submitAllWTPH.sh")
if os.path.exists(submit_file):
    os.remove(submit_file)

pw = getpass.getpass("Please enter your grid password:")
cwd = os.getcwd()

# setup stuff for individual scripts
HEADER = "#!/bin/bash\n"
SETUP = f"""lsetup rucio
    echo {pw} | voms-proxy-init -voms atlas
    cd {c.MTPPP_ROOT}
    asetup {c.RELEASE}
    source */setup.sh
    mkdir -p ${c.WTPH_OUTPUT_DIR}
    cd {os.path.join(c.MTPPP_ROOT, "run")}\n"""

# stuff we'll write into the master script to run at the end
main_file_lines = []

# For each year, systematic, and period, make a script to run WTPH
for year in c.YEARS:
    for syst in c.VARIATIONS:
        for period in RUN_NUMBERS[year]:
            # find input configs, guaranteed to exist from earlier code
            data_input_file = os.path.join(
                c.WTPH_INPUT_CONF_DIR, f"data_{year}_{period}.conf")
            mc_input_file = os.path.join(
                c.WTPH_INPUT_CONF_DIR, f"{year}_{period}_Zmumu.conf")

            # find run configs
            for trigs in ["SingleMuonTriggers", "MultiLegTriggers"]:
                run_configs = os.listdir(
                    os.path.join(c.WTPH_RUN_CONF_DIR, trigs))
                print(year, period, syst, trigs)

                run_config = "MuonProbes_" + trigs + \
                    f"_{syst}_{year}_{period}.conf"
                assert run_config in run_configs
                run_conf_dir = os.path.join(c.WTPH_RUN_CONF_DIR, trigs)
                run_config = os.path.join(run_conf_dir, run_config)

                # output files we'll write to
                data_output_file = os.path.join(
                    c.WTPH_OUTPUT_DIR,
                    f"data{year}_{period}_{syst}_{ntupv}_{trigs}.root")
                mc_output_file = os.path.join(
                    c.WTPH_OUTPUT_DIR,
                    f"mc{year}_{period}_{syst}_{ntupv}_{trigs}.root")

                # write the bash scripts that runs WTPH
                data_job_file = os.path.join(
                    c.WTPH_JOB_AREA, f"data{year}-{period}-{syst}-{trigs}.sh")
                with open(data_job_file, "w", encoding="utf-8") as jfile:
                    jfile.write(HEADER + SETUP + "WriteTagProbeHistos" +
                        f" -i {data_input_file} -h {c.WTPH_2D_HISTO_CONF}" +
                        f" -r {run_config} -o {data_output_file}")
                mc_job_file = os.path.join(
                    c.WTPH_JOB_AREA, f"mc{year}-{period}-{syst}-{trigs}.sh")
                with open(mc_job_file, "w", encoding="utf-8") as jfile:
                    jfile.write(HEADER + SETUP + "WriteTagProbeHistos" +
                        f" -i {mc_input_file} -h {c.WTPH_2D_HISTO_CONF}" +
                        f" -r {run_config} -o {mc_output_file}")

                # make the ATLAS-formatted job files as required for Cedar
                data_atlfile = os.path.join(
                    c.WTPH_JOB_AREA,
                    f"atlas-data{year}-{period}-{syst}-{trigs}.sh")
                # this is the command that makes the atlas-formatted file
                os.system(
                    f'batchScript "source {data_job_file}" -O {data_atlfile}')

                mc_atlfile = os.path.join(
                    c.WTPH_JOB_AREA,
                    f"atlas-mc{year}-{period}-{syst}-{trigs}.sh")
                os.system(
                    f'batchScript "source {mc_job_file}" -O {mc_atlfile}')

                main_file_lines += [
                    f"echo 'Submitting {data_atlfile}'",
                    f"cd {c.WTPH_SUBMIT_AREA}",
                    f"sbatch --account {c.ACCOUNT} --time {c.TIME} " +
                    f"--mail-user {c.MAIL_USER} --mail-type {c.MAIL_TYPE} "+
                    f"{data_atlfile}",
                    f"cd {cwd}",
                    f"echo 'Submitting {mc_atlfile}'",
                    f"cd {c.WTPH_SUBMIT_AREA}",
                    f"sbatch --account {c.ACCOUNT} --time {c.TIME} " +
                    f"--mail-user {c.MAIL_USER} --mail-type {c.MAIL_TYPE} "+
                    f"{mc_atlfile}",
                    f"cd {cwd}"]

with open(submit_file, "a", encoding="utf-8") as subfile:
    subfile.writelines(main_file_lines)

print("\033[0;32mNow running all jobs! \033[0m")
os.system(f"source {submit_file}")
