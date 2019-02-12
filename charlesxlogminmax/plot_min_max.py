"""
This file is made to plot log info from log or csv file
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import charlesxlogminmax
import charlesxlogminmax.extract_data as ext_dat


def get_colors(n_curves):
    """
    Get color of plots from colormap.
    the color of plots should be change by the flag "color=next(color)"
    :param n_curves: number of curves
    :return: color iterator
    """
    # Use offsets to avoid shitty crappy min/max colors (ugly yellow or white for example)
    first_step = 1. / (n_curves + 1.)
    last_step = 1.
    nb_steps = n_curves + 1
    color_range = np.linspace(first_step, last_step, nb_steps)
    color = iter(plt.cm.hot(color_range))
    return color


def clean_file_name(file_name):
    if 'time-per-iter' in file_name:
        file_name = file_name.replace('time-per-iter x n_procs/n_cvs (microseconds)',
                                      'time-per-iter nCPU per n_cvs in microseconds')
    else:
        for char in ['(', ')', ' ']:
            file_name = file_name.replace(char, '')

    return file_name


def plot_log_data(input_file, fill=False, ext='png', show=False):
    """
    Plot the lof data either from csv or CharlesX.log
    :param input_file: csv or charles x log file
    :param fill: True if you want a filled range version of the plot to be output
    :param ext: extension of the outfile (pdf, png, ...)
    :param show: True if you want to visualize the plots on the screen
    """
    # Use homemade matplotlib style
    plt.style.use(charlesxlogminmax.__path__[0] + '/style_quentin_douasbin.mplstyle')
    # plt.style.use('ggplot')
    plt.rcParams["savefig.format"] = ext

    directory = './LogFigures'
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        df_new = pd.read_csv(input_file)
    except pd.errors.ParserError:
        ext_dat.extract_log_data(input_file, 'dummy.csv')
        df_new = pd.read_csv('dummy.csv')
        os.remove('./dummy.csv')

    # create variable name list
    data_name = []
    for col in df_new.columns:
        if '_min' in col:
            if '_TF_' not in col:
                data_name.append(col.replace('_min', ''))

    for data in data_name:
        plt.figure()
        max_nm = data + '_max'
        min_nm = data + '_min'

        plt.plot(df_new.time, df_new[min_nm], '-', lw=1, markevery=0.05, label='Min')
        plt.plot(df_new.time, df_new[max_nm], '-', lw=1, markevery=0.05, label='Max')
        plt.xlabel("Time [s]")
        plt.ylabel("%s" % data)
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig(directory + '/range_%s' % data)
        if not show:
            plt.close()

        if fill:
            plt.figure()
            plt.plot(df_new.time, df_new[min_nm], 'k-', lw=0.5)
            plt.plot(df_new.time, df_new[max_nm], 'k-', lw=0.5)
            plt.fill_between(df_new.time, df_new[min_nm], y2=df_new[max_nm], alpha=0.15)
            plt.xlabel("Time [s]")
            plt.ylabel("%s" % data)
            plt.tight_layout()
            plt.savefig(directory + '/range_%s_fill' % data)
            if not show:
                plt.close()

    for name in df_new.columns:
        if '_min' in name or '_max' in name:
            df_new = df_new.drop(columns=[name])

    # create variable name list
    data_name = df_new.columns

    for name in data_name:
        plt.figure()

        plt.plot(df_new.time, df_new[name], '-', lw=1)
        plt.xlabel("Time [s]")
        plt.ylabel("%s" % name)
        plt.tight_layout()
        out_file = clean_file_name(directory + '/single_value_%s' % name)
        plt.savefig(out_file)
        if not show:
            plt.close()

    if show:
        plt.show()
