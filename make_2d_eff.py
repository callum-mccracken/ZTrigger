"""
This script makes 2D efficiency plots and scale factor info.

Purpose:
--------

- Creating phi vs. eta efficiency plots (data and mc separately)
  - in ROOT files in format necessary for acceptance by TriggerScaleFactorTool
- if --makeSFPlots=True: Creating phi vs. eta scale factor (data/mc) plots
- if --printSFValues=True: Printing inclusive SF values and their systematics
- **See SF tutorial for details of what efficiencies/SFs are.**

Inputs
------

The inputs for this script are the outputs of the
WriteTagProbeHistos (WTPH) command of the MuonTPPostProcessing package
(ntuples containing histograms 2D efficiency histograms).

To run this script, the user needs to have produced ntuples
using WriteTagProbeHistos for each systematic, for data and MC individually.
Those files should follow the naming convention:
[data/mc][year or mc production][period if data]_[systematic_[date].root
e.g. data18B_isoTight_Oct20.root
e.g. mc16e_Oct20.root (this file would be the nominal file)

If the user runs into problems accessing the files,
ROOT will complain about the file not being found.

Execution:
----------
(requires python 2!)

python 2Dsysts.py -d [input fils directory] -y [year] -p [period]
-r [region] -t [trigger] -q [quality] --[other options]

See the parser option lines below for more details about the other options.
The parser options also allow the user to use the batch script batch2DEff.sh
to run this script many times for different
years/periods/regions/triggers/qualities.
In this way, output ROOT files can, in one go,
be filled with all of the necessary plots.

Outputs:
--------

ROOT files containing 2D eta/phi efficiency plots,
for data and MC, for a number of systematics,
as well as total systematic and statistical uncertainty up/down plots.


(this file was originally created by Alec,
but there's no need to put copyright/edit info here, that's all in GitLab!)
"""
# Imports and Option Parser
from __future__ import print_function
import math
import optparse
import sys
import os
import logging
import itertools
from ROOT import *
import constants as c
from run_numbers import periods
from triggers import triggers_in_period

# TODO Need to be careful about period K 2017 nvtx systematic:
# TODO cut >/< 19 vertices for 2017 but >/< 25 for period K

# Suppresses basic info prints to terminal (used to shut up TEff constructor)
gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
# set up global style stuff
gROOT.LoadMacro('AtlasUtils.C')
gROOT.LoadMacro('AtlasLabels.C')
if gROOT.LoadMacro('AtlasStyle.C') > 0:
    SetAtlasStyle()

DEFAULT_IN_DIR = '../../../../../output/'
DEFAULT_OUT_DIR = '../../../../../run/'

RELEASE = 22
MC_NUMBER = "20" if RELEASE >= 22 else "16"  # not sure how actually defined
MC_CAMPAIGNS = {
    "15": MC_NUMBER+"a",
    "16": MC_NUMBER+"a",
    "17": MC_NUMBER+"d",
    "18": MC_NUMBER+"e",
}


def draw_hist(out_dir, title_prefix, hist, name):
    """Make a histogram."""
    canvas = TCanvas()
    canvas.SetTopMargin(0.1)
    canvas.SetBottomMargin(0.15)
    canvas.SetLeftMargin(0.15)
    canvas.SetRightMargin(0.15)
    gStyle.SetOptTitle(1)
    gStyle.SetOptStat(0)
    gStyle.SetPaintTextFormat(".3f")
    title = title_prefix + name
    hist.SetDirectory(0)
    hist.SetTitle(title)
    hist.SetTitleSize(0.02, "t")
    hist.SetMaximum(1.0)
    hist.SetMinimum(0.0)
    hist.Draw("COLZ TEXT")
    canvas.SaveAs(out_dir + title_prefix + name + ".png")
    canvas.Close()


