import charlesxlogminmax.extract_data as ext_dat
import charlesxlogminmax.plot_min_max as plt_minmax

if __name__ == "__main__":
    # Test with csv input
    #log_file = 'data/charlesx_log_test.out'
    log_file = 'data/real_log.out'
    out_file = 'test_extract_out.csv'

    print('extract data')
    ext_dat.extract_log_data(log_file, out_file)
    print('plotting')
    plt_minmax.plot_log_data(out_file)
    print('plots done')

    # Test with log input
    plt_minmax.plot_log_data(log_file, show=True)
