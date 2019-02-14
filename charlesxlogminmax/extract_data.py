"""
This file contains the main extraction function.

It reads the log file line by line:

    - filter non data containing lines
    - match and extract temporal data
    - match and extract scalar range data
    - match and vector scalar range data
    - match and efficiency data
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import pandas as pd

from . import regex


def extract_log_data(input_log, output_csv):
    """
    Extracts scalar data from charlesx log
    :param input_log:
    :param output_csv:
    :return:
    """
    lst = [line for line in open(input_log)]

    temp_data = {}
    i = 0
    # Iterate over the line to scrap the data
    for my_line in lst:
        # First get the iteration, time and time step
        match_temp, iter, time, dt = regex.get_temporal_info(my_line)
        if match_temp:
            i += 1
            try:
                temp_data['idx'].append(i)
                temp_data['iteration'].append(iter)
                temp_data['time'].append(time)
                temp_data['dt'].append(dt)
            except KeyError:
                temp_data['idx'] = []
                temp_data['iteration'] = []
                temp_data['time'] = []
                temp_data['dt'] = []
                temp_data['idx'].append(i)
                temp_data['iteration'].append(iter)
                temp_data['time'].append(time)
                temp_data['dt'].append(dt)
        if i > 0:
            if regex.filter_non_data(my_line):
                # Get every printed scalar
                match_scalar, name, data_min, data_max = regex.get_scalarRange(my_line)
                if match_scalar:
                    try:
                        temp_data['%s_min' % name].append(data_min)
                        temp_data['%s_max' % name].append(data_max)
                    except KeyError:
                        temp_data['%s_min' % name] = []
                        temp_data['%s_max' % name] = []
                        temp_data['%s_min' % name].append(data_min)
                        temp_data['%s_max' % name].append(data_max)

                match_eff, name, eff = regex.get_efficiency(my_line)
                if match_eff:
                    try:
                        temp_data['%s' % name].append(eff)
                    except KeyError:
                        temp_data['%s' % name] = []
                        temp_data['%s' % name].append(eff)

                # Get every printed 3D vectors (RHOU and U)
                for data in regex.get_vector_range(my_line):
                    match_vector, name, data_min, data_max = data
                    if match_vector:
                        try:
                            temp_data['%s_min' % name].append(data_min)
                            temp_data['%s_max' % name].append(data_max)
                        except KeyError:
                            temp_data['%s_min' % name] = []
                            temp_data['%s_max' % name] = []
                            temp_data['%s_min' % name].append(data_min)
                            temp_data['%s_max' % name].append(data_max)

    # Get data as pandas data frame
    n_data = []
    for key in temp_data.keys():
        n_data.append(len(temp_data[key]))

    min_length = min(n_data)
    for key in match_temp.keys():
        temp_data[key] = temp_data[key][0:min_length]

    #df = pd.DataFrame(dict([(key, pd.Series(val)) for key, val in temp_data.iteritems()]))
    df = pd.DataFrame.from_dict(temp_data)

    for name in df.columns:
        if 'idx' in name:
            df = df.drop(columns=[name])
        if 'Unnamed' in name:
            df = df.drop(columns=[name])

    print("The variables found in the log are:")
    for name in df.columns:
        print("\t%s" % name)

    # Output data as csv file
    if not output_csv.endswith('.csv'):
        df.to_csv(output_csv + '.csv')
    else:
        df.to_csv(output_csv)


if __name__ == "__main__":
    infile = '../test/data/charlesx_log_test.out'
    outfile = '../test/test_out.csv'
    extract_log_data(infile, outfile)
