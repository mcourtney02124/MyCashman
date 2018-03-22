#!/usr/bin/env python3
# Copyright (c) 2018 Meredith Courtney All rights reserved.

"""
This module provides unit tests for utility functions used with sipp execution (the sipp_procs module).

"""

import os.path
import shutil
import pytest

myPath = '/Users/Meredith/PycharmProjects/MyCashman/data/'

from src.sipp_utils import no_failed_calls, how_many_success, cleanup_screen_log, empty_screen_log

"""Tests for `sipp_utils.py`, these are assumed to be executed from top level directory."""


def test_no_failed_calls():
    """no_failed_calls: check a saved sipp screen log for a run that had 0 failed calls."""
    script = "test_data.xml"
    pid = 3875
    assert no_failed_calls(script, pid)


def test_how_many_success():
    """how_many_success: check a saved sipp screen log for a run that had 10 successful calls."""
    script = "test_data.xml"
    pid = 3876
    assert how_many_success(script, pid) == 10


def test_cleanup_screen_log():
    """cleanup:screen_log: delete sipp screen log from the data directory, identified by script name and process id."""
    file_path = myPath + 'test_data_3877_screen.log'
    try:
        shutil.copy(myPath + 'test_data_3876_screen.log', file_path)
    except IOError:
        pytest.fail('could not copy test log file')
        return

    script = "test_data.xml"
    pid = 3877
    cleanup_screen_log(script, pid)
    assert not os.path.isfile(file_path)


def test_empty_screen_log():
    """ File must exist and have size 0. """
    script = "test_data.xml"
    pid = 3876
    assert not empty_screen_log(script, pid)
    pid = 0
    assert not empty_screen_log(script, pid)
    pid = 3878
    assert empty_screen_log(script, pid)
