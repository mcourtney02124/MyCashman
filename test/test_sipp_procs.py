#!/usr/bin/env python3
# Copyright (c) 2018 Meredith Courtney All rights reserved.

"""
This module provides tests for executing sipp scripts (Sipp module)

"""

import os.path
import time
import pytest
from subprocess import TimeoutExpired

from src.sipp_procs import SippServer, SippClient
from src.sipp_utils import no_failed_calls, how_many_success, cleanup_screen_log, empty_screen_log


def test_create_default_server():
    """Create a default SippServer object, do we get the expected data in the object?"""

    p = SippServer()
    assert p.script == "uas.xml"
    assert p.port == "5060"
    assert p.command == ""
    assert p.pid == 0


def test_create_default_client():
    """Create a default SippClient object, do we get the expected data in the object?"""

    p = SippClient()
    assert p.script == "uac.xml"
    assert p.port == "6060"
    assert p.command == ""
    assert p.pid == 0
    assert p.target == "127.0.0.1"
    assert p.rport == "5060"


def test_launch_default_server():
    """Make a default SippServer and launch it, do we get the expected output."""

    p = SippServer()
    sipp_server_proc = SippServer.launch(p)
    time.sleep(5)
    try:
        outs, errs = sipp_server_proc.communicate(input="q", timeout=15)
        print ("shutdown successful")
        print (outs)
        print (errs)
    except TimeoutExpired:
        sipp_server_proc.kill()
        outs, errs = sipp_server_proc.communicate()
        print ("timed out")
        print (outs)
        print (errs)


    # The script ran, took no calls - this may mean the screen log file is null, and there was a clean manual shutdown.
    if empty_screen_log(p.script, p.pid):
        assert True
    else:
        assert no_failed_calls(p.script, p.pid)
    cleanup_screen_log(p.script, p.pid)


def test_launch_server_options():
    """Make and launch a non-default SippServer ."""
    p = SippServer(script="uas_ivr.xml", port=7070, command="-m 1")
    assert p.script == "uas_ivr.xml"
    assert p.port == "7070"
    assert p.command == "-m 1"
    sipp_server_proc = SippServer.launch(p)
    time.sleep(5)
    try:
        outs, errs = sipp_server_proc.communicate(input="q", timeout=15)
    except TimeoutExpired:
        sipp_server_proc.kill()
        outs, errs = sipp_server_proc.communicate()

    # The script ran, took no calls - this may mean the screen log file is null, and there was a clean manual shutdown.
    if empty_screen_log(p.script, p.pid):
        assert True
    else:
        assert no_failed_calls(p.script, p.pid)
    cleanup_screen_log(p.script, p.pid)


class TestSippRunCalls:
    ps = SippServer()
    sipp_server_proc = None

    def setup_method(self, method):
        """ Make and launch server. """
        TestSippRunCalls.sipp_server_proc = SippServer.launch(TestSippRunCalls.ps)
        time.sleep(2)

    def teardown_method(self, method):
        """ Make sure server is down. """
        try:
            outs, errs = TestSippRunCalls.sipp_server_proc.communicate(input="q", timeout=10)
        except TimeoutExpired:
            TestSippRunCalls.sipp_server_proc.kill()
            outs, errs = TestSippRunCalls.sipp_server_proc.communicate()
            #print(outs)
            #print(errs)
            #pytest.fail('problem stopping sipp server')
        cleanup_screen_log(TestSippRunCalls.ps.script, TestSippRunCalls.ps.pid)

    def test_run_1_call(self):
        """The setUp will launch server, make and launch client to run 1 call, report 1 successful call."""

        pc = SippClient(target="localhost", command="-m 1")
        sipp_client_proc = SippClient.launch(pc)
        time.sleep(12)
        # at this point,
        try:
            outs, errs = sipp_client_proc.communicate(input="q", timeout=10)
        except TimeoutExpired:
            sipp_client_proc.kill()
            outs, errs = sipp_client_proc.communicate()

        assert how_many_success(pc.script, pc.pid) == 1

        cleanup_screen_log(pc.script, pc.pid)

    def test_run_3_cps(self):
        """The setUp will launch server, make and launch client to run 30 calls at 3 calls per second, report 30 successful calls."""

        pc = SippClient(target="localhost", command="-r 3 -m 30")
        sipp_client_proc = SippClient.launch(pc)
        time.sleep(15)
        # at this point,
        try:
            outs, errs = sipp_client_proc.communicate(input="q", timeout=10)
        except TimeoutExpired:
            sipp_client_proc.kill()
            outs, errs = sipp_client_proc.communicate()
            #print(outs)
            #print(errs)
            #pytest.fail('problem stopping sipp client')


        assert how_many_success(pc.script, pc.pid) == 30

        cleanup_screen_log(pc.script, pc.pid)

