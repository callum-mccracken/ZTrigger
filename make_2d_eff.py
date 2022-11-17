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
from ROOT import *
import constants as c

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
        logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

    if options.year is None:
        print("using default year: 2018")
        options.year = "2018"
    if options.period is None:
        print("using default period: B")
        options.period = "B"
    if options.region is None:
        print("using default region: Barrel")
        options.region = "Barrel"
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


def main():
    """Make 2D Efficiency Histograms."""
    options = get_options()

    year = options.year
    period = options.period
    region = options.region
    trigger = options.trigger
    quality = options.quality
    version = options.version
    input_dir = options.inDir

    trigger_type = "SingleMuonTriggers"  # TODO loop over single and multi

    # Load input files
    logging.debug("Looking for input files in directory: %s", input_dir)
    input_files = os.listdir(input_dir)
    print("Found", len(input_files), "wtph outputs in directory", input_dir)

    # for storing actual file data
    root_files = {
        "data": {},
        "mc": {}}

    for d_mc in ["data", "mc"]:
        root_files[d_mc][year] = {}
        root_files[d_mc][year][period] = {}
        period_files = [
            input_file for input_file in input_files
            if input_file.startswith(d_mc+str(year)+"_"+period)]
        for var in c.VARIATIONS:
            var_confs = [df for df in period_files if var in df]
            if len(var_confs) != 1:
                raise ValueError(
                    "Multiple variation configs found... Why?", var_confs)
            var_conf = os.path.join(options.inDir, var_confs[0])
            root_files[d_mc][year][period][var] = TFile(var_conf)

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
            "Will look in directory\n"+probe_dir+
            "\nFor hist\n"+probe_hist)

        # get probe / match hists for each variation
        probe_hists = {}
        match_hists = {}
        # and calculate efficiencies / make histograms
        effs = {}
        hists = {}
        for variation in c.VARIATIONS:
            # get associated file
            var_file = root_files[d_mc][year][period][variation]
            # get probe hist, raise error if not found
            probe_hists[d_mc][variation] = var_file.Get(
                probe_dir + "/" + probe_hist)
            if not probe_hists[d_mc][variation]:
                raise ValueError(
                    "Couldn't find {}. Does this really exist in {}?\n".format(
                        probe_dir + probe_hist, var_file.GetName()))
            # get match hist, raise error if not found
            match_hists[d_mc][variation] = var_file.Get(
                match_dir + "/" + match_hist)
            if not match_hists[d_mc][variation]:
                raise ValueError(
                    "Couldn't find {}. Does this really exist in {}?\n".format(
                        match_dir + match_hist, var_file.GetName()))
            logging.debug("Got "+d_mc+" probe & match hists for "+variation)

            # Make TEff object to do stat errors properly
            effs[d_mc][variation] = TEfficiency(
                match_hists[d_mc][variation], probe_hists[d_mc][variation])

            # Make empty TH2 which will be filled with TEff bin values
            # (+/- errors if needed) down below
            hists[d_mc][variation] = probe_hists[d_mc][variation].Clone()
            hists[d_mc][variation].Reset()

    # Setting up data systematic, statistical variation histograms
    # for data
    data_probe_nominal = probe_hists["data"]["nominal"]

    dSystUp = data_probe_nominal.Clone('dSystUp')
    dSystUp.Reset()
    dSystDw = data_probe_nominal.Clone('dSystDw')
    dSystDw.Reset()
    dStatUp = data_probe_nominal.Clone('dStatUp')
    dStatUp.Reset()
    dStatDw = data_probe_nominal.Clone('dStatDw')
    dStatDw.Reset()
    hists["data"]["IsoEnv"] = data_probe_nominal.Clone('IsoEnv')
    hists["data"]["IsoEnv"].Reset()

    # MC:
    mc_probe_nominal = probe_hists["mc"]["nominal"]
    mcSystUp = mc_probe_nominal.Clone('mcSystUp')
    mcSystUp.Reset()
    mcSystDw = mc_probe_nominal.Clone('mcSystDw')
    mcSystDw.Reset()
    mcStatUp = mc_probe_nominal.Clone('mcStatUp')
    mcStatUp.Reset()
    mcStatDw = mc_probe_nominal.Clone('mcStatDw')
    mcStatDw.Reset()
    hists["mc"]["IsoEnv"] = mc_probe_nominal.Clone('IsoEnv')
    hists["mc"]["IsoEnv"].Reset()

    # Number of x- and y-bins - will be used many times
    # assumed to be the same for data and mc
    xbins = data_probe_nominal.GetNbinsX()
    ybins = data_probe_nominal.GetNbinsY()

    # (If options.makeSFPlots): Initialize stat/syst up/down
    if options.makeSFPlots:
        logging.debug("makeSFPlots = True! Will initialize SF hists")
        sfHists = {}
        for k in hists["data"].keys():
            sfHists[k] = hists[k].Clone()
            sfHists[k].Reset()
        sfStatUp = dStatUp.Clone()
        sfStatDw = dStatDw.Clone()
        sfSystUp = dSystUp.Clone()
        sfSystDw = dSystDw.Clone()

    # (If options.printSFValues):
    # Initlaize SF value variables and obtain inclusive stat uncertainty
    if options.printSFValues:
        logging.debug(
            "printSFValues = True! Will keep track of SF values for each syst")
        # To get inclusive SF values,
        # need to add probes and matches across all bins
        nDataMatches = {}
        nDataProbes = {}
        nMCMatches = {}
        nMCProbes = {}
        sfValues = {}
        for k in hists["data"].keys():
            nDataMatches[k] = 0
            nDataProbes[k] = 0
            nMCMatches[k] = 0
            nMCProbes[k] = 0
            sfValues[k] = 0
        sfValues["IsoEnv"] = 0
        sfValues["TotSyst"] = 0

        # Inclusive SF stat uncertainty using 1-bin copies of data/mc hists
        #Data inclusive eff
        data_match_nominal = match_hists["data"]["nominal"]

        dM1bin = data_match_nominal.Clone()
        dM1bin.Rebin2D(xbins, ybins)
        dP1bin = data_probe_nominal.Clone()
        dP1bin.Rebin2D(xbins, ybins)
        dE1bin = TEfficiency(dM1bin, dP1bin)

        d1bin = hists["data"]["nominal"].Clone()
        d1bin.Reset()
        d1bin.Rebin2D(xbins, ybins)
        gbin = dE1bin.GetGlobalBin(1, 1)
        deff = dE1bin.GetEfficiency(gbin)
        dstaterr = dE1bin.GetEfficiencyErrorUp(gbin)

        #MC inclusive eff
        mc_match_nominal = match_hists["mc"]["nominal"]
        mcM1bin = mc_match_nominal.Clone()
        mcM1bin.Rebin2D(xbins, ybins)
        mcP1bin = mc_probe_nominal.Clone()
        mcP1bin.Rebin2D(xbins, ybins)
        mcE1bin = TEfficiency(mcM1bin, mcP1bin)

        mc1bin = hists["mc"]["nominal"].Clone()
        mc1bin.Reset()
        mc1bin.Rebin2D(xbins, ybins)
        mceff = mcE1bin.GetEfficiency(gbin)
        mcstaterr = mcE1bin.GetEfficiencyErrorUp(gbin)

        # Error propagation:
        # err_sf = sf*(err_data_eff/data_eff + err_mc_eff/mc_eff)
        sf = deff / mceff
        sfstaterr = (sf * (dstaterr / deff + mcstaterr / mceff))

    # Looping through each bin of each histogram
    # to grab the nominal efficiency and the systematic variations
    logging.debug('Now starting loop over bins...')
    for i in range(1, xbins + 2):
        for j in range(1, ybins + 2):
            # Debugging particular bin issues
            # print("Bin : ("+str(i)+","+str(j)+")")

            # Global bin # to used w GetEfficiency()
            # and GetEfficiencyErrorUp/Low()
            globalbin = effs["data"]["nominal"].GetGlobalBin(i, j)

            # Getting data, MC nominal efficiency and up/down stat bin errors:
            dnom = effs["data"]["nominal"].GetEfficiency(globalbin)
            dstatup = effs["data"]["nominal"].GetEfficiencyErrorUp(globalbin)
            dstatdw = effs["data"]["nominal"].GetEfficiencyErrorLow(globalbin)
            mcnom = effs["mc"]["nominal"].GetEfficiency(globalbin)
            mcstatup = effs["mc"]["nominal"].GetEfficiencyErrorUp(globalbin)
            mcstatdw = effs["mc"]["nominal"].GetEfficiencyErrorLow(globalbin)

            # Fill nominal + statUp/statDw data, MC efficiency TH2's
            hists["data"]["nominal"].SetBinContent(i, j, dnom)
            hists["mc"]["nominal"].SetBinContent(i, j, mcnom)
            dStatUp.SetBinContent(i, j, dnom + dstatup)
            mcStatUp.SetBinContent(i, j, mcnom + mcstatup)
            dStatDw.SetBinContent(i, j, dnom - dstatdw)
            mcStatDw.SetBinContent(i, j, mcnom - dstatdw)

            # Error propagation for SF stat up/down hists, in each bin
            if options.makeSFPlots:
                if mcnom != 0:
                    sfbinerrup = (dnom/mcnom) * (dstatup/dnom + mcstatup/mcnom)
                    sfStatUp.SetBinContent(i, j, dnom/mcnom + sfbinerrup)
                    sfbinerrdw = (dnom/mcnom) * (dstatdw/dnom + mcstatdw/mcnom)
                    sfStatDw.SetBinContent(i, j, dnom/mcnom - sfbinerrdw)
                else:
                    sfStatUp.SetBinContent(i, j, 0)
                    sfStatDw.SetBinContent(i, j, 0)

            # Getting data, MC up/down systematic bin errors
            # Ints to keep track of systematic variations summed in quadrature:
            dsyst_tot = 0
            mcsyst_tot = 0

            # Isolation envelope systematic for the bin:
            # Data
            dsyst_tight = effs["IsoTight"].GetEfficiency(globalbin)
            dsyst_tto = effs["IsoTTO"].GetEfficiency(globalbin)
            if abs(dnom - dsyst_tight) > abs(dnom - dsyst_tto):
                dsyst_iso = dnom - dsyst_tight
                hists["IsoEnv"].SetBinContent(i, j, dsyst_tight)
            if abs(dnom - dsyst_tight) <= abs(dnom - dsyst_tto):
                dsyst_iso = dnom - dsyst_tto
                hists["IsoEnv"].SetBinContent(i, j, dsyst_tto)
            # Add iso syst in quadrature to total syst bin error
            dsyst_tot += (dsyst_iso**2)

            # MC
            mcsyst_tight = effs["mc"]["IsoTight"].GetEfficiency(globalbin)
            mcsyst_tto = effs["mc"]["IsoTTO"].GetEfficiency(globalbin)
            # If tight systematic larger than TTO systematic
            if abs(mcnom - mcsyst_tight) > abs(mcnom - mcsyst_tto):
                mcsyst_iso = mcnom - mcsyst_tight
                hists["mc"]["IsoEnv"].SetBinContent(i, j, mcsyst_tight)
                #SF inclusive IsoEnv value (if options.printSFValues)
                if options.printSFValues:
                    nDataMatches["IsoEnv"] += match_hists[
                        "IsoTight"].GetBinContent(i, j)
                    nDataProbes["IsoEnv"] += probe_hists[
                        "IsoTight"].GetBinContent(i, j)
                    nMCMatches["IsoEnv"] += match_hists["mc"][
                        "IsoTight"].GetBinContent(i, j)
                    nMCProbes["IsoEnv"] += probe_hists["mc"][
                        "IsoTight"].GetBinContent(i, j)
            # If TTO systematic larger than tight systematic
            elif abs(mcnom - mcsyst_tight) <= abs(mcnom - mcsyst_tto):
                mcsyst_iso = mcnom - mcsyst_tto
                hists["mc"]["IsoEnv"].SetBinContent(i, j, mcsyst_tto)
                # SF inclusive IsoEnv value (if options.printSFValues)
                if options.printSFValues:
                    nDataMatches["IsoEnv"] += match_hists[
                        "IsoTTO"].GetBinContent(i, j)
                    nDataProbes["IsoEnv"] += probe_hists[
                        "IsoTTO"].GetBinContent(i, j)
                    nMCMatches["IsoEnv"] += match_hists["mc"][
                        "IsoTTO"].GetBinContent(i, j)
                    nMCProbes["IsoEnv"] += probe_hists["mc"][
                        "IsoTTO"].GetBinContent(i, j)
            # Add iso syst in quadrature to total syst bin error
            mcsyst_tot += (mcsyst_iso**2)

            # Get non-isolation systematics for the bin:
            for k in hists["data"].keys():
                if ("nominal" not in k and "IsoEnv" not in k):
                    #Data:
                    dsyst = effs["data"][k].GetEfficiency(globalbin)
                    hists["data"][k].SetBinContent(i, j, dsyst)
                    if "Iso" not in k:
                        dsyst_tot += ((dnom - dsyst)**2)
                    #MC:
                    mcsyst = effs["mc"][k].GetEfficiency(globalbin)
                    hists["mc"][k].SetBinContent(i, j, mcsyst)
                    if "Iso" not in k:
                        mcsyst_tot += ((mcnom - mcsyst)**2)
                # SF values (if options.makeSFPlots)
                if options.printSFValues and "IsoEnv" not in k:
                    nDataMatches[k] += match_hists["data"][k].GetBinContent(i, j)
                    nDataProbes[k] += probe_hists["data"][k].GetBinContent(i, j)
                    nMCMatches[k] += match_hists["mc"][k].GetBinContent(i, j)
                    nMCProbes[k] += probe_hists["mc"][k].GetBinContent(i, j)

            # Finally, set the bin content of the
            # Syst Up/Dw plots = nominal efficiency + total systematic variation
            dSystUp.SetBinContent(i, j, dnom + math.sqrt(dsyst_tot))
            dSystDw.SetBinContent(i, j, dnom - math.sqrt(dsyst_tot))
            mcSystUp.SetBinContent(i, j, mcnom + math.sqrt(mcsyst_tot))
            mcSystDw.SetBinContent(i, j, mcnom - math.sqrt(mcsyst_tot))

            # (If options.makeSFPlots): Fill syst up/down plots
            if options.makeSFPlots:
                if mcnom != 0 and math.sqrt(mcsyst_tot) != 0:
                    sfSystUp.SetBinContent(i, j, (dnom + math.sqrt(dsyst_tot)) / (
                        mcnom + math.sqrt(mcsyst_tot)))
                    sfSystDw.SetBinContent(i, j, (dnom - math.sqrt(dsyst_tot)) / (
                        mcnom - math.sqrt(mcsyst_tot)))
                else:
                    sfSystUp.SetBinContent(i, j, 0)
                    sfSystDw.SetBinContent(i, j, 0)
                for k in hists["data"].keys():
                    sfHists[k] = hists[k].Clone()
                    sfHists[k].Divide(hists["mc"][k])

    # If inclusive SF values requested,
    # get them by dividing total matches/probes for data and mc
    if options.printSFValues:
        for k in hists["data"].keys():
            sfValues[k] = (nDataMatches[k] / nDataProbes[k]) / (
                nMCMatches[k] / nMCProbes[k])

    # Create/update systematics Efficiencies TFile
    if year == '15':
        montecarlo = montecarlo.replace('_2015', '')
    elif year == '16':
        montecarlo = montecarlo.replace('_2016', '')

    # Do not make efficiency ROOT files if options.printSFValues == True
    if (not options.makeSFPlots and not options.printSFValues):
        if options.debug:
            logging.debug(
                "Will output data, MC efficiencies to file " +\
                options.outDir + "/debug.root")
            # test output file
            effs_file = TFile(options.outDir + '/debug.root', 'update')
        else:
            # Change ntuple version to match your inputs!
            print('\033[1;32m' + "INFO: " + '\033[0m' + "Will output data, MC " +
                "efficiencies to file " + options.outDir +
                "/muontrigger_sf_20%s_mc%s_%s.root" %
                (options.year.replace("20", ""), montecarlo, options.version))
            effs_file = TFile(
                options.outDir + '/muontrigger_sf_20%s_mc%s_%s.root' %
                (options.year.replace("20", ""), montecarlo, options.version),
                'update')  # outfile named in format for SF tool
        # Create directory
        if ("_RM" in options.trigger):
            dir_name = options.quality + "/Period" + options.period + "/" +\
                options.trigger.replace("_RM", "") + "/"
        else:
            dir_name = options.quality + "/Period" + options.period + "/" +\
                options.trigger + "/"
        if options.debug:
            print('\033[1;32m' + "DEBUG: " + '\033[0m' +
                " - Directory: " + dir_name)
        effs_file.mkdir(dir_name)
        effs_file.cd(dir_name)
        # Put corresponding plots into working point directory
        #Data:
        hists["data"]["nominal"].Write("eff_etaphi_fine_%s_data_nominal" % (
            options.region.lower()), TObject.kOverwrite)
        dSystUp.Write("eff_etaphi_fine_%s_data_syst_up" % (
            options.region.lower()), TObject.kOverwrite)
        dSystDw.Write("eff_etaphi_fine_%s_data_syst_down" % (
            options.region.lower()), TObject.kOverwrite)
        dStatUp.Write("eff_etaphi_fine_%s_data_stat_up" % (
            options.region.lower()), TObject.kOverwrite)
        dStatDw.Write("eff_etaphi_fine_%s_data_stat_down" % (
            options.region.lower()), TObject.kOverwrite)
        for k in sorted(hists.keys()):
            if (k != "dnominal"):
                hists[k].Write("eff_etaphi_fine_%s_data_%s" % (
                    options.region.lower(), k), TObject.kOverwrite)
        #MC:
        hists["mc"]["nominal"].Write("eff_etaphi_fine_%s_mc_nominal" % (
            options.region.lower()), TObject.kOverwrite)
        mcSystUp.Write("eff_etaphi_fine_%s_mc_syst_up" % (
            options.region.lower()), TObject.kOverwrite)
        mcSystDw.Write("eff_etaphi_fine_%s_mc_syst_down" % (
            options.region.lower()), TObject.kOverwrite)
        mcStatUp.Write("eff_etaphi_fine_%s_mc_stat_up" % (
            options.region.lower()), TObject.kOverwrite)
        mcStatDw.Write("eff_etaphi_fine_%s_mc_stat_down" % (
            options.region.lower()), TObject.kOverwrite)
        for k in sorted(hists["mc"].keys()):
            if (k != "nominal"):
                hists["mc"][k].Write("eff_etaphi_fine_%s_mc_%s" % (
                    options.region.lower(), k), TObject.kOverwrite)

    # Save all data, mc (and SF, if SF plots made) hists as pngs
    if options.savePNGs:
        # Directory
        outdir = "./savePNGs_%s/" % (options.year)
        logging.debug("savePNGs = True! Will save PNGs to: " + outdir)
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        # prefix for hist titles
        title_prefix = "%s_%s_%s_etaphi_fine_%s_" % (
            options.quality, options.period,
            options.trigger.replace("_RM", ""),
            options.region.lower())
        gROOT.SetBatch()
        # Data stat/syst up/down
        draw_hist(outdir, title_prefix, dSystUp, "dataEff_syst_up")
        draw_hist(outdir, title_prefix, dSystDw, "dataEff_syst_dw")
        draw_hist(outdir, title_prefix, dStatUp, "dataEff_stat_up")
        draw_hist(outdir, title_prefix, dStatDw, "dataEff_stat_dw")
        # MC stat/syst up/down
        draw_hist(outdir, title_prefix, mcSystUp, "mcEff_syst_up")
        draw_hist(outdir, title_prefix, mcSystDw, "mcEff_syst_dw")
        draw_hist(outdir, title_prefix, mcStatUp, "mcEff_stat_up")
        draw_hist(outdir, title_prefix, mcStatDw, "mcEff_stat_dw")
        # (If options.makeSFPlots): SF stat/syst up/down
        if options.makeSFPlots:
            draw_hist(outdir, title_prefix, sfSystUp, "SF_syst_up")
            draw_hist(outdir, title_prefix, sfSystDw, "SF_syst_dw")
            draw_hist(outdir, title_prefix, sfStatUp, "SF_stat_up")
            draw_hist(outdir, title_prefix, sfStatDw, "SF_stat_dw")
        # Everything else
        for k in hists["data"].keys():
            draw_hist(
                outdir, title_prefix,
                hists["data"][k], "dataEff_{}".format(k))
            draw_hist(
                outdir, title_prefix,
                hists["mc"][k], "mcEff_{}".format(k))
            if (options.makeSFPlots):
                draw_hist(outdir, title_prefix, sfHists[k], "SF_{}".format(k))

    # Create separate SF TFile
    if options.makeSFPlots:
        logging.debug(" ---> Will output SFs to file debug_SF.root")
        if options.debug:
            SFFile = TFile('debug_SF.root', 'update')
        else:
            SFFile = TFile('SFPlots_%s_%s.root' % (
                year, options.version), 'update')
        dir_name = quality + "/Period" + period + "/" + trigger + "/"
        logging.debug(" - Directory: " + dir_name)
        SFFile.mkdir(dir_name)
        SFFile.cd(dir_name)
        sfHists["nominal"].Write("sf_%s_nominal" % (options.region.lower()))
        sfSystUp.Write("sf_%s_syst_up" % (
            options.region.lower()), TObject.kOverwrite)
        sfSystDw.Write("sf_%s_syst_down" % (
            options.region.lower()), TObject.kOverwrite)
        sfStatUp.Write("sf_%s_stat_up" % (
            options.region.lower()), TObject.kOverwrite)
        sfStatDw.Write("sf_%s_stat_down" % (
            options.region.lower()), TObject.kOverwrite)
        for k in sorted(sfHists.keys()):
            if k != "nominal":
                sfHists[k].Write("sf_%s_%s" % (
                    options.region.lower(), k), TObject.kOverwrite)

    # (If options.makeSFPlots): Create separate SF TFile
    if options.makeSFPlots:
        if options.debug:
            logging.debug("Will output SFs to file debug_SF.root")
            SFFile = TFile('debug_SF.root', 'update')
        else:
            # Change ntuple version to match your inputs!
            SFFile = TFile('SFPlots_%s_%s.root' % (
                options.year, options.version), 'update')
        dir_name = options.quality + "/Period" + options.period + "/" +\
            options.trigger + "/"
        logging.debug(" - Directory: " + dir_name)
        SFFile.mkdir(dir_name)
        SFFile.cd(dir_name)
        sfHists["nominal"].Write("sf_%s_nominal" % (options.region.lower()))
        sfSystUp.Write("sf_%s_syst_up" % (
            options.region.lower()), TObject.kOverwrite)
        sfSystDw.Write("sf_%s_syst_down" % (
            options.region.lower()), TObject.kOverwrite)
        sfStatUp.Write("sf_%s_stat_up" % (
            options.region.lower()), TObject.kOverwrite)
        sfStatDw.Write("sf_%s_stat_down" % (
            options.region.lower()), TObject.kOverwrite)
        for k in sorted(sfHists.keys()):
            if k != "nominal":
                sfHists[k].Write("sf_%s_%s" % (
                    options.region.lower(), k), TObject.kOverwrite)

    # (If options.printSFValues):
    # Print inclusive SF for nominal, systematic plots
    if options.printSFValues:
        print('Scale Factor Values: %s, %s, %s, %s, %s' % (
            options.trigger, options.region, options.quality, options.year,
            options.period))
        placeholder = 0
        print("{:<15} {:<15} {:<15}".format('Systematic', 'Value', '% Diff'))
        print("{:<15} {:<15} {:<15} {:<15}".format(
            "nominal", round(sfValues["nominal"], 5),
            "N/A", "Stat Error: " + str(sfstaterr)))
        for k, v in sorted(sfValues.items()):
            if (k != "nominal" and k != "TotSyst"):
                placeholder += (v - sfValues["nominal"])**2
                print("{:<15} {:<15} {:<15}".format(k, round(v, 5), round(
                    (v - sfValues["nominal"]) / sfValues["nominal"], 5) * 100))
        sfValues["TotSyst"] = sfValues["nominal"] + math.sqrt(placeholder)
        print(
            "{:<15} {:<15} {:<15}".format(
                "Total",
                round(sfValues["TotSyst"], 5),
                round(
                    (sfValues["TotSyst"]-sfValues["nominal"]
                    )/sfValues["nominal"], 5) * 100))

if __name__ == "__main__":
    main()
