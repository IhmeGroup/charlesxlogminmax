from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

from charlesxlogminmax.extract_data import extract_log_data
from charlesxlogminmax.plot_min_max import plot_log_data

if __name__ == "__main__":
    # Test with csv input
    log_file = 'data/real_log.out'
    out_file = 'test_extract_out.csv'

    extract_log_data(log_file, out_file)
    plot_log_data(out_file, savefig=True)

    # Test with log input
    plot_log_data(log_file, savefig=True)
