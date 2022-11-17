"""Module storing info about which triggers were used when."""
import numpy as np

def get_ors(trigger_list):
    """
    Return the OR combinations we need to consider.

    THIS IS ONLY TO BE USED WITH SINGLE MUON TRIGGERS,
    PATTERN MATCHING MAY NOT WORK WITH MULTI-LEG ONES!

    (I assume triggers have names like HLT_muX_Y)

    Example trigger list:
        ["HLT_mu20_iloose_L1MU15",
        "HLT_mu40",
        "HLT_mu60_0eta105_msonly"]

    We also want these:
    - HLT_mu20_iloose_L1MU15_OR_HLT_mu40
    - HLT_mu20_iloose_L1MU15_OR_HLT_mu60_0eta105_msonly
    - HLT_mu40_OR_HLT_mu60_0eta105_msonly

    I.e. take all unique pairings where the lower-pt muon goes first.
    """
    def get_pt(trigger_name):
        """Given a single-muon trigger name, return the muon pt."""
        trigger_name = str(trigger_name)
        return int(trigger_name.split("_")[1].replace("mu", ""))

    # sort triggers by pt
    pt_list = np.array([get_pt(trig) for trig in trigger_list])
    pt_order = np.argsort(pt_list)
    triggers_pt_sorted = np.array(trigger_list)[pt_order]

    or_triggers = []
    for i, trig_i in enumerate(triggers_pt_sorted[:-1]):
        for trig_j in triggers_pt_sorted[i+1:]:
            or_triggers.append(trig_i+"_OR_"+trig_j)
    return or_triggers


TRIGGERS = {
    # do I need to worry about only using C2-C4 and D3-D6
    2015: {
        "ANY": {
            "SINGLE": [
                "HLT_mu20_iloose_L1MU15",
                "HLT_mu40",
                "HLT_mu60_0eta105_msonly"
            ],
            "MULTI": [
                "HLT_2mu10",
                "HLT_3mu6",
                "HLT_3mu6_msonly",
                "HLT_mu18_2mu4noL1",
                "HLT_mu18_mu8noL1"
            ]
        }
    },
    2016: {  # do I need to worry about stuff like split periods
        "A": {
            "SINGLE": [
                "HLT_mu24_iloose",
                "HLT_mu24_ivarloose",
                "HLT_mu40",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu10",
                "HLT_2mu10_nomucomb",
                "HLT_mu20_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu4",
                "HLT_mu6_2mu4",
                "HLT_mu20_nomucomb_mu6noL1_nscan03",
                "HLT_mu11_nomucomb_2mu4noL1_nscan03_L1MU11_2MU6",
                "HLT_mu20_msonly_mu10noL1_msonly_nscan05_noComb",
                "HLT_mu11_nomucomb_2mu4noL1_nscan03_L1MU11_2MU6_bTau",
                "HLT_mu11_nomucomb_mu6noL1_nscan03_L1MU11_2MU6_bTau",
                "HLT_mu6_nomucomb_2mu4_nomucomb_bTau_L1MU6_3MU4",
                "HLT_2mu6_nomucomb_mu4_nomucomb_bTau_L12MU6_3MU4"
            ]
        },
        "B": {
            "SINGLE": [
                "HLT_mu24_ivarmedium",
                "HLT_mu24_imedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_2mu14_nomucomb",
                "HLT_mu20_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6",
                "HLT_mu6_2mu4",
                "HLT_mu20_nomucomb_mu6noL1_nscan03",
                "HLT_mu11_nomucomb_2mu4noL1_nscan03_L1MU11_2MU6",
                "HLT_mu20_msonly_mu10noL1_msonly_nscan05_noComb",
                "HLT_mu11_nomucomb_2mu4noL1_nscan03_L1MU11_2MU6_bTau",
                "HLT_mu11_nomucomb_mu6noL1_nscan03_L1MU11_2MU6_bTau",
                "HLT_mu6_nomucomb_2mu4_nomucomb_bTau_L1MU6_3MU4",
                "HLT_2mu6_nomucomb_mu4_nomucomb_bTau_L12MU6_3MU4"
            ]
        },
        "C": {
            "SINGLE": [
                "HLT_mu24_ivarmedium",
                "HLT_mu24_imedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_2mu14_nomucomb",
                "HLT_mu20_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6",
                "HLT_mu6_2mu4",
                "HLT_mu20_nomucomb_mu6noL1_nscan03",
                "HLT_mu11_nomucomb_2mu4noL1_nscan03_L1MU11_2MU6",
                "HLT_mu20_msonly_mu10noL1_msonly_nscan05_noComb",
                "HLT_mu11_nomucomb_2mu4noL1_nscan03_L1MU11_2MU6_bTau",
                "HLT_mu11_nomucomb_mu6noL1_nscan03_L1MU11_2MU6_bTau",
                "HLT_mu6_nomucomb_2mu4_nomucomb_bTau_L1MU6_3MU4",
                "HLT_2mu6_nomucomb_mu4_nomucomb_bTau_L12MU6_3MU4"
            ]
        },
        "D1D3": {  # first part of D = same as B/C
            "SINGLE": [
                "HLT_mu24_ivarmedium",
                "HLT_mu24_imedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_2mu14_nomucomb",
                "HLT_mu20_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6",
                "HLT_mu6_2mu4",
                "HLT_mu20_nomucomb_mu6noL1_nscan03",
                "HLT_mu11_nomucomb_2mu4noL1_nscan03_L1MU11_2MU6",
                "HLT_mu20_msonly_mu10noL1_msonly_nscan05_noComb",
                "HLT_mu11_nomucomb_2mu4noL1_nscan03_L1MU11_2MU6_bTau",
                "HLT_mu11_nomucomb_mu6noL1_nscan03_L1MU11_2MU6_bTau",
                "HLT_mu6_nomucomb_2mu4_nomucomb_bTau_L1MU6_3MU4",
                "HLT_2mu6_nomucomb_mu4_nomucomb_bTau_L12MU6_3MU4"
            ]
        },
        "D4D8": {  # the second part of D = same as E
            "SINGLE": [
                "HLT_mu24_ivarmedium",
                "HLT_mu26_ivarmedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_mu20_mu8noL1",
                "HLT_mu22_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6_msonly"
            ]
        },
        "E": {  # did I understand the slash after ivarmedium correctly?
            "SINGLE": [
                "HLT_mu24_ivarmedium",
                "HLT_mu26_ivarmedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_mu20_mu8noL1",
                "HLT_mu22_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6_msonly"
            ]
        },
        "F": {
            "SINGLE": [
                "HLT_mu26_ivarmedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_mu22_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6_msonly"
            ]
        },
        "G": {  # only the first half of G
            "SINGLE": [
                "HLT_mu26_ivarmedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_mu22_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6_msonly"
            ]
        },
        "H": {
            "SINGLE": [
                "HLT_mu26_ivarmedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_mu22_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6_msonly"
            ]
        },
        "I": {  # only the first half of I
            "SINGLE": [
                "HLT_mu26_ivarmedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_mu22_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6_msonly"
            ]
        },
        "K": {
            "SINGLE": [
                "HLT_mu26_ivarmedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_mu22_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6_msonly"
            ]
        },
        "L": {
            "SINGLE": [
                "HLT_mu26_ivarmedium",
                "HLT_mu50"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_mu22_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6_msonly"
            ]
        }
    },
    2017: {
        "ANY": {
            "SINGLE": [
                "HLT_mu26_ivarmedium",
                "HLT_mu50",
                "HLT_mu60_0eta105_msonly"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_mu22_mu8noL1",
                "HLT_mu22_mu8noL1_calotag_0eta010",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6",
                "HLT_3mu6_msonly",
                "HLT_4mu4"
            ]
        }
    },
    2018: {
        "ANY": {
            "SINGLE": [
                "HLT_mu26_ivarmedium",
                "HLT_mu50",
                # "HLT_mu26_ivarmedium_OR_HLT_mu50",
                "HLT_mu60_0eta105_msonly"
            ],
            "MULTI": [
                "HLT_2mu14",
                "HLT_mu22_mu8noL1",
                "HLT_mu20_2mu4noL1",
                "HLT_3mu6"
            ]
        }
    }
}


