from diffpy.utils.parsers import load_PDF_into_db, markup_PDF, apply_schema
from diffpy.utils.parsers import loadData
from diffpy.utils.tests.testhelpers import datafile

import os
import filecmp

tests_dir = os.path.dirname(os.path.abspath(locals().get('__file__', 'file.py')))

generatedjson = datafile('tljson.json')
targetjson = datafile('targetdb.json')

schemaname = datafile('strumining.json')
muload = datafile('loadmu.txt')
generatedmu = datafile('tmujson.json')
targetmu = datafile('targetmu.json')


def test_load_gr():
    # generate json and apply schema
    tddbload_list = os.listdir(os.path.join(tests_dir, "testdata", "dbload"))
    tddbload_list.sort()
    print(tddbload_list)
    for headerfile in tddbload_list:
        headerfile = os.path.join(tests_dir, "testdata", "dbload", headerfile)
        hdata, rv = loadData(headerfile, headers=True)
        load_PDF_into_db(generatedjson, headerfile, hdata, rv, show_path=False)
    apply_schema(generatedjson, schemaname, multiple_entries=True)

    # compare to target
    assert filecmp.cmp(generatedjson, targetjson)

    # cleanup
    os.remove(generatedjson)


def test_markup_gr():
    # put into json and apply schema
    hdata, rv = loadData(muload, headers=True)
    markup_PDF(generatedmu, hdata, rv)
    apply_schema(generatedmu, schemaname)

    # check against target
    assert filecmp.cmp(generatedmu, targetmu)

    # cleanup
    os.remove(generatedmu)
