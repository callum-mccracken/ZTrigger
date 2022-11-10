"""
Module to list run numbers for each period we care about.

The numbers here come from
[COMA](https://atlas-tagservices.cern.ch/tagservices/RunBrowser/runBrowserReport/rBR_Period_Report.php)
"""

# 2015
# using AllYear 13TeV data periods
# we can probably ignore cosmic runs, 5TeV runs,
# heavy ion / lead runs, commissioning, and beam splash periods, right?
# commented out some since they didn't appear in the trigger recommendations
# PERIOD_A_2015_START = 266904
# PERIOD_A_2015_END = 267639
# PERIOD_B_2015_START = 267358
# PERIOD_B_2015_END = 267599
PERIOD_C_2015_START = 270441  # trigger recs say only C2-C4
PERIOD_C_2015_END = 272531
PERIOD_D_2015_START = 276073  # trigger recs say D3-D6
PERIOD_D_2015_END = 276954
PERIOD_E_2015_START = 278727
PERIOD_E_2015_END = 279928
PERIOD_F_2015_START = 279932
PERIOD_F_2015_END = 280422
PERIOD_G_2015_START = 280423
PERIOD_G_2015_END = 281075
PERIOD_H_2015_START = 281130
PERIOD_H_2015_END = 281411
# PERIOD_I_2015_START = 281662
# PERIOD_I_2015_END = 282482
PERIOD_J_2015_START = 282625
PERIOD_J_2015_END = 284484

# 2016
# again using AllYear 13TeV data periods: A-L no J (J is in a different spot)
# ignoring the same things as before (also AFP whatever that means?)
PERIOD_A_2016_START = 296939
PERIOD_A_2016_END = 300287
PERIOD_B_2016_START = 300345
PERIOD_B_2016_END = 300908
PERIOD_C_2016_START = 301912
PERIOD_C_2016_END = 302393
PERIOD_D1D3_2016_START = 302737
PERIOD_D1D3_2016_END = 302872
PERIOD_D4D8_2016_START = 302919
PERIOD_D4D8_2016_END = 303560
PERIOD_E_2016_START = 303638
PERIOD_E_2016_END = 303892
PERIOD_F_2016_START = 303943
PERIOD_F_2016_END = 304494
PERIOD_G_2016_START = 305291  # trigger recs change G2-G3
PERIOD_G_2016_END = 306714
PERIOD_H_2016_START = 305359  # I comes before H in COMA
PERIOD_H_2016_END = 310216
PERIOD_I_2016_START = 307124  # trigger recs change I3-I4
PERIOD_I_2016_END = 308084
PERIOD_K_2016_START = 309311
PERIOD_K_2016_END = 309759
PERIOD_L_2016_START = 310015
PERIOD_L_2016_END = 311481

# 2017
# again using AllYear 13TeV data periods, A-N no J, L, M
# ignoring period G since it had no end number and said "not for physics"
# ignoring the same things as before
# PERIOD_A_2017_START = 324320
# PERIOD_A_2017_END = 325558
PERIOD_B_2017_START = 325713
PERIOD_B_2017_END = 328393
PERIOD_C_2017_START = 329385
PERIOD_C_2017_END = 330470
PERIOD_D_2017_START = 330857
PERIOD_D_2017_END = 332304
PERIOD_E_2017_START = 332720
PERIOD_E_2017_END = 334779
PERIOD_F_2017_START = 334842
PERIOD_F_2017_END = 335290
PERIOD_H_2017_START = 336497
PERIOD_H_2017_END = 336782
PERIOD_I_2017_START = 336832
PERIOD_I_2017_END = 337833
PERIOD_K_2017_START = 338183
PERIOD_K_2017_END = 340453
PERIOD_N_2017_START = 341257
PERIOD_N_2017_END = 341649

# 2018
# again using AllYear 13TeV data periods
# ignoring the same things as before (also BSRT)
# ignoring period R since it doesn't seem to have an end number
# PERIOD_A_2018_START = 348197  # B comes before A in COMA
# PERIOD_A_2018_END = 348836
PERIOD_B_2018_START = 348885
PERIOD_B_2018_END = 349533
PERIOD_C_2018_START = 349534
PERIOD_C_2018_END = 350220
PERIOD_D_2018_START = 350310
PERIOD_D_2018_END = 352107
PERIOD_E_2018_START = 352123  # F comes before E in COMA
PERIOD_E_2018_END = 352137
PERIOD_F_2018_START = 352274
PERIOD_F_2018_END = 352514
PERIOD_G_2018_START = 354107
PERIOD_G_2018_END = 354494
PERIOD_H_2018_START = 354826
PERIOD_H_2018_END = 355224
PERIOD_I_2018_START = 355261
PERIOD_I_2018_END = 355273
PERIOD_J_2018_START = 355331
PERIOD_J_2018_END = 355468
PERIOD_K_2018_START = 355529
PERIOD_K_2018_END = 356259
PERIOD_L_2018_START = 357050
PERIOD_L_2018_END = 359171
PERIOD_M_2018_START = 359191
PERIOD_M_2018_END = 360414
PERIOD_N_2018_START = 361635
PERIOD_N_2018_END = 361696
PERIOD_O_2018_START = 361738
PERIOD_O_2018_END = 363400
PERIOD_Q_2018_START = 363664
PERIOD_Q_2018_END = 364292

