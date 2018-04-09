# Copyright (c) 2018 Meredith Courtney All rights reserved.

"""
This module provides non-REST tests for the MyCashman application, invoked from the IVR (aka sipp scripts)
Run this immediately after

"""
import time
from subprocess import TimeoutExpired
import pytest
from src.sipp_procs import SippClient

def test_ivr_balance():
    """ Trigger the sipp client script via the REST API, to work around server not reading port 5060 unless app launches client. """

    "pytest.main("test/test_MyCashman_ivr_trigger_balance.tavern.yaml")

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


