# Copyright (c) 2018 Meredith Courtney All rights reserved.

"""
This module provides non-REST tests for the MyCashman application.
It assumes the REST tests have already run, to set up initial conditions.
It also assumes execution from the top level MyCashman directory.
At present these are skeleton tests, so I can learn how to work with the infrastruture.

"""
import time
from subprocess import TimeoutExpired
from src.sipp_procs import SippClient

def test_pizza():
    found_pizza = False
    fh = None
    try:
        fh = open("transaction.log", encoding = "utf8")
        for lino, line in enumerate(fh, start=1):
            line = line.rstrip()
            if line.find("pizza") > -1:
                found_pizza = True
                break
    except EnvironmentError as err:
            print (err)
    finally:
        if fh is not None:
            fh.close()
    assert found_pizza == True

def test_covert():
    found_covert = False
    fh = None
    try:
        fh = open("transaction.log", encoding = "utf8")
        for lino, line in enumerate(fh, start=1):
            line = line.rstrip()
            if line.find("covert") > -1:
                found_covert = True
                break
    except EnvironmentError as err:
            print (err)
    finally:
        if fh is not None:
            fh.close()
    assert found_covert == True

def test_balance():
    found_balance = False
    fh = None
    try:
        fh = open("transaction.log", encoding = "utf8")
        for lino, line in enumerate(fh, start=1):
            line = line.rstrip()
            if line.find("Balance inquiry") > -1:
                found_balance = True
                break
    except EnvironmentError as err:
            print (err)
    finally:
        if fh is not None:
            fh.close()
    assert found_balance == True



