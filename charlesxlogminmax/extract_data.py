"""
This file contains the main extraction function.

It reads the log file line by line:

    - filter non data containing lines
    - match and extract temporal data
    - match and extract scalar range data
    - match and vector scalar range data
    - match and efficiency data
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pandas as pd

from . import regex


def extract_log_data(input_log, output_csv, verbose=True):
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
        # First get the iteration, time, time_elapsed (since start of run) and time step
        match_temp, iter, time, time_elapsed, dt = regex.get_temporal_info(my_line)
        if match_temp:
            i += 1
            try:
                temp_data['idx'].append(i)
                temp_data['iteration'].append(iter)
                temp_data['time'].append(time)
                temp_data['time_elapsed'].append(time_elapsed)
                temp_data['dt'].append(dt)
            except KeyError:
                temp_data['idx'] = []
                temp_data['iteration'] = []
                temp_data['time'] = []
                temp_data['time_elapsed'] = []
                temp_data['dt'] = []
                temp_data['idx'].append(i)
                temp_data['iteration'].append(iter)
                temp_data['time'].append(time)
                temp_data['time_elapsed'].append(time_elapsed)
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

                match_rewind, name, rewind = regex.get_rewind(my_line)
                if match_rewind:
                    try:
                        temp_data['%s' % name].append(rewind)
                    except KeyError:
                        temp_data['%s' % name] = []
                        temp_data['%s' % name].append(rewind)

                match_eff, name, eff = regex.get_efficiency(my_line)
                if match_eff:
                    try:
                        temp_data['%s' % name].append(eff)
                    except KeyError:
                        temp_data['%s' % name] = []
                        temp_data['%s' % name].append(eff)

                match_df, name, percent_df = regex.get_doubleflux_info(my_line)
                if match_df:
                    try:
                        temp_data['%s' % name].append(percent_df)
                    except KeyError:
                        temp_data['%s' % name] = []
                        temp_data['%s' % name].append(percent_df)

                match_recon, name, recon = regex.get_reconstruction_info(my_line)
                if match_recon:
                    try:
                        for iN in range(len(recon)):
                            temp_data['%s' % name[iN]].append(recon[iN])
                    except KeyError:
                        for iN in range(len(recon)):
                            temp_data['%s' % name[iN]] = []
                            temp_data['%s' % name[iN]].append(recon[iN])

                match_subphysics, name, subphysics = regex.get_subphysics_info(my_line)
                if match_subphysics:
                    try:
                        for iN in range(len(subphysics)):
                            temp_data['%s' % name[iN]].append(subphysics[iN])
                    except KeyError:
                        for iN in range(len(subphysics)):
                            temp_data['%s' % name[iN]] = []
                            temp_data['%s' % name[iN]].append(subphysics[iN])

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
    # Python 2
    try:
        df = pd.DataFrame(dict([(key, pd.Series(val)) for key, val in temp_data.iteritems()]))
    # Python 3
    except AttributeError:
        df = pd.DataFrame(dict([(key, pd.Series(val)) for key, val in temp_data.items()]))

    for name in df.columns:
        if 'idx' in name:
            df = df.drop(columns=[name])
        if 'Unnamed' in name:
            df = df.drop(columns=[name])

    if verbose:
        print('\nThe variables found in the log "%s" are:' % input_log)
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
