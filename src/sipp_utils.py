#!/usr/bin/env python3
# Copyright (c) 2018 Meredith Courtney All rights reserved.

"""
This module provides utilities for use with execution of sipp scripts.

"""

import os
import os.path
import re

fail_count_re = re.compile(r"""^Failed.*\s(\d+)$""")
success_re = re.compile(r"""^Successful.*\s(\d+)$""")

myPath = '/Users/Meredith/PycharmProjects/MyCashman/data/'



def parse_screen_log(script, pid, regexper):
    """Examine a sipp screen log file located in the data directory and return the value captured by the passed-in regex.
       The script name plus process id identify a sipp script execution ('script run')
    """
    file_path = myPath + script[:-4] + "_" + str(pid) + "_screen.log"
    fh = None
    ret_value = None
    if os.path.isfile(file_path):
        try:
            fh = open(file_path)
            for lino, line in enumerate(fh, start=1):
                line = line.strip()
                match = regexper.search(line)
                if match:
                    ret_value = int(match.group(1))
        except {IOError, ValueError} as err:
            print("{0}: error {1} trying to read screen.log file".format(os.path.basename(sys.argv[0]), err))

        finally:
            if fh is not None:
                fh.close()

    return ret_value


def empty_screen_log(script, pid):
    """ Return True if screen log file exists and is empty.
    """
    file_path = myPath + script[:-4] + "_" + str(pid) + "_screen.log"
    if os.path.isfile(file_path):
        if os.path.getsize(file_path) == 0:
            return True
        else:
            return False
    else:
        return False


def no_failed_calls(script, pid):
    """Determine is the specified script run reported any failed calls."""
    if parse_screen_log(script, pid, fail_count_re) == 0:
        return True
    else:
        return False


def how_many_success(script, pid):
    """Determine how many successful calls were reported for the specified script run."""
    ret_value = parse_screen_log(script, pid, success_re)
    if ret_value is None:
        return 0
    else:
        return ret_value


def cleanup_screen_log(script, pid):
    """Delete the screen log for a sipp script run, it is NOT an error if the file does not exist."""
    file_path = myPath + script[:-4] + "_" + str(pid) + "_screen.log"
    try:
        os.remove(file_path)
    except OSError:
        pass