from diffpy.utils.parsers import load_PDF_into_db, load_from_db, markup_PDF, apply_schema_to_file, markup_oneline
from diffpy.utils.parsers import loadData
from diffpy.utils.tests.testhelpers import datafile

import os
import filecmp

tests_dir = os.path.dirname(os.path.abspath(locals().get('__file__', 'file.py')))

targetjson = datafile('targetdb.json')

schemaname = datafile('strumining.json')
muload = datafile('loadmu.txt')
targetmu = datafile('targetmu.json')


def test_load_gr(tmp_path):
    # generate json and apply schema
    generatedjson = tmp_path / "generated_db.json"
    tddbload_list = os.listdir(os.path.join(tests_dir, "testdata", "dbload"))
    tddbload_list.sort()
    for headerfile in tddbload_list:
        headerfile = os.path.join(tests_dir, "testdata", "dbload", headerfile)
        hdata = loadData(headerfile, headers=True)
        rv = loadData(headerfile)
        db_data = load_PDF_into_db(generatedjson, headerfile, hdata, rv, show_path=False)
    apply_schema_to_file(generatedjson, schemaname, multiple_entries=True)
    markup_oneline(generatedjson)

    # compare to target
    # first compare if base data is same
    import json
    target_db_data = load_from_db(targetjson)
    assert target_db_data == db_data
    # then compare file structure/organization
    assert filecmp.cmp(generatedjson, targetjson)


def test_markup_gr(tmp_path):
    # put into json and apply schema
    generatedmu = tmp_path / "generated_markup.json"
    hdata = loadData(muload, headers=True)
    rv = loadData(muload)
    data = markup_PDF(hdata, rv, generatedmu)
    apply_schema_to_file(generatedmu, schemaname)
    markup_oneline(generatedmu)

    # check against target
    # first compare data is same
    target_data = load_from_db(targetmu)
    assert target_data == data
    # then compare structure
    assert filecmp.cmp(generatedmu, targetmu)
