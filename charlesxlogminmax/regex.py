"""
This file contains all the functions needed to filter the data.
 - filter_non_data gets rid of non-data-containing lines
 - the get_* functions use regular expressions to extract the data
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

import numpy as np


def filter_non_data(line):
    """
    Returns true if the line contains data
    :param line: line of a file (str)
    :return: Bool
    """
    if '*' in line or '-' in line or '>' in line:
        res = True
    else:
        res = False
    if 'calcSgsStuff' in line:
        res = False
    return res


def get_scalarRange(line):
    """
    Scraps data for a scalarRange kind of data output
    :param line: line of a file (str)
    :return: tuple --> regex obj (can be treated as bool), name, min, max
    """
    name = ''
    data_min = 0
    data_max = 0
    match_obj = re.match(r'.*dumpScalarRange:(.*).*,\s(.*):(.*).*', line)
    if match_obj:
        name = str(match_obj.group(1))
        while ' ' in name:
            name = name.replace(' ', '')

        data_min = float(match_obj.group(2))
        data_max = float(match_obj.group(3))
    return match_obj, name, data_min, data_max


def get_vector_range(line):
    """
    Scraps data for a vectorRange kind of data output
    :param line: line of a file (str)
    :return: tuple of scalar tuples --> regex obj (can be treated as bool), name, min, max
    """
    name = ''
    data = []
    match_obj = re.match(r'.*dumpVectorRange:\s(.*),\s0:\s(.*):(.*),\s1:\s(.*):(.*),\s2:\s(.*):(.*)', line)
    data.append(match_obj)
    if match_obj:
        name = str(match_obj.group(1)).replace(' ', '')
        while ' ' in name:
            name = name.replace(' ', '')

        for idx in range(6):
            data.append(float(match_obj.group(2 + idx)))

    if 'RHOU' in name:
        name_1, name_2, name_3 = 'RHOU', 'RHOV', 'RHOW'
        data_1 = tuple((match_obj, name_1, data[1], data[2]))
        data_2 = tuple((match_obj, name_2, data[3], data[4]))
        data_3 = tuple((match_obj, name_3, data[5], data[6]))
    elif name == 'U':
        name_1, name_2, name_3 = 'U', 'V', 'W'
        data_1 = tuple((match_obj, name_1, data[1], data[2]))
        data_2 = tuple((match_obj, name_2, data[3], data[4]))
        data_3 = tuple((match_obj, name_3, data[5], data[6]))
    # for LSP
    elif 'XP' in name:
        name_1, name_2, name_3 = 'LSP:XP', 'LSP:YP', 'LSP:ZP'
        data_1 = tuple((match_obj, name_1, data[1], data[2]))
        data_2 = tuple((match_obj, name_2, data[3], data[4]))
        data_3 = tuple((match_obj, name_3, data[5], data[6]))
    elif 'UP' in name:
        name_1, name_2, name_3 = 'LSP:UP', 'LSP:VP', 'LSP:WP'
        data_1 = tuple((match_obj, name_1, data[1], data[2]))
        data_2 = tuple((match_obj, name_2, data[3], data[4]))
        data_3 = tuple((match_obj, name_3, data[5], data[6]))
        
    if match_obj:
        out = data_1, data_2, data_3
    else:
        dummy = [False, 'dummy', np.nan, np.nan]
        out = dummy, dummy, dummy

    return out


def get_reconstruction_info(line):
    """
    Scraps data for a shock-capturing recomnstruction kind of data output
    :param line: line of a file (str)
    :return: tuple of scalar tuples --> regex obj (can be treated as bool), name, recon 
    """
    name = ''
    recon = [0, 0, 0]
    match_obj = re.match(r'.*WENO\s:\s(.*)\%\sENO\s:\s(.*)\%\sFIRST_ORDER\s:\s(.*)\%.*', line)
    if match_obj:
        if 'shock-capturing' in line:
            # name = [str(match_obj.group(3)),str(match_obj.group(5)),str(match_obj.group(7))]
            name = ["WENO", "ENO", "FIRST_ORDER"]
            # recon =  [float(match_obj.group(4)),float(match_obj.group(6)),float(match_obj.group(8))]
            recon = [float(match_obj.group(1)), float(match_obj.group(2)), float(match_obj.group(3))]
        else:
            match_obj = False

    return match_obj, name, recon


def get_doubleflux_info(line):
    """
    Scraps data for the doubleflux percentage
    :param line: line of log file (str)
    :return: tuple --> regex obj (treated as bool), name, value
    """
    match_obj = re.match(r'.*double-flux.*:(.*).*\%', line)
    if match_obj:
        name = 'DoubleFlux'
        percent_df = float(match_obj.group(1))
    else:
        name = ''
        percent_df = -1
        match_obj = False
    return match_obj, name, percent_df

def get_subphysics_info(line):
    """
    Scraps data for the total sub-physics percentage
    :param line: line of a file (str)
    :return: tuple of scalar tuples --> regex obj (can be treated as bool), name, recon 
    """
    name = ''
    subphysics = [0, 0]
    match_obj = re.match(r'.*FPVA\s:\s(.*)\%\sMULTI_SPECIES\s:\s(.*)\%.*', line)
    #match_obj = re.match(r'.*total\ssub-physics*FPVA\s:\s(.*)\%\sMULTI_SPECIES\s:\s(.*)\%.*', line)
    #match_obj = re.match(r'.*total\ssub-physics\spercentage\sover\s(.*)\svolumes:\s(FPVA\s:\s(.*)\%\sMULTI_SPECIES\s:\s(.*)\%.*', line)
    if match_obj:
        if 'total sub-physics' in line:
            #name = [str(match_obj.group(3)),str(match_obj.group(5)),str(match_obj.group(7))]
            name = ["FPVA","MULTI_SPECIES"]
            subphysics =  [float(match_obj.group(1)),float(match_obj.group(2))]
        else:
            match_obj = False

    return match_obj, name, subphysics


def get_temporal_info(line):
    """
    Scraps data for a temporal kind of data output
    :param line: line of a file (str)
    :return: tuple --> regex obj (can be treated as bool), iter, time, dt
    """
    iter = 0
    time = 0
    dt = 0

    match_obj = re.match(r'.*step:(.*).*time:\s(.*)\sdt:\s(.*).*\*\s2', line)
    if match_obj:
        iter = int(match_obj.group(1))
        time = float(match_obj.group(2))
        dt = float(match_obj.group(3)) * 2
    else:
        match_obj = re.match(r'.*step:(.*).*time:\s(.*)\sdt:\s(.*)', line)
        if match_obj:
            iter = int(match_obj.group(1))
            time = float(match_obj.group(2))
            dt = float(match_obj.group(3))

    return match_obj, iter, time, dt


def get_efficiency(line):
    """
    Scraps data for efficiency output
    :param line: line of a file (str)
    :return: tuple --> regex obj (can be treated as bool), name, efficiency
    """
    name = ''
    eff = 0.
    match_obj = re.match(r'\s>\s(.*):\s(.*)', line)
    if match_obj:
        if 'time-per-iter' in line:
            name = str(match_obj.group(1))
            eff = float(match_obj.group(2))
        else:
            match_obj = False
    return match_obj, name, eff
