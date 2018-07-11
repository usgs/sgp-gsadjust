import pytest
import GSadjust


def test_readfile_exceptions():
    bad_filename = './test_doesnotexist.txt'
    bad_indexdata_filename = './test_badindex_BurrisData.txt'
    bad_valuedata_filename = './test_badvalue_BurrisData.txt'
    meter_type = 'Burris'
    with pytest.raises(IOError) as excinfo:
        data = GSadjust.MainProg.read_raw_data_file(bad_filename, meter_type)
    with pytest.raises(IndexError) as excinfo:
        data = GSadjust.MainProg.read_raw_data_file(bad_indexdata_filename, meter_type)
    with pytest.raises(ValueError) as excinfo:
        data = GSadjust.MainProg.read_raw_data_file(bad_valuedata_filename, meter_type)

def test_read_Burris():
    filename = './test_BurrisData.txt'
    meter_type = 'Burris'
    data = GSadjust.MainProg.read_raw_data_file(filename, meter_type)
    assert len(data.dial) == 497
    assert len(data.raw_grav) == 497
    assert len(data.corr_g) == 0
    first_station = 'rg37'
    for idx, el in enumerate(data.station):
        if el != first_station:
            first_station_data = data.raw_grav[:idx]
            break
    mean = sum(first_station_data) / len(first_station_data)
    # This value calculated independently in Excel
    assert abs(mean - 2775777) < 0.1

def test_read_ScintrexCG6():
    filename = './test_ScintrexCG5Data.txt'
    meter_type = 'Scintrex'
    data = GSadjust.MainProg.read_raw_data_file(filename, meter_type)
    first_station = '1'
    assert len(data.dial) == 0
    assert len(data.keepdata) == 2096
    assert len(data.raw_grav) == 2096
    assert len(data.corr_g) == 0
    for idx, el in enumerate(data.station):
        if el != first_station:
            first_station_data = data.raw_grav[:idx]
            break
    mean = sum(first_station_data) / len(first_station_data)
    # This value calculated independently in Excel
    assert abs(mean - 2639322) < 0.1