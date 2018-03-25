# Copyright (c) 2018 Meredith Courtney All rights reserved.

"""
This module provides non-REST tests for the MyCashman application, invoked from the IVR (aka sipp scripts)

"""
import time
from subprocess import TimeoutExpired
import pytest
from src.sipp_procs import SippClient

def test_ivr_balance():

    uac = SippClient(script = "uac_g711_info1.xml", target = "localhost", command="-m 1")
    clientProc = SippClient.launch(uac)
    time.sleep(15)
    # at this point, make sure the client completed

    try:
        outs, errs = clientProc.communicate(input="q", timeout=10)
    except TimeoutExpired:
        clientProc.kill()
        outs, errs = clientProc.communicate()
        print(outs)
        print(errs)
        pytest.fail('problem with sipp client')

    found_balance = False
    fh = None
    try:
        fh = open("transaction.log", encoding = "utf8")
        for lino, line in enumerate(fh, start=1):
            line = line.rstrip()
            if line.find("ivr") > -1:
                found_balance = True
                break
    except EnvironmentError as err:
            pytest.fail('problem with transaction log')
    finally:
        if fh is not None:
            fh.close()
    assert found_balance == True


