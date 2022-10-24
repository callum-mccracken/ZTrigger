import re
import os
from constants import WORKING_POINTS, DETECTOR_REGIONS, TOP_LEVEL_DIR,\
    SM_PRE_NOMINAL_CONFIG_TEMPLATE, ML_PRE_NOMINAL_CONFIG_TEMPLATE,\
    SM_NOMINAL_CONFIG_TEMPLATE, ML_NOMINAL_CONFIG_TEMPLATE
from triggers import triggers_in_period
from run_numbers import RUN_NUMBERS

single_block_template = """
New_TPSelection ZmumuTPMerged OC MuonProbes
    NameProbeSel {working_point}MuonProbes
    ProbeCut bool probe_matched_{working_point}Muons = 1
    ProbeCut floatGeV probe_pt > {pt_cutoff}
    Matches {trigger}
    DetRegion {detector_regions}
End_TPSelection
"""
multi_block_template = """
New_TPSelection ZmumuTPMuon OC {working_point}Probes_noProbeIP
    NameProbeSel {working_point}
    ProbeCut bool probe_matched_{working_point} = 1
    ProbeCut floatGeV probe_pt > {pt_cutoff:.1f}
    Matches {trigger} 
    DetRegion {detector_regions}
End_TPSelection
"""

def lowest_pt_from_single_trigger(trigger: str):
    """Given a trigger name, return """
    # pattern explanation:
    # blablabla_mu102_mu19blablala -- lowest pt is the second one
    match = re.match(r"(.)*(mu([0-9]+)){1,2}(.)*", trigger)
    assert match
    groups = match.groups()
    last_muon_pt = int(groups[2])
    return last_muon_pt

def pt_for_cutoff(trigger: str):
    """Get the pt to use in a cut, we do a little more than this value."""
    if "_OR_" in trigger:
        trigger_1, trigger_2, = trigger.split("_OR_")
        assert "mu" in trigger_1 and "mu" in trigger_2
        pt_1 = lowest_pt_from_single_trigger(trigger_1)
        pt_2 = lowest_pt_from_single_trigger(trigger_2)
        return pt_1 if pt_1 < pt_2 else pt_2
    else:
        return lowest_pt_from_single_trigger(trigger)

def pt_cutoff(trigger, single):
    """Get the pt value to use in the cut, a little higher than the trigger."""
    # TODO: is there a reason these are different?
    if single:
        return pt_for_cutoff(trigger) * 1.05
    else:
        return pt_for_cutoff(trigger) + 1


def make_selection_blocks(single, year, period):    
    blocks = []
    template = single_block_template if single else multi_block_template
    triggers = triggers_in_period(single, year, period)
    for working_point in WORKING_POINTS:
        for trigger in triggers:
            if "_OR_" in trigger:
                trigger_1, trigger_2, = trigger.split("_OR_")
                assert "mu" in trigger_1 and "mu" in trigger_2
                
            pt_cut = pt_cutoff(trigger, single)
            blocks.append(template.format(
                working_point=working_point,
                trigger=trigger,
                pt_cutoff=pt_cut,
                detector_regions=" ".join(DETECTOR_REGIONS)))
    return "".join(blocks)


def make_nominal_config(single, year, period, basic_filename):
    # get template
    if single:
        pre_nominal_template = SM_PRE_NOMINAL_CONFIG_TEMPLATE
    else:
        pre_nominal_template = ML_PRE_NOMINAL_CONFIG_TEMPLATE

    # get template text
    with open(pre_nominal_template, "r", encoding="utf-8") as pre_nom_file:
        pre_nominal_template_text = pre_nom_file.read()

    # make period cut
    start = RUN_NUMBERS[year][period]["START"]
    end = RUN_NUMBERS[year][period]["END"]
    nominal_file_text = pre_nominal_template_text.replace(
        "PERIOD_CUT_HERE",
        f"GlobalCut int runNumber RNG {start} {end}")

    nominal_file_text = nominal_file_text.replace(
        "BASIC_CONFIG_PATH_HERE",
        os.path.join(TOP_LEVEL_DIR, basic_filename))

    # make blocks
    nominal_file_text = nominal_file_text.replace(
        "SELECTIONS_HERE",
        make_selection_blocks(single, year, period))

    if single:
        nominal_filename = SM_NOMINAL_CONFIG_TEMPLATE
    else:
        nominal_filename = ML_NOMINAL_CONFIG_TEMPLATE
    with open(nominal_filename, "w", encoding="utf-8") as nominal_file:
        nominal_file.write(nominal_file_text)

    return nominal_filename