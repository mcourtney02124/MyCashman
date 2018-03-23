#!/usr/bin/env python3
# Copyright (c) 2018 Meredith Courtney All rights reserved.

"""
This module provides support for executing sipp scripts located in the data directory.

"""
import shlex
import subprocess

#myPath = '/Users/Meredith/PycharmProjects/MyCashman/data/'
myPath = './data/'

class SippServer:

    def __init__(self, script="uas.xml", port=5060, command=""):
        self.script = script
        self.port = str(port)
        self.command = command
        self.pid = 0

    def launch(self):
        moreArgs = shlex.split(self.command)
        global myPath
        args = ['sipp', '-sf', myPath + self.script, '-p', self.port, '-trace_screen'] + moreArgs[:]
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
        self.pid = p.pid
        return p


class SippClient(SippServer):

    def __init__(self, script="uac.xml", target="127.0.0.1", lport=6060, rport=5060, command=""):
        super().__init__(script, lport, command)
        self.target = target
        self.rport = str(rport)

    def launch(self):
        moreArgs = shlex.split(self.command)
        global myPath
        args = ['sipp', self.target + ":" + self.rport, '-sf', myPath + self.script, '-p', self.port,
                '-trace_screen'] + moreArgs[:]
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
        self.pid = p.pid
        return p


