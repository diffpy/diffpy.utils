from diffpy.utils.pdfitc_helpers import strumining_processing
from diffpy.utils.parsers import load_PDF_into_db, markup_PDF, apply_schema
from diffpy.utils.parsers import loadData
from diffpy.utils.tests.testhelpers import datafile

import os
import filecmp

tests_dir = os.path.dirname(os.path.abspath(locals().get('__file__', 'file.py')))

nload = datafile("loadneutron.txt")
xload = datafile("loadxray.txt")

neutron_target = datafile("targetsmn.json")
xray_target = datafile("targetsmx.json")

neutron_generated = datafile("gensmn.json")
xray_generated = datafile("gensmx.json")

sm_schema = datafile("strumining.json")


def test_sm_preprocessing():
    # simple workflow for neutron data
    hddata, rv = loadData(nload, headers=True)
    hddata = strumining_processing(hddata)
    markup_PDF(neutron_generated, hddata, rv)
    apply_schema(neutron_generated, sm_schema)

    # simple workflow for xray data
    hddata, rv = loadData(xload, headers=True)
    hddata = strumining_processing(hddata)
    markup_PDF(xray_generated, hddata, rv)
    apply_schema(xray_generated, sm_schema)

    # check against target files
    assert filecmp.cmp(neutron_generated, neutron_target)
    assert filecmp.cmp(xray_generated, xray_target)

    # cleanup
    os.remove(neutron_generated)
    os.remove(xray_generated)
