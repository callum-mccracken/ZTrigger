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


# Imports and Option Parser #
from ROOT import *
from array import array
import math
import optparse
import os
import fnmatch

# Suppresses basic info prints to terminal (used to shut up TEff constructor)
gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")

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
parser.add_option('-i', '--inDir', type='string', default='./',
                  dest='inDir')
# path to directory where you want the output(s) of the script to be stored
parser.add_option('-o', '--outDir', type='string', default='./',
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

(options, args) = parser.parse_args()

gROOT.LoadMacro('AtlasStyle.C')
gROOT.LoadMacro('AtlasUtils.C')
gROOT.LoadMacro('AtlasLabels.C')

if gROOT.LoadMacro('AtlasStyle.C') > 0:
    SetAtlasStyle()

# Load input files
if options.debug:
    print('\033[1;32m' + "DEBUG: " + '\033[0m' +
          "Looking for input files in directory: " + options.inDir)

# Data input files:
for filename in fnmatch.filter(
        os.listdir(options.inDir), "*data*{}*".format(options.period)):
    if options.debug:
        print('\033[1;32m' + "DEBUG: " +
              '\033[0m' + "Found data file: " + filename)
    if "nominal" in filename:
        dataNominal = TFile(options.inDir + "/" + filename)
    elif "isoTightTrackOnly" in filename:
        dataIsoTTO = TFile(options.inDir + "/" + filename)
    elif "isoTight" in filename:
        dataIsoTight = TFile(options.inDir + "/" + filename)
    elif "mll" in filename:
        dataMll = TFile(options.inDir + "/" + filename)
    elif "dphill" in filename:
        dataDPHill = TFile(options.inDir + "/" + filename)
    elif "ptup" in filename:
        dataPtUp = TFile(options.inDir + "/" + filename)
    elif "ptdw" in filename:
        dataPtDw = TFile(options.inDir + "/" + filename)
    elif "noIP" in filename:
        dataNoIP = TFile(options.inDir + "/" + filename)
    elif "mupos" in filename:
        dataMuPos = TFile(options.inDir + "/" + filename)
    elif "muneg" in filename:
        dataMuNeg = TFile(options.inDir + "/" + filename)
    elif "nvtx_up" in filename:
        dataNvtxUp = TFile(options.inDir + "/" + filename)
    elif "nvtx_dw" in filename:
        dataNvtxDw = TFile(options.inDir + "/" + filename)
# MC input files
if '15' in options.year:
    montecarlo = '16a_2015'
elif '16' in options.year:
    montecarlo = '16a_2016'
elif '17' in options.year:
    montecarlo = '16d'
elif '18' in options.year:
    montecarlo = '16e'
else:
    print('\033[1;32m' + "WARNING: " + '\033[0m' + "Not a valid year. " +
          "Please specify 15, 16, 17 or 18 with the -y option.")
for filename in fnmatch.filter(os.listdir(options.inDir), "*mc*"):
    if options.debug:
        print('\033[1;32m' + "DEBUG: " + '\033[0m' +
              "Found MC file: " + filename)
    if montecarlo not in filename:
        continue
    if "nominal" in filename:
        monteCarloNominal = TFile(options.inDir + "/" + filename)
    elif "isoTightTrackOnly" in filename:
        monteCarloIsoTTO = TFile(options.inDir + "/" + filename)
    elif "isoTight" in filename:
        monteCarloIsoTight = TFile(options.inDir + "/" + filename)
    elif "mll" in filename:
        monteCarloMll = TFile(options.inDir + "/" + filename)
    elif "dphill" in filename:
        monteCarloDPHill = TFile(options.inDir + "/" + filename)
    elif "ptup" in filename:
        monteCarloPtUp = TFile(options.inDir + "/" + filename)
    elif "ptdw" in filename:
        monteCarloPtDw = TFile(options.inDir + "/" + filename)
    elif "noIP" in filename:
        monteCarloNoIP = TFile(options.inDir + "/" + filename)
    elif "mupos" in filename:
        monteCarloMuPos = TFile(options.inDir + "/" + filename)
    elif "muneg" in filename:
        monteCarloMuNeg = TFile(options.inDir + "/" + filename)
    # Need to be careful about period K 2017 nvtx systematic:
    # cut >/< 19 vertices for 2017 but >/< 25 for period K
    if (options.year == '17' and options.period == 'K'):
        print("Getting nvtx files for 2017 period K")
        #if "nvtx_up" in filename and 'K' in filename:
        #     monteCarloNvtxUp = TFile(options.inDir+filename)
        #if "nvtx_dw" in filename and 'K' in filename:
        #     monteCarloNvtxDw = TFile(options.inDir+filename)
    else:
        if "nvtx_up" in filename:
            monteCarloNvtxUp = TFile(options.inDir + "/" + filename)
        if "nvtx_dw" in filename:
            monteCarloNvtxDw = TFile(options.inDir + "/" + filename)

# Creating dictionaries with (histname, hist) tuples
# Directories where probe and match hists are located
# (identically name in every WTPH output)
probeDir = 'ZmumuTPMerged/%sMuonProbes_%s/OC/%s/Probe/' % (
    options.quality, options.region.capitalize(), options.trigger)
matchDir = 'ZmumuTPMerged/%sMuonProbes_%s/OC/%s/Match/' % (
    options.quality, options.region.capitalize(), options.trigger)

# Hists to look for in the above directories
# (also identically named) in every WTPH output)
probeHist = '%sMuonProbes_%s_OC_%s_Probe_etaphi_fine_%s' % (
    options.quality, options.region.capitalize(), options.trigger,
    options.region.capitalize())
matchHist = '%sMuonProbes_%s_OC_%s_Match_etaphi_fine_%s' % (
    options.quality, options.region.capitalize(), options.trigger,
    options.region.capitalize())
if options.debug:
    print('\033[1;32m' + "DEBUG: " + '\033[0m' + "In each ROOT file, " +
          "will look in directory \n" + probeDir + " for hist \n" + probeHist +
          '\n')
histNames = ["Nominal", "IsoTight", "IsoTTO", "Mll", "PtUp", "PtDw", "NoIP",
             "MuPos", "MuNeg", "NvtxUp", "NvtxDw", "DPHill"]

# Data:
dataProbeHists = {}
dataMatchHists = {}
dataEffs = {}
dataHists = {}
for i, v in enumerate([
        dataNominal, dataIsoTight, dataIsoTTO, dataMll, dataPtUp, dataPtDw,
        dataNoIP, dataMuPos, dataMuNeg, dataNvtxUp, dataNvtxDw, dataDPHill]):
    name = histNames[i]
    dataProbeHists[name] = v.Get(probeDir + "/" + probeHist)
    if not dataProbeHists[name]:
        print('\033[1;32m' + "WARNING: " + '\033[0m' +
              "Couldn't find {}. Does this really exist in {}?\n".format(
                  probeDir + probeHist, v.GetName()))
        exit()
    dataMatchHists[name] = v.Get(matchDir + "/" + matchHist)
    if not dataMatchHists[name]:
        print('\033[1;32m' + "WARNING: " + '\033[0m' +
              "Couldn't find {}. Does this really exist in {}?\n".format(
                  matchDir + matchHist, v.GetName()))
        exit()
    if options.debug:
        print('\033[1;32m' + "DEBUG: " + '\033[0m' +
              "Data probe & match hists acquired: " + name)
    # Make TEff object to do stat errors properly
    dataEffs[name] = TEfficiency(dataMatchHists[name], dataProbeHists[name])
    #dataEffs[name].SetStatisticOption(TEfficiency.kFNormal)
    # Make empty TH2 which will be filled with TEff bin values
    # (+/- errors if needed) down below
    dataHists[name] = dataProbeHists[name].Clone()
    dataHists[name].Reset()
# Setting up data systematic, statistical variation histograms
dSystUp = dataProbeHists["Nominal"].Clone('dSystUp')
dSystUp.Reset()
dSystDw = dataProbeHists["Nominal"].Clone('dSystDw')
dSystDw.Reset()
dStatUp = dataProbeHists["Nominal"].Clone('dStatUp')
dStatUp.Reset()
dStatDw = dataProbeHists["Nominal"].Clone('dStatDw')
dStatDw.Reset()
dataHists["IsoEnv"] = dataProbeHists["Nominal"].Clone('IsoEnv')
dataHists["IsoEnv"].Reset()

# MC:
mcProbeHists = {}
mcMatchHists = {}
mcEffs = {}
mcHists = {}
for j, w in enumerate([
        monteCarloNominal, monteCarloIsoTight, monteCarloIsoTTO, monteCarloMll,
        monteCarloPtUp, monteCarloPtDw, monteCarloNoIP, monteCarloMuPos,
        monteCarloMuNeg, monteCarloNvtxUp, monteCarloNvtxDw,
        monteCarloDPHill]):
    name = histNames[j]
    mcProbeHists[name] = w.Get(probeDir + "/" + probeHist)
    if not mcProbeHists[name]:
        print('\033[1;32m' + "WARNING: " + '\033[0m' +
              "Couldn't find MC in {}. Does this really exist in {}?\n".format(
                probeDir + probeHist, w.GetName()))
        exit()
    mcMatchHists[name] = w.Get(matchDir + "/" + matchHist)
    if not mcMatchHists[name]:
        print('\033[1;32m' + "WARNING: " + '\033[0m' +
              "Couldn't find MC in {}. Does this really exist in {}?\n".format(
                probeDir + probeHist, w.GetName()))
        exit()
    if options.debug:
        print('\033[1;32m' + "DEBUG: " + '\033[0m' +
              "MC probe & match hists acquired: " + name)
    # Make TEff object to do stat errors properly
    mcEffs[name] = TEfficiency(mcMatchHists[name], mcProbeHists[name])
    #mcEffs[name].SetStatisticOption(TEfficiency.kFNormal)
    # Make empty TH2 which will be filled with TEff bin values
    # (+/- errors if needed) down below
    mcHists[name] = mcProbeHists[name].Clone()
    mcHists[name].Reset()
# Setting up mc systematic, statistical variation histograms
mcSystUp = mcProbeHists["Nominal"].Clone('mcSystUp')
mcSystUp.Reset()
mcSystDw = mcProbeHists["Nominal"].Clone('mcSystDw')
mcSystDw.Reset()
mcStatUp = mcProbeHists["Nominal"].Clone('mcStatUp')
mcStatUp.Reset()
mcStatDw = mcProbeHists["Nominal"].Clone('mcStatDw')
mcStatDw.Reset()
mcHists["IsoEnv"] = mcProbeHists["Nominal"].Clone('IsoEnv')
mcHists["IsoEnv"].Reset()

# Number of x- and y-bins - will be used many times
xbins = dataProbeHists["Nominal"].GetNbinsX()
ybins = dataProbeHists["Nominal"].GetNbinsY()

# (If options.makeSFPlots): Initialize stat/syst up/down
if options.makeSFPlots:
    if options.debug:
        print('\033[1;32m' + "DEBUG: " + '\033[0m' +
              "makeSFPlots = True! Will initialize SF hists")
    sfHists = {}
    for k in dataHists.keys():
        sfHists[k] = dataHists[k].Clone()
        sfHists[k].Reset()
    sfStatUp = dStatUp.Clone()
    sfStatDw = dStatDw.Clone()
    sfSystUp = dSystUp.Clone()
    sfSystDw = dSystDw.Clone()

# (If options.printSFValues):
# Initlaize SF value variables and obtain inclusive stat uncertainty
if (options.printSFValues):
    if options.debug:
        print('\033[1;32m' + "DEBUG: " + '\033[0m' + "printSFValues = True! " +
              "Will keep track of SF values for each syst")
    # To get inclusive SF values,
    # need to add probes and matches across all bins
    nDataMatches = {}
    nDataProbes = {}
    nMCMatches = {}
    nMCProbes = {}
    sfValues = {}
    for k in dataHists.keys():
        nDataMatches[k] = 0
        nDataProbes[k] = 0
        nMCMatches[k] = 0
        nMCProbes[k] = 0
        sfValues[k] = 0
    sfValues["IsoEnv"] = 0
    sfValues["TotSyst"] = 0

    # Inclusive SF stat uncertainty using 1-bin copies of data/mc hists
    #Data inclusive eff
    dM1bin = dataMatchHists["Nominal"].Clone()
    dM1bin.Rebin2D(xbins, ybins)
    dP1bin = dataProbeHists["Nominal"].Clone()
    dP1bin.Rebin2D(xbins, ybins)
    dE1bin = TEfficiency(dM1bin, dP1bin)

    d1bin = dataHists["Nominal"].Clone()
    d1bin.Reset()
    d1bin.Rebin2D(xbins, ybins)
    gbin = dE1bin.GetGlobalBin(1, 1)
    deff = dE1bin.GetEfficiency(gbin)
    dstaterr = dE1bin.GetEfficiencyErrorUp(gbin)

    #MC inclusive eff
    mcM1bin = mcMatchHists["Nominal"].Clone()
    mcM1bin.Rebin2D(xbins, ybins)
    mcP1bin = mcProbeHists["Nominal"].Clone()
    mcP1bin.Rebin2D(xbins, ybins)
    mcE1bin = TEfficiency(mcM1bin, mcP1bin)

    mc1bin = mcHists["Nominal"].Clone()
    mc1bin.Reset()
    mc1bin.Rebin2D(xbins, ybins)
    mceff = mcE1bin.GetEfficiency(gbin)
    mcstaterr = mcE1bin.GetEfficiencyErrorUp(gbin)

    #Error propagation: err_sf = sf*(err_data_eff/data_eff + err_mc_eff/mc_eff)
    sf = deff / mceff
    sfstaterr = (sf * (dstaterr / deff + mcstaterr / mceff))

# Looping through each bin of each histogram
# to grab the nominal efficiency and the systematic variations
if options.debug:
    print('\033[1;32m' + "DEBUG: " + '\033[0m' +
          'Now starting loop over bins...')
for i in range(1, xbins + 2):
    for j in range(1, ybins + 2):
        # Debugging particular bin issues
        # print("Bin : ("+str(i)+","+str(j)+")")
        # Global bin # to used w GetEfficiency() and GetEfficiencyErrorUp/Low()
        globalbin = dataEffs["Nominal"].GetGlobalBin(i, j)
        # Getting data, MC nominal efficiency and up/down stat bin errors:
        dnom = dataEffs["Nominal"].GetEfficiency(globalbin)
        dstatup = dataEffs["Nominal"].GetEfficiencyErrorUp(globalbin)
        dstatdw = dataEffs["Nominal"].GetEfficiencyErrorLow(globalbin)
        mcnom = mcEffs["Nominal"].GetEfficiency(globalbin)
        mcstatup = mcEffs["Nominal"].GetEfficiencyErrorUp(globalbin)
        mcstatdw = mcEffs["Nominal"].GetEfficiencyErrorLow(globalbin)

        # Fill nominal + statUp/statDw data, MC efficiency TH2's
        dataHists["Nominal"].SetBinContent(i, j, dnom)
        mcHists["Nominal"].SetBinContent(i, j, mcnom)
        dStatUp.SetBinContent(i, j, dnom + dstatup)
        mcStatUp.SetBinContent(i, j, mcnom + mcstatup)
        dStatDw.SetBinContent(i, j, dnom - dstatdw)
        mcStatDw.SetBinContent(i, j, mcnom - dstatdw)

        # (If options.makeSFPlots):
        # Error propagation for SF stat up/down hists, in each bin
        if (options.makeSFPlots):
            if (mcnom != 0):
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
        dsyst_tight = dataEffs["IsoTight"].GetEfficiency(globalbin)
        dsyst_tto = dataEffs["IsoTTO"].GetEfficiency(globalbin)
        if (abs(dnom - dsyst_tight) > abs(dnom - dsyst_tto)):
            dsyst_iso = dnom - dsyst_tight
            dataHists["IsoEnv"].SetBinContent(i, j, dsyst_tight)
        if (abs(dnom - dsyst_tight) <= abs(dnom - dsyst_tto)):
            dsyst_iso = dnom - dsyst_tto
            dataHists["IsoEnv"].SetBinContent(i, j, dsyst_tto)
        # Add iso syst in quadrature to total syst bin error
        dsyst_tot += (dsyst_iso**2)
        # MC
        mcsyst_tight = mcEffs["IsoTight"].GetEfficiency(globalbin)
        mcsyst_tto = mcEffs["IsoTTO"].GetEfficiency(globalbin)
        # If tight systematic larger than TTO systematic
        if (abs(mcnom - mcsyst_tight) > abs(mcnom - mcsyst_tto)):
            mcsyst_iso = mcnom - mcsyst_tight
            mcHists["IsoEnv"].SetBinContent(i, j, mcsyst_tight)
            #SF inclusive IsoEnv value (if options.printSFValues)
            if (options.printSFValues):
                nDataMatches["IsoEnv"] += dataMatchHists[
                    "IsoTight"].GetBinContent(i, j)
                nDataProbes["IsoEnv"] += dataProbeHists[
                    "IsoTight"].GetBinContent(i, j)
                nMCMatches["IsoEnv"] += mcMatchHists[
                    "IsoTight"].GetBinContent(i, j)
                nMCProbes["IsoEnv"] += mcProbeHists[
                    "IsoTight"].GetBinContent(i, j)
        # If TTO systematic larger than tight systematic
        elif (abs(mcnom - mcsyst_tight) <= abs(mcnom - mcsyst_tto)):
            mcsyst_iso = mcnom - mcsyst_tto
            mcHists["IsoEnv"].SetBinContent(i, j, mcsyst_tto)
            # SF inclusive IsoEnv value (if options.printSFValues)
            if (options.printSFValues):
                nDataMatches["IsoEnv"] += dataMatchHists[
                    "IsoTTO"].GetBinContent(i, j)
                nDataProbes["IsoEnv"] += dataProbeHists[
                    "IsoTTO"].GetBinContent(i, j)
                nMCMatches["IsoEnv"] += mcMatchHists[
                    "IsoTTO"].GetBinContent(i, j)
                nMCProbes["IsoEnv"] += mcProbeHists[
                    "IsoTTO"].GetBinContent(i, j)
        # Add iso syst in quadrature to total syst bin error
        mcsyst_tot += (mcsyst_iso**2)

        # Get non-isolation systematics for the bin:
        for k in dataHists.keys():
            if ("Nominal" not in k and "IsoEnv" not in k):
                #Data:
                dsyst = dataEffs[k].GetEfficiency(globalbin)
                dataHists[k].SetBinContent(i, j, dsyst)
                if ("Iso" not in k): dsyst_tot += ((dnom - dsyst)**2)
                #MC:
                mcsyst = mcEffs[k].GetEfficiency(globalbin)
                mcHists[k].SetBinContent(i, j, mcsyst)
                if ("Iso" not in k): mcsyst_tot += ((mcnom - mcsyst)**2)
            # SF values (if options.makeSFPlots)
            if (options.printSFValues and "IsoEnv" not in k):
                nDataMatches[k] += dataMatchHists[k].GetBinContent(i, j)
                nDataProbes[k] += dataProbeHists[k].GetBinContent(i, j)
                nMCMatches[k] += mcMatchHists[k].GetBinContent(i, j)
                nMCProbes[k] += mcProbeHists[k].GetBinContent(i, j)

        # Finally, set the bin content of the
        # Syst Up/Dw plots = nominal efficiency + total systematic variation
        dSystUp.SetBinContent(i, j, dnom + math.sqrt(dsyst_tot))
        dSystDw.SetBinContent(i, j, dnom - math.sqrt(dsyst_tot))
        mcSystUp.SetBinContent(i, j, mcnom + math.sqrt(mcsyst_tot))
        mcSystDw.SetBinContent(i, j, mcnom - math.sqrt(mcsyst_tot))

        # (If options.makeSFPlots): Fill syst up/down plots
        if (options.makeSFPlots):
            if (mcnom != 0 and math.sqrt(mcsyst_tot) != 0):
                sfSystUp.SetBinContent(i, j, (dnom + math.sqrt(dsyst_tot)) / (
                    mcnom + math.sqrt(mcsyst_tot)))
                sfSystDw.SetBinContent(i, j, (dnom - math.sqrt(dsyst_tot)) / (
                    mcnom - math.sqrt(mcsyst_tot)))
            else:
                sfSystUp.SetBinContent(i, j, 0)
                sfSystDw.SetBinContent(i, j, 0)
            for k in dataHists.keys():
                sfHists[k] = dataHists[k].Clone()
                sfHists[k].Divide(mcHists[k])

# If inclusive SF values requested,
# get them by dividing total matches/probes for data and mc
if (options.printSFValues):
    for k in dataHists.keys():
        sfValues[k] = (nDataMatches[k] / nDataProbes[k]) / (
            nMCMatches[k] / nMCProbes[k])

# Create/update systematics Efficiencies TFile
if (options.year == '15'):
    montecarlo = montecarlo.replace('_2015', '')
elif (options.year == '16'):
    montecarlo = montecarlo.replace('_2016', '')

# Do not make efficiency ROOT files if options.printSFValues == True
if (not options.makeSFPlots and not options.printSFValues):
    if options.debug:
        print('\033[1;32m' + "DEBUG: " + '\033[0m' + "Will output data, MC " +
              "efficiencies to file " + options.outDir + "/debug.root")
        # test output file
        EfficienciesFile = TFile(options.outDir + '/debug.root', 'update')
    else:
        # Change ntuple version to match your inputs!
        print('\033[1;32m' + "INFO: " + '\033[0m' + "Will output data, MC " +
              "efficiencies to file " + options.outDir +
              "/muontrigger_sf_20%s_mc%s_%s.root" %
              (options.year.replace("20", ""), montecarlo, options.version))
        EfficienciesFile = TFile(
            options.outDir + '/muontrigger_sf_20%s_mc%s_%s.root' %
            (options.year.replace("20", ""), montecarlo, options.version),
            'update')  # outfile named in format for SF tool
    # Create directory
    if ("_RM" in options.trigger):
        dirName = options.quality + "/Period" + options.period + "/" +\
            options.trigger.replace("_RM", "") + "/"
    else:
        dirName = options.quality + "/Period" + options.period + "/" +\
            options.trigger + "/"
    if options.debug:
        print('\033[1;32m' + "DEBUG: " + '\033[0m' +
              " - Directory: " + dirName)
    EfficienciesFile.mkdir(dirName)
    EfficienciesFile.cd(dirName)
    # Put corresponding plots into working point directory
    #Data:
    dataHists["Nominal"].Write("eff_etaphi_fine_%s_data_nominal" % (
        options.region.lower()), TObject.kOverwrite)
    dSystUp.Write("eff_etaphi_fine_%s_data_syst_up" % (
        options.region.lower()), TObject.kOverwrite)
    dSystDw.Write("eff_etaphi_fine_%s_data_syst_down" % (
        options.region.lower()), TObject.kOverwrite)
    dStatUp.Write("eff_etaphi_fine_%s_data_stat_up" % (
        options.region.lower()), TObject.kOverwrite)
    dStatDw.Write("eff_etaphi_fine_%s_data_stat_down" % (
        options.region.lower()), TObject.kOverwrite)
    for k in sorted(dataHists.keys()):
        if (k != "dNominal"):
            dataHists[k].Write("eff_etaphi_fine_%s_data_%s" % (
                options.region.lower(), k), TObject.kOverwrite)
    #MC:
    mcHists["Nominal"].Write("eff_etaphi_fine_%s_mc_nominal" % (
        options.region.lower()), TObject.kOverwrite)
    mcSystUp.Write("eff_etaphi_fine_%s_mc_syst_up" % (
        options.region.lower()), TObject.kOverwrite)
    mcSystDw.Write("eff_etaphi_fine_%s_mc_syst_down" % (
        options.region.lower()), TObject.kOverwrite)
    mcStatUp.Write("eff_etaphi_fine_%s_mc_stat_up" % (
        options.region.lower()), TObject.kOverwrite)
    mcStatDw.Write("eff_etaphi_fine_%s_mc_stat_down" % (
        options.region.lower()), TObject.kOverwrite)
    for k in sorted(mcHists.keys()):
        if (k != "Nominal"):
            mcHists[k].Write("eff_etaphi_fine_%s_mc_%s" % (
                options.region.lower(), k), TObject.kOverwrite)


# (If options.savePNGs):
# Save all data, mc (and SF, if SF plots made) hists as pngs
def drawHist(outdir, titlePrefix, hist, name):
    c = TCanvas()
    c.SetTopMargin(0.1)
    c.SetBottomMargin(0.15)
    c.SetLeftMargin(0.15)
    c.SetRightMargin(0.15)
    gStyle.SetOptTitle(1)
    gStyle.SetOptStat(0)
    gStyle.SetPaintTextFormat(".3f")
    title = titlePrefix + name
    hist.SetDirectory(0)
    hist.SetTitle(title)
    hist.SetTitleSize(0.02, "t")
    hist.SetMaximum(1.0)
    hist.SetMinimum(0.0)
    hist.Draw("COLZ TEXT")
    c.SaveAs(outdir + titlePrefix + name + ".png")
    c.Close()


if (options.savePNGs):
    # Directory
    outdir = "./savePNGs_%s/" % (options.year)
    if options.debug: print("savePNGs = True! Will save PNGs to: " + outdir)
    if not os.path.exists(outdir): os.mkdir(outdir)
    # prefix for hist titles
    titlePrefix = "%s_%s_%s_etaphi_fine_%s_" % (
        options.quality, options.period, options.trigger.replace("_RM", ""),
        options.region.lower())
    gROOT.SetBatch()
    # Data stat/syst up/down
    drawHist(outdir, titlePrefix, dSystUp, "dataEff_syst_up")
    drawHist(outdir, titlePrefix, dSystDw, "dataEff_syst_dw")
    drawHist(outdir, titlePrefix, dStatUp, "dataEff_stat_up")
    drawHist(outdir, titlePrefix, dStatDw, "dataEff_stat_dw")
    # MC stat/syst up/down
    drawHist(outdir, titlePrefix, mcSystUp, "mcEff_syst_up")
    drawHist(outdir, titlePrefix, mcSystDw, "mcEff_syst_dw")
    drawHist(outdir, titlePrefix, mcStatUp, "mcEff_stat_up")
    drawHist(outdir, titlePrefix, mcStatDw, "mcEff_stat_dw")
    # (If options.makeSFPlots): SF stat/syst up/down
    if (options.makeSFPlots):
        drawHist(outdir, titlePrefix, sfSystUp, "SF_syst_up")
        drawHist(outdir, titlePrefix, sfSystDw, "SF_syst_dw")
        drawHist(outdir, titlePrefix, sfStatUp, "SF_stat_up")
        drawHist(outdir, titlePrefix, sfStatDw, "SF_stat_dw")
    # Everything else
    for k in dataHists.keys():
        drawHist(outdir, titlePrefix, dataHists[k], "dataEff_{}".format(k))
        drawHist(outdir, titlePrefix, mcHists[k], "mcEff_{}".format(k))
        if (options.makeSFPlots):
            drawHist(outdir, titlePrefix, sfHists[k], "SF_{}".format(k))

# (If options.makeSFPlots): Create separate SF TFile
if (options.makeSFPlots):
    if options.debug:
        print(" ---> Will output SFs to file debug_SF.root")
        SFFile = TFile('debug_SF.root', 'update')
    else:
        SFFile = TFile('SFPlots_%s_%s.root' % (
            options.year.replace("20", ""), options.version), 'update')
    dirName = options.quality + "/Period" + options.period + "/" +\
        options.trigger + "/"
    if options.debug:
        print(" - Directory: " + dirName)
    SFFile.mkdir(dirName)
    SFFile.cd(dirName)
    sfHists["Nominal"].Write("sf_%s_nominal" % (options.region.lower()))
    sfSystUp.Write("sf_%s_syst_up" % (
        options.region.lower()), TObject.kOverwrite)
    sfSystDw.Write("sf_%s_syst_down" % (
        options.region.lower()), TObject.kOverwrite)
    sfStatUp.Write("sf_%s_stat_up" % (
        options.region.lower()), TObject.kOverwrite)
    sfStatDw.Write("sf_%s_stat_down" % (
        options.region.lower()), TObject.kOverwrite)
    for k in sorted(sfHists.keys()):
        if (k != "Nominal"):
            sfHists[k].Write("sf_%s_%s" % (
                options.region.lower(), k), TObject.kOverwrite)

# (If options.makeSFPlots): Create separate SF TFile
if (options.makeSFPlots):
    if options.debug:
        print('\033[1;32m' + "DEBUG: " + '\033[0m' +
              "Will output SFs to file debug_SF.root")
        SFFile = TFile('debug_SF.root', 'update')
    else:
        # Change ntuple version to match your inputs!
        SFFile = TFile('SFPlots_%s_%s.root' % (
            options.year, options.version), 'update')
    dirName = options.quality + "/Period" + options.period + "/" +\
        options.trigger + "/"
    if options.debug:
        print('\033[1;32m' + "DEBUG: " + '\033[0m' +
              " - Directory: " + dirName)
    SFFile.mkdir(dirName)
    SFFile.cd(dirName)
    sfHists["Nominal"].Write("sf_%s_nominal" % (options.region.lower()))
    sfSystUp.Write("sf_%s_syst_up" % (
        options.region.lower()), TObject.kOverwrite)
    sfSystDw.Write("sf_%s_syst_down" % (
        options.region.lower()), TObject.kOverwrite)
    sfStatUp.Write("sf_%s_stat_up" % (
        options.region.lower()), TObject.kOverwrite)
    sfStatDw.Write("sf_%s_stat_down" % (
        options.region.lower()), TObject.kOverwrite)
    for k in sorted(sfHists.keys()):
        if (k != "Nominal"):
            sfHists[k].Write("sf_%s_%s" % (
                options.region.lower(), k), TObject.kOverwrite)

# (If options.printSFValues):
# Print inclusive SF for nominal, systematic plots
if (options.printSFValues):
    print('Scale Factor Values: %s, %s, %s, %s, %s' % (
        options.trigger, options.region, options.quality, options.year,
        options.period))
    placeholder = 0
    print("{:<15} {:<15} {:<15}".format('Systematic', 'Value', '% Diff'))
    print("{:<15} {:<15} {:<15} {:<15}".format("Nominal",
                                               round(sfValues["Nominal"], 5),
          "N/A", "Stat Error: " + str(sfstaterr)))
    for k, v in sorted(sfValues.items()):
        if (k != "Nominal" and k != "TotSyst"):
            placeholder += (v - sfValues["Nominal"])**2
            print("{:<15} {:<15} {:<15}".format(k, round(v, 5), round(
                (v - sfValues["Nominal"]) / sfValues["Nominal"], 5) * 100))
    sfValues["TotSyst"] = sfValues["Nominal"] + math.sqrt(placeholder)
    print("{:<15} {:<15} {:<15}".format("Total", round(sfValues["TotSyst"], 5),
        round((sfValues["TotSyst"]-sfValues["Nominal"])/sfValues["Nominal"],
              5) * 100))
