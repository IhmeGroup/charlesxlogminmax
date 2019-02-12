import charlesxlogminmax.extract_data as ext_dat

log_file = 'test/data/charlesx_log_test.out'
out_file = 'test_extract_out.csv'
ext_dat.extract_log_data(log_file, out_file)