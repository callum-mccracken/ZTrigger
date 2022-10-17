Muon Trigger Scale Factor Production
========================
These instructions describe how to produce scale factors for the ATLAS single-muon triggers using the MuonTPPostProcessing framework. General instructions for the MuonTPPostProcessing framework can be found in the [README](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/README.md). These instructions document specific steps to take for seamless muon trigger SF production.

# Setup

### Cloning the project
```
mkdir MuonTPP
cd MuonTPP
mkdir build run output
git clone --recursive ssh://git@gitlab.cern.ch:7999/atlas-mcp/MuonTPPostProcessing.git
```

### Optional: Checkout a new or existing branch to work on
#### New branch:
```
cd MuonTPPostProcessing
git checkout -b my-new-branch
```

#### Existing branch:
```
cd MuonTPPostProcessing
git checkout my-existing-branch
git submodule update
```

### Building the project
```
cd ../build
setupATLAS
lsetup rucio
voms-proxy-init -voms atlas
asetup AthAnalysis,21.2.196
cmake ../MuonTPPostProcessing
make -j
source */setup.sh
```

### On every login
```
setupATLAS
lsetup rucio
voms-proxy-init -voms atlas
cd MuonTPP/build
asetup
source */setup.sh
```
where the `lsetup rucio` and `voms-proxy-init` steps are only needed if you are running over input ntuples stored on the grid.

# Steps Toward Scale Factor Production

