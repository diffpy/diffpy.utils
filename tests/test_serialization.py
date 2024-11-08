import os

import numpy
import pytest

from diffpy.utils.parsers import deserialize_data, loadData, serialize_data
from diffpy.utils.parsers.custom_exceptions import ImproperSizeError, UnsupportedTypeError

tests_dir = os.path.dirname(os.path.abspath(locals().get("__file__", "file.py")))


def test_load_multiple(tmp_path, datafile):
    # Load test data
    targetjson = datafile("targetjson.json")
    generatedjson = tmp_path / "generated_serialization.json"

    tlm_list = os.listdir(os.path.join(tests_dir, "testdata", "dbload"))
    tlm_list.sort()
    generated_data = None
    for hfname in tlm_list:
        # gather data using loadData
        headerfile = os.path.normpath(os.path.join(tests_dir, "testdata", "dbload", hfname))
        hdata = loadData(headerfile, headers=True)
        data_table = loadData(headerfile)

        # check path extraction
        generated_data = serialize_data(headerfile, hdata, data_table, dt_colnames=["r", "gr"], show_path=True)
        assert headerfile == os.path.normpath(generated_data[hfname].pop("path"))

        # rerun without path information and save to file
        generated_data = serialize_data(
            headerfile,
            hdata,
            data_table,
            dt_colnames=["r", "gr"],
            show_path=False,
            serial_file=generatedjson,
        )

    # compare to target
    target_data = deserialize_data(targetjson)
    assert target_data == generated_data
    # ensure file saved properly
    assert target_data == deserialize_data(generatedjson, filetype=".json")


def test_exceptions(datafile):
    # Load test data
    wrongtype = datafile("wrong.type")
    loadfile = datafile("loadfile.txt")
    warningfile = datafile("generatewarnings.txt")
    nodt = datafile("loaddatawithheaders.txt")
    hdata = loadData(loadfile, headers=True)
    data_table = loadData(loadfile)

    # improper file types
    with pytest.raises(UnsupportedTypeError):
        serialize_data(loadfile, hdata, data_table, serial_file=wrongtype)
    with pytest.raises(UnsupportedTypeError):
        deserialize_data(wrongtype)

    # various dt_colnames inputs
    with pytest.raises(ImproperSizeError):
        serialize_data(loadfile, hdata, data_table, dt_colnames=["one", "two", "three is too many"])
    # check proper output
    normal = serialize_data(loadfile, hdata, data_table, dt_colnames=["r", "gr"])
    data_name = list(normal.keys())[0]
    r_list = normal[data_name]["r"]
    gr_list = normal[data_name]["gr"]
    # three equivalent ways to denote no column names
    missing_parameter = serialize_data(loadfile, hdata, data_table, show_path=False)
    empty_parameter = serialize_data(loadfile, hdata, data_table, show_path=False, dt_colnames=[])
    none_entry_parameter = serialize_data(loadfile, hdata, data_table, show_path=False, dt_colnames=[None, None])
    # check equivalence
    assert missing_parameter == empty_parameter
    assert missing_parameter == none_entry_parameter
    assert numpy.allclose(missing_parameter[data_name]["data table"], data_table)
    # extract a single column
    r_extract = serialize_data(loadfile, hdata, data_table, show_path=False, dt_colnames=["r"])
    gr_extract = serialize_data(loadfile, hdata, data_table, show_path=False, dt_colnames=[None, "gr"])
    incorrect_r_extract = serialize_data(loadfile, hdata, data_table, show_path=False, dt_colnames=[None, "r"])
    # check proper columns extracted
    assert numpy.allclose(gr_extract[data_name]["gr"], incorrect_r_extract[data_name]["r"])
    assert "r" not in gr_extract[data_name]
    assert "gr" not in r_extract[data_name] and "gr" not in incorrect_r_extract[data_name]
    # check correct values extracted
    assert numpy.allclose(r_extract[data_name]["r"], r_list)
    assert numpy.allclose(gr_extract[data_name]["gr"], gr_list)
    # no datatable
    nodt_hdata = loadData(nodt, headers=True)
    nodt_dt = loadData(nodt)
    no_dt = serialize_data(nodt, nodt_hdata, nodt_dt, show_path=False)
    nodt_data_name = list(no_dt.keys())[0]
    assert numpy.allclose(no_dt[nodt_data_name]["data table"], nodt_dt)

    # ensure user is warned when columns are overwritten
    hdata = loadData(warningfile, headers=True)
    data_table = loadData(warningfile)
    with pytest.warns(RuntimeWarning) as record:
        serialize_data(
            warningfile,
            hdata,
            data_table,
            show_path=False,
            dt_colnames=["c1", "c2", "c3"],
        )
    assert len(record) == 4
    for msg in record:
        assert "overwritten" in msg.message.args[0]