def get_options():
    """Return a parser with all args we'll need for this script."""
    parser = optparse.OptionParser()
    # Save PNGs of 2D data/mc efficiency hists
    parser.add_option('--savePNGs', action='store_true', default=False,
                      dest='savePNGs')
    # Make separate ROOT file with SF hists
    parser.add_option('--makeSFPlots', action='store_true', default=False,
                      dest='makeSFPlots')
    # print SF values and systematics: **efficiency files not produced if True!**
    parser.add_option('--printSFValues', action='store_true', default=False,
                      dest='printSFValues')
    # debug mode - various print statements
    parser.add_option('--debug', action='store_true', default=False,
                      dest='debug')
    # path to directory where inputs (outputs of WTPH) are stored
    parser.add_option('-i', '--inDir', type='string',
                      default=DEFAULT_IN_DIR,
                      dest='inDir')
    # path to directory where you want the output(s) of the script to be stored
    parser.add_option('-o', '--outDir', type='string',
                      default=DEFAULT_OUT_DIR,
                      dest='outDir')
    # year: 2015, 2016, 2017, or 2018
    parser.add_option('-y', '--year', type='string', default=None,
                      dest='year')
    # data period letter: A,B,C, etc.
    parser.add_option('-p', '--period', type='string', default=None,
                      dest='period')
    # detector region: Endcap or Barrel (must be capitalized!)
    parser.add_option('-r', '--region', type='string', default=None,
                      dest='region')
    # trigger selection: HLT_{mu10, mu14, etc.}
    parser.add_option('-t', '--trigger', type='string', default=None,
                      dest='trigger')
    # trigger type selection, SingleMuonTriggers or MultiLegTriggers
    parser.add_option('-T', '--triggerType', type='string', default=None,
                      dest='triggerType')
    # muon quality working point: Medium, Loose, Tight, HighPt
    parser.add_option('-q', '--quality', type='string', default=None,
                      dest='quality')
    # T&P NTuple Version e.g. v65.3.2 or v064
    parser.add_option('-v', '--version', type='string', default=None,
                      dest='version')

    (options, _) = parser.parse_args()

    if options.debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    if options.year is None:
        print("using default year: 2018 (18)")
        options.year = "18"
    if options.period is None:
        print("using default period: B")
        options.period = "B"
    if options.region is None:
        print("using default region: Barrel")
        options.region = "Barrel"
    if options.triggerType is None:
        print("using defualt triggerType: SingleMuonTriggers")
        options.triggerType = "SingleMuonTriggers"
    if options.trigger is None:
        print("using defualt trigger: HLT_mu26_ivarmedium")
        options.trigger = "HLT_mu26_ivarmedium"
    if options.quality is None:
        print("using defualt quality: Medium")
        options.quality = "Medium"
    if options.version is None:
        print("using defualt ntuple version: v66.3.0")
        options.version = "v66.3.0"
    return options


