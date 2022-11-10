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

def triggers_in_period(single: bool, year: int, period: str):
    """Return a list of triggers in a given period"""
    triggers_in_year = TRIGGERS[year]
    if period in triggers_in_year.keys():
        trigs_in_period = triggers_in_year[period]
    elif "ANY" in triggers_in_year.keys():
        trigs_in_period = triggers_in_year["ANY"]
    else:
        raise KeyError(period)
    triggers = trigs_in_period["SINGLE" if single else "MULTI"]
    return triggers

def get_matches_text(single, year, period):
    """single = True if you want SINGLE triggers, else MULTI triggers"""
    triggers = triggers_in_period(single, year, period)
    matches_text = ""
    for trigger in triggers:
        if "_OR_" in trigger:
            trigger_1, trigger_2 = trigger.split("_OR_")
            matches_text += OR_TRIGGER_TEMPLATE.format(
                trigger_name=trigger, trigger_1=trigger_1, trigger2=trigger_2)
        else:
            matches_text += SINGLE_TRIGGER_TEMPLATE.format(trigger_name=trigger)
    return matches_text
