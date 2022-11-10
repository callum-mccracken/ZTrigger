"""Module for making systematic variation configs."""
from constants import SM_VAR_CONFIG_PATH_FMT,\
    ML_VAR_CONFIG_PATH_FMT

def new_pt_from_cut_line(single, line: str, return_original=False):
    """Given a cut line, return the new pt, i.e. if """
    original_pt = line.split("probe_pt > ")[-1]
    pt_num = float(line.split("probe_pt > ")[-1])
    if single:
        if pt_num==27.3:
            new_pt = 40.0
        elif pt_num==52.5:
            new_pt = 70.0
        else:
            new_pt = pt_num + 5  # TODO is this how I should deal with this?
    else:
        new_pt = pt_num + 5  # different bc of single vs multi turn-on curves
    if return_original:
        return original_pt, new_pt
    return new_pt


def make_variation_config(nominal_template, variation, year, period, single):
    """Make a systematic variation config file."""
    # get template text
    with open(nominal_template, "r", encoding="utf-8") as variation_file:
        var_file_text = variation_file.read()

    # make edits based on variation
    if variation == "nominal":
        var_file_text = var_file_text.replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "")
    elif variation == "dphill":
        var_file_text = var_file_text.replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "ProbeCut float dilep_dphi |<| 3.0426\n")
    elif variation == "isoTight":
        var_file_text = var_file_text.replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "GlobalCut bool probe_matched_IsoFCTight = 1\n")
    elif variation == "isoTightTrackOnly":
        var_file_text = var_file_text.replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "GlobalCut bool probe_matched_IsoFCTightTrackOnly = 1\n")
    elif variation == "mll":
        var_file_text = var_file_text.replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "").replace(
                "ProbeCut floatGeV dilep_mll |RNG| 81.2 101.2",
                "ProbeCut floatGeV dilep_mll |RNG| 76.2 106.2")
    elif variation == "muneg":
        var_file_text = var_file_text.replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "GlobalCut float probe_q < 0.0\n")
    elif variation == "mupos":
        var_file_text = var_file_text.replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "GlobalCut float probe_q > 0.0\n")
    elif variation == "noIP":
        var_file_text = var_file_text.replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "").replace(
                "GlobalCut float z0SinTheta < 0.5\n",
                "").replace(
                    "GlobalCut D0Sig probe |<| 3\n",
                    "")
    elif variation == "nvtx_dw":
        var_file_text = var_file_text.replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "GlobalCut int PV_n < 19\n")
    elif variation == "nvtx_up":
        var_file_text = var_file_text.replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "GlobalCut int PV_n >= 19\n")
    elif variation == "ptdw":
        lines = var_file_text.splitlines(keepends=True)
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if "ProbeCut floatGeV probe_pt >" in line:
                new_pt = new_pt_from_cut_line(single, line)
                new_lines.append(
                    f"    ProbeCut floatGeV probe_pt <= {new_pt:.1f}\n")
        var_file_text = "".join(new_lines).replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "")
    elif variation == "ptup":
        lines = var_file_text.splitlines(keepends=True)
        new_lines = []
        for line in lines:
            if "ProbeCut floatGeV probe_pt >" in line:
                line_pt, new_pt = new_pt_from_cut_line(
                    single, line, return_original=True)
                new_lines.append(line.replace(line_pt, f"{new_pt:.1f}\n"))
            else:
                new_lines.append(line)

        var_file_text = "".join(new_lines).replace(
            "EXTRA_GLOBAL_CUTS_HERE\n",
            "")
        var_file_text = var_file_text.replace(
            "ProbeCut floatGeV probe_pt > 27.3",
            "ProbeCut floatGeV probe_pt > 40.0").replace(
                "ProbeCut floatGeV probe_pt > 52.5",
                "ProbeCut floatGeV probe_pt > 70.0")
    else:
        raise ValueError(f"Variation {variation} unaccounted for!")

    # save the file
    fmt = SM_VAR_CONFIG_PATH_FMT if single else ML_VAR_CONFIG_PATH_FMT
    var_filename = fmt.format(variation=variation, year=year, period=period)
    with open(var_filename, "w", encoding="utf-8") as variation_file:
        variation_file.write(var_file_text)
