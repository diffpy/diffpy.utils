def strumining_processing(sminputs: dict):
    """Process metadata dictionary before put into strumining.

    sminputs    -- Dictionary of strumining parameters (either read from loadData or given)
    """

    # preprocessing
    # FIXME: make lowercase and check string inputting

    # ensure stype either x-ray or neutron
    if "mode" in sminputs:
        stype = sminputs.pop("mode")
        if stype.lower in ["xray", "x-ray", "x"]:
            stype = "X"
        elif stype.lower in ["neutron", "n"]:
            stype = "N"
        sminputs.update({"stype": stype})
    if "stype" not in sminputs:
        raise Exception("Cannot find stype.")

    # ensure structure given
    if "composition" in sminputs:
        stru_str = sminputs.pop("composition")
        sminputs.update({"stru_str": stru_str})
    if "stru_str" not in sminputs:
        raise Exception("Cannot find stru_str.")

    # set default values
    defaults = {"rmin": 1.5, "rmax": 20, "qmin": 0, "qmax": 20, "spd": 0,
                "refinepos_option": "n", "mpi_option": "n", "db_option": "cod", "max_num": 1000}
    stype = sminputs.get("stype")
    if stype == "N":
        defaults.update({"qdamp": 0.02, "qbroad": 0.02})
    elif stype == "X":
        defaults.update({"qdamp": 0.04, "qbroad": 0.01})
    else:
        raise Exception("Improper stype.")
    for key in defaults.keys():
        if key not in sminputs:
            sminputs.update({key: defaults.get(key)})