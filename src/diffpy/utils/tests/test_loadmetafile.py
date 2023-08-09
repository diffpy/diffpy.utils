from diffpy.utils.parsers import serialize_data, deserialize_data, apply_schema_to_file, serial_oneline
from diffpy.utils.parsers import loadData
from diffpy.utils.tests.testhelpers import datafile

import os
import filecmp

tests_dir = os.path.dirname(os.path.abspath(locals().get('__file__', 'file.py')))

targetjson = datafile('targetjson.json')
schemaname = datafile('strumining.json')

muload = datafile('loadmu.txt')
targetmu = datafile('targetmu.json')


def test_load_gr(tmp_path):
    # generate json and apply schema
    generatedjson = tmp_path / "generated_serialization.json"
    tddbload_list = os.listdir(os.path.join(tests_dir, "testdata", "dbload"))
    tddbload_list.sort()
    for headerfile in tddbload_list:
        headerfile = os.path.join(tests_dir, "testdata", "dbload", headerfile)
        hdata = loadData(headerfile, headers=True)
        data_table = loadData(headerfile)
        db_data = serialize_data(headerfile, hdata, data_table, dt_colnames=['r', 'gr'],
                                 show_path=False, serial_file=generatedjson)
    apply_schema_to_file(generatedjson, schemaname, multiple_entries=True)
    serial_oneline(generatedjson)

    # compare to target
    # first compare if base data is same
    import json
    target_db_data = deserialize_data(targetjson)
    assert target_db_data == db_data
    # then compare file structure/organization
    assert filecmp.cmp(generatedjson, targetjson)


# FIXME: tests for REST API, remove after merge
def test_markup_gr(tmp_path):
    # put into json and apply schema
    generatedmu = tmp_path / "generated_markup.json"
    hdata = loadData(muload, headers=True)
    data_table = loadData(muload)
    data = serialize_data(muload, hdata, data_table, dt_colnames=['r', 'gr'], show_path=False).get('loadmu.txt')

    # compare data is same
    target_data = deserialize_data(targetmu)
    assert target_data == data
