# Copyright (c) 2018 Meredith Courtney All rights reserved.

"""
This module provides non-REST tests for the MyCashman application
It assumes the REST tests have already run, to set up initial conditions
At present these are skeleton tests, so I can learn how to work with the infrastruture

"""

def test_pizza():
    found_pizza = False
    fh = None
    try:
        fh = open("/Users/Meredith/PycharmProjects/MyCashman/transaction.log", encoding = "utf8")
        for lino, line in enumerate(fh, start=1):
            line = line.rstrip()
            if line.find("pizza"):
                found_pizza = True
                break
    except EnvironmentError as err:
            print (err)
    finally:
        if fh is not None:
            fh.close()
    assert found_pizza == True