# add OR combinations for single-muon triggers
for yr in TRIGGERS:
    year_dict = TRIGGERS[yr]
    for prd in year_dict:
        period_dict = year_dict[prd]
        single_triggers = period_dict["SINGLE"]
        single_triggers += get_ors(single_triggers)
        period_dict["SINGLE"] = single_triggers


SINGLE_TRIGGER_TEMPLATE = """
New_MatchSelection
    MatchName {trigger_name}
    Cut bool probe_matched_{trigger_name} = 1
End_MatchSelection
"""

OR_TRIGGER_TEMPLATE = """
New_MatchSelection
    MatchName {trigger_name}
    MatchCombCut OR
        Cut bool probe_matched_{trigger_2} = 1
        Cut bool probe_matched_{trigger_1} = 1
    End_CombCut
End_MatchSelection
"""

def triggers_in_period(single, year, period):
    """Return a list of triggers in a given period"""
    triggers_in_year = TRIGGERS[year]
    if period in triggers_in_year.keys():
        trigs_in_period = triggers_in_year[period]
    elif "ANY" in triggers_in_year.keys():
        trigs_in_period = triggers_in_year["ANY"]
    else:
        raise KeyError(period)
    trigs = trigs_in_period["SINGLE" if single else "MULTI"]
    return trigs

def get_matches_text(single, year, period):
    """single = True if you want SINGLE triggers, else MULTI triggers"""
    trigs = triggers_in_period(single, year, period)
    matches_text = ""
    for trigger in trigs:
        if "_OR_" in trigger:
            trigger_1, trigger_2 = trigger.split("_OR_")
            matches_text += OR_TRIGGER_TEMPLATE.format(
                trigger_name=trigger, trigger_1=trigger_1, trigger_2=trigger_2)
        else:
            matches_text += SINGLE_TRIGGER_TEMPLATE.format(
                trigger_name=trigger)
    return matches_text
