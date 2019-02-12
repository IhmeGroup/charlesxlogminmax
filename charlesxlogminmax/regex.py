#todo : docstring
import re


def filter_non_data(line):
    #todo : docstring
    if '*' in line or '-' in line or '>' in line:
        res = True
    else:
        res = False
    if 'calcSgsStuff' in line:
        res = False
    return res


def get_scalarRange(line):
    #todo : docstring
    name = ''
    data_min = 0
    data_max = 0
    matchObj = re.match(r'.*dumpScalarRange:(.*).*,\s(.*):(.*).*', line)
    if matchObj:
        name = str(matchObj.group(1))
        while ' ' in name:
            name = name.replace(' ', '')

        data_min = float(matchObj.group(2))
        data_max = float(matchObj.group(3))
    return matchObj, name, data_min, data_max


def get_vector_range(line):
    #todo : docstring
    name = ''
    data = []
    matchObj = re.match(r'.*dumpVectorRange:\s(.*),\s0:\s(.*):(.*),\s1:\s(.*):(.*),\s2:\s(.*):(.*)', line)
    data.append(matchObj)
    if matchObj:
        name = str(matchObj.group(1)).replace(' ', '')
        while ' ' in name:
            name = name.replace(' ', '')

        for idx in range(6):
            data.append(float(matchObj.group(2 + idx)))

    if 'RHOU' in name:
        name_1, name_2, name_3 = 'RHOU', 'RHOV', 'RHOW'
        data_1 = tuple((matchObj, name_1, data[1], data[2]))
        data_2 = tuple((matchObj, name_2, data[3], data[4]))
        data_3 = tuple((matchObj, name_3, data[5], data[6]))
    elif name == 'U':
        name_1, name_2, name_3 = 'U', 'V', 'W'
        data_1 = tuple((matchObj, name_1, data[1], data[2]))
        data_2 = tuple((matchObj, name_2, data[3], data[4]))
        data_3 = tuple((matchObj, name_3, data[5], data[6]))

    if matchObj:
        out = data_1, data_2, data_3
    else:
        dummy = [False, 'dummy', np.nan, np.nan]
        out = dummy, dummy, dummy

    return out


def get_temporal_info(line):
    #todo : docstring
    iter = 0
    time = 0
    dt = 0

    matchObj = re.match(r'.*step:(.*).*time:\s(.*)\sdt:\s(.*).*\*\s2', line)
    if matchObj:
        iter = int(matchObj.group(1))
        time = float(matchObj.group(2))
        dt = float(matchObj.group(3)) * 2

    return matchObj, iter, time, dt


def get_efficiency(line):
    #todo : docstring
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
