#todo : docstring
import numpy as np
import pandas as pd

from . import regex


def extract_data(input_log, output_csv):
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

    df = pd.DataFrame.from_dict(temp_data)
    df.to_csv(output_csv)


if __name__ == "__main__":
    infile = 'data_test/charlesx_log_test.out'
    outfile = 'test_out.csv'
    extract_data(infile, outfile)