RUN_NUMBERS = {
    # I've only left the ones in Robin's skype message
    2015: {
        # "A": {"START": PERIOD_A_2015_START, "END": PERIOD_A_2015_END},
        # "B": {"START": PERIOD_B_2015_START, "END": PERIOD_B_2015_END},
        # "C": {"START": PERIOD_C_2015_START, "END": PERIOD_C_2015_END},
        "D": {"START": PERIOD_D_2015_START, "END": PERIOD_D_2015_END},
        "E": {"START": PERIOD_E_2015_START, "END": PERIOD_E_2015_END},
        "F": {"START": PERIOD_F_2015_START, "END": PERIOD_F_2015_END},
        "G": {"START": PERIOD_G_2015_START, "END": PERIOD_G_2015_END},
        "H": {"START": PERIOD_H_2015_START, "END": PERIOD_H_2015_END},
        # "I": {"START": PERIOD_I_2015_START, "END": PERIOD_I_2015_END},
        "J": {"START": PERIOD_J_2015_START, "END": PERIOD_J_2015_END},
    },
    2016: {
        "A": {"START": PERIOD_A_2016_START, "END": PERIOD_A_2016_END},
        "B": {"START": PERIOD_B_2016_START, "END": PERIOD_B_2016_END},
        "C": {"START": PERIOD_C_2016_START, "END": PERIOD_C_2016_END},
        "D1D3": {"START": PERIOD_D1D3_2016_START, "END": PERIOD_D1D3_2016_END},
        "D4D8": {"START": PERIOD_D4D8_2016_START, "END": PERIOD_D4D8_2016_END},
        "E": {"START": PERIOD_E_2016_START, "END": PERIOD_E_2016_END},
        "F": {"START": PERIOD_F_2016_START, "END": PERIOD_F_2016_END},
        "G": {"START": PERIOD_G_2016_START, "END": PERIOD_G_2016_END},
        # "H": {"START": PERIOD_H_2016_START, "END": PERIOD_H_2016_END},
        "I": {"START": PERIOD_I_2016_START, "END": PERIOD_I_2016_END},
        "K": {"START": PERIOD_K_2016_START, "END": PERIOD_K_2016_END},
        "L": {"START": PERIOD_L_2016_START, "END": PERIOD_L_2016_END},
    },
    2017: {
        # "A": {"START": PERIOD_A_2017_START, "END": PERIOD_A_2017_END},
        "B": {"START": PERIOD_B_2017_START, "END": PERIOD_B_2017_END},
        "C": {"START": PERIOD_C_2017_START, "END": PERIOD_C_2017_END},
        "D": {"START": PERIOD_D_2017_START, "END": PERIOD_D_2017_END},
        "E": {"START": PERIOD_E_2017_START, "END": PERIOD_E_2017_END},
        "F": {"START": PERIOD_F_2017_START, "END": PERIOD_F_2017_END},
        "H": {"START": PERIOD_H_2017_START, "END": PERIOD_H_2017_END},
        "I": {"START": PERIOD_I_2017_START, "END": PERIOD_I_2017_END},
        "K": {"START": PERIOD_K_2017_START, "END": PERIOD_K_2017_END},
        # "L": {"START": PERIOD_N_2017_START, "END": PERIOD_N_2017_END},
    },
    2018: {
        # "A": {"START": PERIOD_A_2018_START, "END": PERIOD_A_2018_END},
        "B": {"START": PERIOD_B_2018_START, "END": PERIOD_B_2018_END},
        "C": {"START": PERIOD_C_2018_START, "END": PERIOD_C_2018_END},
        "D": {"START": PERIOD_D_2018_START, "END": PERIOD_D_2018_END},
        # "E": {"START": PERIOD_E_2018_START, "END": PERIOD_E_2018_END},
        "F": {"START": PERIOD_F_2018_START, "END": PERIOD_F_2018_END},
        # "G": {"START": PERIOD_G_2018_START, "END": PERIOD_G_2018_END},
        # "H": {"START": PERIOD_H_2018_START, "END": PERIOD_H_2018_END},
        "I": {"START": PERIOD_I_2018_START, "END": PERIOD_I_2018_END},
        # "J": {"START": PERIOD_J_2018_START, "END": PERIOD_J_2018_END},
        "K": {"START": PERIOD_K_2018_START, "END": PERIOD_K_2018_END},
        "L": {"START": PERIOD_L_2018_START, "END": PERIOD_L_2018_END},
        # "M": {"START": PERIOD_M_2018_START, "END": PERIOD_M_2018_END},
        # "N": {"START": PERIOD_N_2018_START, "END": PERIOD_N_2018_END},
        "O": {"START": PERIOD_O_2018_START, "END": PERIOD_O_2018_END},
        "Q": {"START": PERIOD_Q_2018_START, "END": PERIOD_Q_2018_END},
    }
}

def periods(year):
    """Get the list of periods in a year."""
    return RUN_NUMBERS[year].keys()