def make_2d_eff_hists(year, period, region, trigger_type, trigger, quality,
                      version, input_dir, output_dir, make_sf_plots,
                      print_sf_values, debug, save_pngs):
    """Make 2D Efficiency histograms for all the given parameters."""
    print(year, period, quality, region, trigger_type)
    # Suppresses basic info prints to terminal (used to shut up TEff constructor)
    gROOT.ProcessLine("gErrorIgnoreLevel = 10000000;")

    # check year
    if year not in MC_CAMPAIGNS.keys():
        raise ValueError("Invalid year! Use one of", MC_CAMPAIGNS.keys())

    # check period
    number_year = int("20"+year)
    if period not in periods(number_year):
        raise ValueError("Invalid period! Use one of", periods(number_year))

    # check region
    if region not in c.DETECTOR_REGIONS:
        raise ValueError(
            "Invalid detector region! Use one of", c.DETECTOR_REGIONS)

    # check trigger_type
    if trigger_type not in c.TRIGGER_TYPES:
        raise ValueError(
            "Invalid trigger type! Use one of", c.TRIGGER_TYPES)

    # check trigger
    single = (trigger_type == "SingleMuonTriggers")
    if trigger not in triggers_in_period(single, number_year, period):
        raise ValueError(
            "Invalid detector region! Use one of", c.DETECTOR_REGIONS)

    # check quality working point
    if quality not in c.WORKING_POINTS:
        raise ValueError(
            "Invalid quality working point! Use one of", c.WORKING_POINTS)

    # show warning if you're running over another version
    if version != c.NTUPLE_VERSION:
        logging.warning("Version is not the same as in constants module!")

    # check input/output dirs exist
    if not os.path.exists(input_dir):
        raise ValueError("Input directory does not exist!", input_dir)
    if not os.path.exists(output_dir):
        raise ValueError("Output directory does not exist!", output_dir)

    assert isinstance(make_sf_plots, bool)
    assert isinstance(print_sf_values, bool)
    assert isinstance(debug, bool)
    assert isinstance(save_pngs, bool)

    montecarlo = MC_CAMPAIGNS[year]

    # Load input files
    logging.debug("Looking for input files in directory: %s", input_dir)
    input_files = os.listdir(input_dir)
    logging.debug("Found %s files in %s", len(input_files), input_dir)

    # get probe / match hists for each variation
    probe_hists = {"data": {}, "mc": {}}
    match_hists = {"data": {}, "mc": {}}
    # and calculate efficiencies / make histograms
    effs = {"data": {}, "mc": {}}
    hists = {"data": {}, "mc": {}}

    for d_mc in ["data", "mc"]:

        # Creating dictionaries with (histname, hist) tuples
        # Directories where probe and match hists are located
        # (identically name in every WTPH output)
        dir_fmt = "ZmumuTPMerged/"+quality+"MuonProbes_"+\
            region.capitalize()+"/OC/"+trigger+"/"
        probe_dir = dir_fmt+"Probe/"
        match_dir = dir_fmt+"Match/"

        # Hists to look for in the above directories
        # (also identically named) in every WTPH output)
        hist_fmt = str(
            quality+"MuonProbes_"+region.capitalize()+"_OC_"+
            trigger+"_{}_etaphi_fine_"+region.capitalize())
        probe_hist = hist_fmt.format("Probe")
        match_hist = hist_fmt.format("Match")

        logging.debug(
            "Will look in directory,\n"+probe_dir+
            "\nFor hist,\n"+probe_hist)

        for var in c.VARIATIONS:
            print(d_mc, var)
            var_conf_name = d_mc+"20"+str(year)+"_"+"_".join(
                [period, var, version, trigger_type])+".root"
            var_conf = os.path.join(input_dir, var_conf_name)
            if not os.path.exists(var_conf):
                raise ValueError("File not found:", var_conf)
           # open file
            var_file = TFile(var_conf)
            # get probe hist, raise error if not found
            probe_branch = os.path.join(probe_dir, probe_hist)
            probe_hists[d_mc][var] = var_file.Get(probe_branch)
            print(type(probe_hists[d_mc][var]))
            if not probe_hists[d_mc][var]:
                raise ValueError(
                    "Couldn't find {}. Does this really exist in {}?\n".format(
                        probe_branch, var_file.GetName()))
            # get match hist, raise error if not found
            match_branch = os.path.join(match_dir, match_hist)
            match_hists[d_mc][var] = var_file.Get(match_branch)
            if not match_hists[d_mc][var]:
                raise ValueError(
                    "Couldn't find {}. Does this really exist in {}?\n".format(
                        match_branch, var_file.GetName()))
            logging.debug("Got "+d_mc+" probe & match hists for "+var)

            # Make TEff object to do stat errors properly
            effs[d_mc][var] = TEfficiency(
                match_hists[d_mc][var], probe_hists[d_mc][var])

            # Make empty TH2 which will be filled with TEff bin values
            # (+/- errors if needed) down below
            hists[d_mc][var] = probe_hists[d_mc][var].Clone()
            hists[d_mc][var].Reset()

    # Setting up data systematic, statistical variation histograms
    # for data
    data_probe_nominal = probe_hists["data"]["nominal"]

    data_syst_up = data_probe_nominal.Clone('dSystUp')
    data_syst_up.Reset()
    data_syst_dw = data_probe_nominal.Clone('dSystDw')
    data_syst_dw.Reset()
    data_stat_up = data_probe_nominal.Clone('dStatUp')
    data_stat_up.Reset()
    data_stat_dw = data_probe_nominal.Clone('dStatDw')
    data_stat_dw.Reset()
    # isoEnv = isolation envelope
    hists["data"]["isoEnv"] = data_probe_nominal.Clone('isoEnv')
    hists["data"]["isoEnv"].Reset()

    # MC:
    mc_probe_nominal = probe_hists["mc"]["nominal"]
    mc_syst_up = mc_probe_nominal.Clone('mcSystUp')
    mc_syst_up.Reset()
    mc_syst_dw = mc_probe_nominal.Clone('mcSystDw')
    mc_syst_dw.Reset()
    mc_stat_up = mc_probe_nominal.Clone('mcStatUp')
    mc_stat_up.Reset()
    mc_stat_dw = mc_probe_nominal.Clone('mcStatDw')
    mc_stat_dw.Reset()
    hists["mc"]["isoEnv"] = mc_probe_nominal.Clone('isoEnv')
    hists["mc"]["isoEnv"].Reset()

    # Number of x- and y-bins - will be used many times
    # assumed to be the same for data and mc
    xbins = data_probe_nominal.GetNbinsX()
    ybins = data_probe_nominal.GetNbinsY()

    # Initialize stat/syst up/down
    if make_sf_plots:
        logging.debug("makeSFPlots = True! Will initialize SF hists")
        sf_hists = {}
        for k in hists["data"]:
            sf_hists[k] = hists["data"][k].Clone()
            sf_hists[k].Reset()
        sf_stat_up = data_stat_up.Clone()
        sf_stat_dw = data_stat_dw.Clone()
        sf_syst_up = data_syst_up.Clone()
        sf_syst_dw = data_syst_dw.Clone()

    # Initlaize SF value variables and obtain inclusive stat uncertainty
    if print_sf_values:
        logging.debug(
            "printSFValues = True! Will keep track of SF values for each syst")
        # To get inclusive SF values,
        # need to add probes and matches across all bins
        n_data_matches = {}
        n_data_probes = {}
        n_mc_matches = {}
        n_mc_probes = {}
        sf_values = {}
        for k in hists["data"]:
            n_data_matches[k] = 0
            n_data_probes[k] = 0
            n_mc_matches[k] = 0
            n_mc_probes[k] = 0
            sf_values[k] = 0
        sf_values["isoEnv"] = 0
        sf_values["TotSyst"] = 0

        # Inclusive SF stat uncertainty using 1-bin copies of data/mc hists
        #Data inclusive eff
        data_match_nominal = match_hists["data"]["nominal"]

        data_match_1_bin = data_match_nominal.Clone()
        data_match_1_bin.Rebin2D(xbins, ybins)
        data_probe_1_bin = data_probe_nominal.Clone()
        data_probe_1_bin.Rebin2D(xbins, ybins)
        data_eff_1_bin = TEfficiency(data_match_1_bin, data_probe_1_bin)

        data_1_bin = hists["data"]["nominal"].Clone()
        data_1_bin.Reset()
        data_1_bin.Rebin2D(xbins, ybins)
        global_bin = data_eff_1_bin.GetGlobalBin(1, 1)
        data_eff = data_eff_1_bin.GetEfficiency(global_bin)
        data_stat_err = data_eff_1_bin.GetEfficiencyErrorUp(global_bin)

        #MC inclusive eff
        mc_match_nominal = match_hists["mc"]["nominal"]
        mc_match_1_bin = mc_match_nominal.Clone()
        mc_match_1_bin.Rebin2D(xbins, ybins)
        mc_probe_1_bin = mc_probe_nominal.Clone()
        mc_probe_1_bin.Rebin2D(xbins, ybins)
        mc_eff_1_bin = TEfficiency(mc_match_1_bin, mc_probe_1_bin)

        mc_1_bin = hists["mc"]["nominal"].Clone()
        mc_1_bin.Reset()
        mc_1_bin.Rebin2D(xbins, ybins)
        mc_eff = mc_eff_1_bin.GetEfficiency(global_bin)
        mc_stat_err = mc_eff_1_bin.GetEfficiencyErrorUp(global_bin)

        # Error propagation:
        # err_sf = sf*(err_data_eff/data_eff + err_mc_eff/mc_eff)
        # TODO: is this the right way to deal with divide-by-zero errors?
        if mc_eff == 0:
            logging.warning("MC efficiency is zero -- skipping!")
            return
        else:
            scale_factor = data_eff / mc_eff
        sfstaterr = 0 if mc_eff == 0 or data_eff == 0 else (scale_factor * (
            data_stat_err / data_eff + mc_stat_err / mc_eff))

    # Looping through each bin of each histogram
    # to grab the nominal efficiency and the systematic variations
    logging.debug('Now starting loop over bins...')
    for i in range(1, xbins + 2):
        for j in range(1, ybins + 2):
            # Debugging particular bin issues
            # print("Bin : ("+str(i)+","+str(j)+")")

            # Global bin # to used w GetEfficiency()
            # and GetEfficiencyErrorUp/Low()
            global_bin = effs["data"]["nominal"].GetGlobalBin(i, j)

            # Getting data, MC nominal efficiency and up/down stat bin errors:
            dnom = effs["data"]["nominal"].GetEfficiency(global_bin)
            dstatup = effs["data"]["nominal"].GetEfficiencyErrorUp(global_bin)
            dstatdw = effs["data"]["nominal"].GetEfficiencyErrorLow(global_bin)
            mcnom = effs["mc"]["nominal"].GetEfficiency(global_bin)
            mcstatup = effs["mc"]["nominal"].GetEfficiencyErrorUp(global_bin)
            mcstatdw = effs["mc"]["nominal"].GetEfficiencyErrorLow(global_bin)

            # Fill nominal + statUp/statDw data, MC efficiency TH2's
            hists["data"]["nominal"].SetBinContent(i, j, dnom)
            hists["mc"]["nominal"].SetBinContent(i, j, mcnom)
            data_stat_up.SetBinContent(i, j, dnom + dstatup)
            mc_stat_up.SetBinContent(i, j, mcnom + mcstatup)
            data_stat_dw.SetBinContent(i, j, dnom - dstatdw)
            mc_stat_dw.SetBinContent(i, j, mcnom - dstatdw)

            # Error propagation for SF stat up/down hists, in each bin
            if make_sf_plots:
                if mcnom != 0:
                    sfbinerrup = (dnom/mcnom) * (dstatup/dnom + mcstatup/mcnom)
                    sf_stat_up.SetBinContent(i, j, dnom/mcnom + sfbinerrup)
                    sfbinerrdw = (dnom/mcnom) * (dstatdw/dnom + mcstatdw/mcnom)
                    sf_stat_dw.SetBinContent(i, j, dnom/mcnom - sfbinerrdw)
                else:
                    sf_stat_up.SetBinContent(i, j, 0)
                    sf_stat_dw.SetBinContent(i, j, 0)

            # Getting data, MC up/down systematic bin errors
            # Ints to keep track of systematic variations summed in quadrature:
            dsyst_tot = 0
            mcsyst_tot = 0

            # Isolation envelope systematic for the bin:
            # Data
            dsyst_tight = effs[
                "data"]["isoTight_VarRad"].GetEfficiency(global_bin)
            dsyst_tight_pflow = effs[
                "data"]["isoPflowTight_VarRad"].GetEfficiency(global_bin)
            if abs(dnom - dsyst_tight) > abs(dnom - dsyst_tight_pflow):
                dsyst_iso = dnom - dsyst_tight
                hists["data"]["isoEnv"].SetBinContent(i, j, dsyst_tight)
            if abs(dnom - dsyst_tight) <= abs(dnom - dsyst_tight_pflow):
                dsyst_iso = dnom - dsyst_tight_pflow
                hists["data"]["isoEnv"].SetBinContent(i, j, dsyst_tight_pflow)
            # Add iso syst in quadrature to total syst bin error
            dsyst_tot += (dsyst_iso**2)

            # MC
            mcsyst_tight = effs[
                "mc"]["isoTight_VarRad"].GetEfficiency(global_bin)
            mcsyst_tight_pflow = effs[
                "mc"]["isoPflowTight_VarRad"].GetEfficiency(global_bin)
            # If tight systematic larger than TTO systematic
            if abs(mcnom - mcsyst_tight) > abs(mcnom - mcsyst_tight_pflow):
                mcsyst_iso = mcnom - mcsyst_tight
                hists["mc"]["isoEnv"].SetBinContent(i, j, mcsyst_tight)
                #SF inclusive isoEnv value
                if print_sf_values:
                    n_data_matches["isoEnv"] += match_hists["data"][
                        "isoTight_VarRad"].GetBinContent(i, j)
                    n_data_probes["isoEnv"] += probe_hists["data"][
                        "isoTight_VarRad"].GetBinContent(i, j)
                    n_mc_matches["isoEnv"] += match_hists["mc"][
                        "isoTight_VarRad"].GetBinContent(i, j)
                    n_mc_probes["isoEnv"] += probe_hists["mc"][
                        "isoTight_VarRad"].GetBinContent(i, j)
            # If TTO systematic larger than tight systematic
            elif abs(mcnom - mcsyst_tight) <= abs(mcnom - mcsyst_tight_pflow):
                mcsyst_iso = mcnom - mcsyst_tight_pflow
                hists["mc"]["isoEnv"].SetBinContent(i, j, mcsyst_tight_pflow)
                # SF inclusive isoEnv value
                if print_sf_values:
                    n_data_matches["isoEnv"] += match_hists["data"][
                        "isoPflowTight_VarRad"].GetBinContent(i, j)
                    n_data_probes["isoEnv"] += probe_hists["data"][
                        "isoPflowTight_VarRad"].GetBinContent(i, j)
                    n_mc_matches["isoEnv"] += match_hists["mc"][
                        "isoPflowTight_VarRad"].GetBinContent(i, j)
                    n_mc_probes["isoEnv"] += probe_hists["mc"][
                        "isoPflowTight_VarRad"].GetBinContent(i, j)
            # Add iso syst in quadrature to total syst bin error
            mcsyst_tot += (mcsyst_iso**2)

            # Get non-isolation systematics for the bin:
            for k in hists["data"]:
                if ("nominal" not in k and "isoEnv" not in k):
                    #Data:
                    dsyst = effs["data"][k].GetEfficiency(global_bin)
                    hists["data"][k].SetBinContent(i, j, dsyst)
                    if not k.startswith("iso"):
                        dsyst_tot += ((dnom - dsyst)**2)
                    #MC:
                    mcsyst = effs["mc"][k].GetEfficiency(global_bin)
                    hists["mc"][k].SetBinContent(i, j, mcsyst)
                    if not k.startswith("iso"):
                        mcsyst_tot += ((mcnom - mcsyst)**2)
                # SF values
                if print_sf_values and "isoEnv" not in k:
                    n_data_matches[k] += match_hists[
                        "data"][k].GetBinContent(i, j)
                    n_data_probes[k] += probe_hists[
                        "data"][k].GetBinContent(i, j)
                    n_mc_matches[k] += match_hists[
                        "mc"][k].GetBinContent(i, j)
                    n_mc_probes[k] += probe_hists[
                        "mc"][k].GetBinContent(i, j)

            # Finally, set the bin content of the
            # Syst Up/Dw plots = nominal efficiency + total syst variation
            data_syst_up.SetBinContent(i, j, dnom + math.sqrt(dsyst_tot))
            data_syst_dw.SetBinContent(i, j, dnom - math.sqrt(dsyst_tot))
            mc_syst_up.SetBinContent(i, j, mcnom + math.sqrt(mcsyst_tot))
            mc_syst_dw.SetBinContent(i, j, mcnom - math.sqrt(mcsyst_tot))

            # Fill syst up/down plots
            if make_sf_plots:
                if mcnom != 0 and math.sqrt(mcsyst_tot) != 0:
                    sf_syst_up.SetBinContent(
                        i, j, (dnom + math.sqrt(dsyst_tot)) / (
                            mcnom + math.sqrt(mcsyst_tot)))
                    sf_syst_dw.SetBinContent(
                        i, j, (dnom - math.sqrt(dsyst_tot)) / (
                            mcnom - math.sqrt(mcsyst_tot)))
                else:
                    sf_syst_up.SetBinContent(i, j, 0)
                    sf_syst_dw.SetBinContent(i, j, 0)
                for k in hists["data"]:
                    sf_hists[k] = hists["data"][k].Clone()
                    sf_hists[k].Divide(hists["mc"][k])

    # If inclusive SF values requested,
    # get them by dividing total matches/probes for data and mc
    if print_sf_values:
        for k in hists["data"]:
            # TODO: is this the right way to deal with /0 errors?
            if n_data_probes[k] == 0 or n_mc_probes[k] == 0:
                sf_values[k] = 0
            else:
                sf_values[k] = (n_data_matches[k] / n_data_probes[k]) / (
                    n_mc_matches[k] / n_mc_probes[k])

    # Create/update systematics Efficiencies TFile
    # make efficiency ROOT files
    if debug:
        effs_filepath = os.path.join(output_dir, "debug.root")
        # test output file
    else:
        # Change ntuple version to match your inputs!
        # outfile named in format for SF tool
        effs_filepath = os.path.join(
            output_dir, 'muontrigger_sf_20%s_mc%s_%s.root' %
            (year, montecarlo, version))
    logging.info("Will output data, MC efficiencies to %s", effs_filepath)
    effs_file = TFile(effs_filepath, 'update')
    # Create directory
    # (trigger may or may not contain _RM, replace does nothing if not)
    dir_name = quality + "/Period" + period + "/" +\
        trigger.replace("_RM", "") + "/"

    logging.debug(" - Directory: %s", dir_name)
    effs_file.mkdir(dir_name)
    effs_file.cd(dir_name)
    # Put corresponding plots into working point directory
    #Data:
    hists["data"]["nominal"].Write("eff_etaphi_fine_%s_data_nominal" % (
        region.lower()), TObject.kOverwrite)
    data_syst_up.Write("eff_etaphi_fine_%s_data_syst_up" % (
        region.lower()), TObject.kOverwrite)
    data_syst_dw.Write("eff_etaphi_fine_%s_data_syst_down" % (
        region.lower()), TObject.kOverwrite)
    data_stat_up.Write("eff_etaphi_fine_%s_data_stat_up" % (
        region.lower()), TObject.kOverwrite)
    data_stat_dw.Write("eff_etaphi_fine_%s_data_stat_down" % (
        region.lower()), TObject.kOverwrite)
    for k in sorted(hists["data"].keys()):
        if k != "dnominal":
            hists["data"][k].Write("eff_etaphi_fine_%s_data_%s" % (
                region.lower(), k), TObject.kOverwrite)
    #MC:
    hists["mc"]["nominal"].Write("eff_etaphi_fine_%s_mc_nominal" % (
        region.lower()), TObject.kOverwrite)
    mc_syst_up.Write("eff_etaphi_fine_%s_mc_syst_up" % (
        region.lower()), TObject.kOverwrite)
    mc_syst_dw.Write("eff_etaphi_fine_%s_mc_syst_down" % (
        region.lower()), TObject.kOverwrite)
    mc_stat_up.Write("eff_etaphi_fine_%s_mc_stat_up" % (
        region.lower()), TObject.kOverwrite)
    mc_stat_dw.Write("eff_etaphi_fine_%s_mc_stat_down" % (
        region.lower()), TObject.kOverwrite)
    for k in sorted(hists["mc"].keys()):
        if k != "nominal":
            hists["mc"][k].Write("eff_etaphi_fine_%s_mc_%s" % (
                region.lower(), k), TObject.kOverwrite)

    # Save all data, mc (and SF, if SF plots made) hists as pngs
    if save_pngs:
        # Directory
        png_outdir = os.path.join(output_dir, "savePNGs_%s/" % (year))
        logging.info("savePNGs = True! Will save PNGs to: %s", png_outdir)
        if not os.path.exists(png_outdir):
            os.mkdir(png_outdir)
        # prefix for hist titles
        title_prefix = "%s_%s_%s_etaphi_fine_%s_" % (
            quality, period, trigger.replace("_RM", ""), region.lower())
        gROOT.SetBatch()
        # Data stat/syst up/down
        draw_hist(png_outdir, title_prefix, data_syst_up, "dataEff_syst_up")
        draw_hist(png_outdir, title_prefix, data_syst_dw, "dataEff_syst_dw")
        draw_hist(png_outdir, title_prefix, data_stat_up, "dataEff_stat_up")
        draw_hist(png_outdir, title_prefix, data_stat_dw, "dataEff_stat_dw")
        # MC stat/syst up/down
        draw_hist(png_outdir, title_prefix, mc_syst_up, "mcEff_syst_up")
        draw_hist(png_outdir, title_prefix, mc_syst_dw, "mcEff_syst_dw")
        draw_hist(png_outdir, title_prefix, mc_stat_up, "mcEff_stat_up")
        draw_hist(png_outdir, title_prefix, mc_stat_dw, "mcEff_stat_dw")
        # SF stat/syst up/down
        if make_sf_plots:
            draw_hist(png_outdir, title_prefix, sf_syst_up, "SF_syst_up")
            draw_hist(png_outdir, title_prefix, sf_syst_dw, "SF_syst_dw")
            draw_hist(png_outdir, title_prefix, sf_stat_up, "SF_stat_up")
            draw_hist(png_outdir, title_prefix, sf_stat_dw, "SF_stat_dw")
        # Everything else
        for k in hists["data"]:
            draw_hist(
                png_outdir, title_prefix,
                hists["data"][k], "dataEff_{}".format(k))
            draw_hist(
                png_outdir, title_prefix,
                hists["mc"][k], "mcEff_{}".format(k))
            if make_sf_plots:
                draw_hist(png_outdir, title_prefix, sf_hists[k], "SF_{}".format(k))

    # Create separate SF TFile
    if make_sf_plots:
        if debug:
            sf_filename = "debug_SF.root"
        else:
            sf_filename = "SFPlots_%s_%s.root" % (year, version)
        sf_filepath = os.path.join(output_dir, sf_filename)
        logging.info(" ---> Will output SFs to file %s", sf_filepath)
        sf_file = TFile(sf_filepath, 'update')
        dir_name = quality + "/Period" + period + "/" + trigger + "/"
        logging.debug(" - Directory: %s", dir_name)
        sf_file.mkdir(dir_name)
        sf_file.cd(dir_name)
        sf_hists["nominal"].Write("sf_%s_nominal" % (region.lower()))
        sf_syst_up.Write("sf_%s_syst_up" % (
            region.lower()), TObject.kOverwrite)
        sf_syst_dw.Write("sf_%s_syst_down" % (
            region.lower()), TObject.kOverwrite)
        sf_stat_up.Write("sf_%s_stat_up" % (
            region.lower()), TObject.kOverwrite)
        sf_stat_dw.Write("sf_%s_stat_down" % (
            region.lower()), TObject.kOverwrite)
        for k in sorted(sf_hists.keys()):
            if k != "nominal":
                sf_hists[k].Write("sf_%s_%s" % (
                    region.lower(), k), TObject.kOverwrite)

    # Print inclusive SF for nominal, systematic plots
    if print_sf_values:
        print("Scale Factor Values: " + ", ".join([
            trigger, region, quality, year, period]))
        placeholder = 0
        print("{:<15} {:<15} {:<15}".format('Systematic', 'Value', '% Diff'))
        print("{:<15} {:<15} {:<15} {:<15}".format(
            "nominal", round(sf_values["nominal"], 5),
            "N/A", "Stat Error: " + str(sfstaterr)))
        for k, sf_val in sorted(sf_values.items()):
            if (k != "nominal" and k != "TotSyst"):
                placeholder += (sf_val - sf_values["nominal"])**2
                sf_rounded = round(sf_val, 5)
                pct_diff = -1 if sf_values["nominal"] == 0 else round((
                    sf_val - sf_values["nominal"]) / sf_values["nominal"],
                    5) * 100
                print("{:<15} {:<15} {:<15}".format(
                    k, sf_rounded, pct_diff))
        sf_values["TotSyst"] = sf_values["nominal"] + math.sqrt(placeholder)
        tot_sf_rounded = round(sf_values["TotSyst"], 5)
        tot_pct_diff = -1 if sf_values["nominal"] == 0 else round(
            (sf_values["TotSyst"]-sf_values["nominal"]
            )/sf_values["nominal"], 5) * 100
        print(
            "{:<15} {:<15} {:<15}".format(
                "Total", tot_sf_rounded, tot_pct_diff))