These instructions walk you through scale factor (SF) production from start to finish. SF production is broadly divided into two steps:
1. Produce probe and match distributions: 
- [Obtain input ntuples](#input-ntuples)
- [Create configs](#creating-configs)
- [Execute WriteTagProbeHistos](#executing-writetagprobehistos)
2. Produce SF maps (using outputs of Step 1.):
- [Execute make2DEff.py](#executing-make2deff)

## Input ntuples
The single-muon trigger SF configs use the Zmumu TP ntuples as input. These are found under scope `group.perf-muons` on Rucio. Subscribe to atlas-cp-muon-tagprobe@cern.ch for production news. You must be able to access data and MC ntuples for every period for which you want to produce SFs.  
Examples for 2018 Period B are:  
```
group.perf-muons:group.perf-muons.data18_13TeV.periodB.physics_Main.PhysCont.DAOD_MUON1.grp18_v01_p4144_v064_EXT0
group.perf-muons:group.perf-muons.mc16_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.NTUP_MCP.r10724_p4145_v064_EXT0
```

## Creating Configs

Three sets of configs are required for producing muon trigger scale factors:
1. **Input configs** provide paths to input MuonTP ntuples ([example](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/data/InputConfTRIUMF/data_2018_B_grp18_v01_p4144.conf))
2. **Run configs** specify selections to make on tag and probe muons used for SF evaluation ([example](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/data/RunConf/ZTrigger/SingleMuonTriggers/MuonProbes_OC_nominal_2018.conf))
3. **Histo configs** define 1D or 2D histograms to be filled ([example](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/data/HistoConf/ZTrigger/SingleMuonTriggers/1D_hist.conf))

### Input configs
Input configs are institution-dependent and point to where your TP ntuples are stored. They also specify which GoodRunLists (GRL) and Pileup Reweighting (PRW) files to use. 

#### RSE storage
You can automatically generate input configs that read TP ntuples stored on a Rucio storage element, so it's advantageous to replicate the TP ntuples you need to read to such an element. You can generate input configs by following the instructions for the `ListDisk.py` and `CreateInputConfigs.py` scripts [here](https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/MuonEfficiencyCorrectionsSubgroup#Input_config_files).
For instance, to access v064 TP ntuples that you've downloaded to CA-SFU-T2_LOCALGROUPDISK, you would run:
```
cd run
python ../MuonTPPostProcessing/ClusterSubmission/python/ListDisk.py --rse CA-SFU-T2_LOCALGROUPDISK -p v064
```
This writes out a file `CA-SFU-T2_LOCALGROUPDISK_<TODAYS-DATE>_v064.txt`, containing the paths to the ntuples stored on CA-SFU-T2_LOCALGROUPDISK. To make input configs, you would run:

```
python ../MuonTPPostProcessing/MuonTPPostProcessing/python/FileManagement/CreateInputConfigs.py -i  CA-SFU-T2_LOCALGROUPDISK_<TODAYS-DATE>_v064.txt --engine SLURM -J SF2018-local --readFromRSE --rse  CA-SFU-T2_LOCALGROUPDISK -o ../MuonTPPostProcessing/MuonTPPostProcessing/data/InputConfTRIUMF
```

where `InputConfigTRIUMF` is an institution-specific directory to which your input configs will be written. Configs produced in this way will automatically have the proper GRL and PRW files listed as inputs.

#### Local storage
If your ntuples are stored locally, you can just add their local paths to a new input config. You will also have to download and store the GRL and PRW files locally; up-to-date recommendations for Run 2 analyses can be found [here](https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/MuonEfficiencyCorrectionsSubgroup#TP_PRW_files).


### Run configs
The run configs decide the selections that will be applied to tag and probe muons. 
New selections must be defined for every quality working point (Loose, Medium, Tight, HighPt), every trigger for which SFs will be produced, and every systematic variation. It is simplest to have different run configs for:

 - Every period for which the triggers are consistent (usually means one set of configs for each year)
 - Every systematic variation
 
Each of these configs can include selections defined for every applicable trigger in that period, and for every quality working point. For example: in [this](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/data/RunConf/ZTrigger/SingleMuonTriggers/MuonProbes_OC_nominal_2018.conf) config, three triggers are specified at each of the four quality working points. 

For the muon trigger SFs, the first line of each selection should read `New_TPSelection ZmumuTPMerged OC MuonProbes` in order to specify the ntuple tree to use. The rest of the syntax is specified in the [tutorial](https://indico.cern.ch/event/835647/contributions/3512911/attachments/1885904/3108902/mpi-beamer-template.pdf#page=26). 

If you are adding a new trigger to your run config, ensure that you have defined a "match" for it in [`MatchesForZmumuMuon.conf`](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/data/RunConf/ZTrigger/SingleMuonTriggers/MatchesforZmumuMuon.conf) as well, following the simple syntax there.

### Histo configs
The histo configs specify the histograms to fill for each selection defined in the run configs. The [2D](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/data/HistoConf/ZTrigger/SingleMuonTriggers/2D_hist.conf) eta-phi histograms are essential for SF production, since SF maps are delivered as a function of eta and phi. The [1D](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/data/HistoConf/ZTrigger/SingleMuonTriggers/1D_hist.conf) histograms provide helpful diagnostic distributions.

## Executing WriteTagProbeHistos

After producing input, run and histo configs, we can finally generate distributions of probe and match muon efficiencies. We do this using `WriteTagProbeHistos`, which produces ROOT files that contain these distributions. This command works as documented in step b [here](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/README.md#2-simple-usage).
For instance, we could do:

```
cd run
WriteTagProbeHistos -i ../MuonTPPostProcessing/MuonTPPostProcessing/data/InputConfTRIUMF/data_2018_B_grp18_v01_p3544_p3553.conf -h ../MuonTPPostProcessing/MuonTPPostProcessing/data/HistoConf/ZTrigger/SingleMuonTriggers/2D_hist.conf -r ../MuonTPPostProcessing/MuonTPPostProcessing/data/RunConf/ZTrigger/SingleMuonTriggers/MuonProbes_OC_nominal_2018.conf -o ../output/data18B_nominal.root
```

This step needs to be performed iteratively for:
- Every year and data-taking period 
- Every MC campaign
- Every systematic variation

At the end of this step, you should have a collection of ROOT files in one directory for every data-taking period/MC campaign and systematic variation.
For the next step to work seamlessly, the ROOT files should be named `data{year}_{period}_{systematic}*.root` and `mc{campaign}_{year}_{systematic}*.root`. For instance, valid naming for the nominal variation of PeriodB 2018 would be `data2018_B_nominal_v064.root` and `mc16e_2018_nominal_v064.root`.

If using a batch system, running `WriteTagProbeHistos` for every combination of the above can be done more efficiently using a bash script to submit batch jobs. Since batch systems vary, the following describes how this can be accomplished for the batch systems of two institutes.

### Tufts
Use the script [`batchWTPH.sh`](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/scripts/Tufts/batchWTPH.sh), which you can run with
```
source batchWTPH.sh
```

### TRIUMF
Use the script [`makeWTPHBatch.sh`](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/scripts/TRIUMF/makeWTPHBatch.sh) to write out job files and a shell script to submit them: 
```
source makeWTPHBatch.sh
```
Then run the resulting shell script, which handles the submission:
```
source submitAllWTPH.sh
```

## Executing make2DEff  

The trigger scale factor tool requires SF maps in a particular format. These need to be made from the output of `WriteTagProbeHistos` that you have produced above, using the 2D histo config, for each data-taking period and each systematic.   

The python script [`make2DEff.py`](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/data/RunConf/ZTrigger/make2DEff.py) exists for this purpose. It can be run with:

```
python make2DEff.py -i [input file directory] -y [year] -p [period] -r [region] -t [trigger] -q [quality] --[other options]
```

where `[input file directory]` is the directory to which you have written the outputs of `WriteTagProbeHistos` in the previous step. For instance, to produce SF maps for Period B 2018, you could run:

```
 python make2DEff.py -i <path/to/WTPH/output> -y 18 -p B -r Barrel -t HLT_mu26_ivarmedium -q Medium 
```

A complete SF ROOT file requires running over every data-taking period, region, trigger and quality working point. Assuming you have already made the required `WriteTagProbeHistos` output,this can be done efficiently by running multiple `make2DEff.py` jobs on a batch system. As long as jobs use `WriteTagProbeHistos` output from a single directory, output will be written to a single SF ROOT file per year. Since batch systems vary, the following describes how this can be accomplished for the batch systems of two institutes.

### Tufts
You can use the script [`batch2DEff.sh`](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/scripts/Tufts/batch2DEff.sh) to submit jobs:

```
source batch2DEff.sh
```
This script is added to the Slurm workload manager. More details are provided in the script itself.

### TRIUMF (Cedar cluster)
You can first use the script [`make2DEffBatch.sh`](https://gitlab.cern.ch/atlas-mcp/MuonTPPostProcessing/-/blob/master/MuonTPPostProcessing/scripts/TRIUMF/make2DEffBatch.sh) to write out job files:
```
source make2DEffBatch.sh 
```
Then submit the jobs by sourcing the file that gets written out, named `submitAll.sh` by default:
```
source submitAll.sh
```