def run_over_everything():
    """Run make_2d_eff_hists"""
    for trigger_type in c.TRIGGER_TYPES:
        single = (trigger_type == "SingleMuonTriggers")
        for number_year in c.YEARS:
            year = str(number_year)[2:]
            for period in periods(number_year):
                # for some reason only barrel and endcap seem to have run
                # (in wtph)
                for region in ["Barrel", "Endcap"]:
                    for trigger in triggers_in_period(single,
                                                      number_year,
                                                      period):
                        for quality in c.WORKING_POINTS:
                            version = c.NTUPLE_VERSION
                            input_dir = DEFAULT_IN_DIR
                            output_dir = DEFAULT_OUT_DIR
                            debug = False
                            make_sf_plots = True
                            print_sf_values = True
                            save_pngs = True
                            make_2d_eff_hists(
                                year, period, region, trigger_type, trigger,
                                quality, version, input_dir, output_dir,
                                make_sf_plots, print_sf_values, debug,
                                save_pngs)


def main():
    """Make 2D Efficiency Histograms."""

    run_all = True

    if run_all:
        run_over_everything()
    else:
        options = get_options()

        year = options.year
        period = options.period
        region = options.region
        trigger_type = options.triggerType
        trigger = options.trigger
        quality = options.quality
        version = options.version
        input_dir = options.inDir
        output_dir = options.outDir
        make_sf_plots = options.makeSFPlots
        print_sf_values = options.printSFValues
        debug = options.debug
        save_pngs = options.savePNGs

        make_2d_eff_hists(
            year, period, region, trigger_type, trigger, quality, version,
            input_dir, output_dir, make_sf_plots, print_sf_values, debug,
            save_pngs)


if __name__ == "__main__":
    main()
