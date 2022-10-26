from killawattr.wrangling import extract_dict_value_or_none, wrangle_power_data, create_filtered_and_sorted_data_frame
from killawattr.wrangling import key_timestamp, key_power, key_supply, key_outdoor
from killawattr.wrangling import key_wrangled_timestamp, key_wrangled_power, key_wrangled_temperature_supply, key_wrangled_temperature_outdoor


class TestExtractingDictValues:
    def test_extracting_returns_value_if_key_exists(self):
        d = {'key': 'value'}
        assert extract_dict_value_or_none(d, 'key') == d['key']

    def test_extracting_returns_none_if_key_does_not_exist(self):
        d = {'key': 'value'}
        assert extract_dict_value_or_none(d, 'hole') == None

    def test_extracting_returns_none_if_value_is_error_string(self):
        d = {'key': 'error'}
        assert extract_dict_value_or_none(d, 'key') == None


class TestWrangling:
    def test_there_are_as_many_output_values_as_inputs(self):
        input = [
            {
                key_timestamp: 'error',
                key_power: 'error',
                key_supply: 'error',
                key_outdoor: 'error',
            },
            {
                key_timestamp: 'error',
                key_power: 'error',
                key_supply: 'error',
                key_outdoor: 'error',
            },
        ]

        output = wrangle_power_data(input)
        assert len(output[key_wrangled_timestamp]) == len(input)
        assert len(output[key_wrangled_power]) == len(input)
        assert len(output[key_wrangled_temperature_supply]) == len(input)
        assert len(output[key_wrangled_temperature_outdoor]) == len(input)

    def test_wrangled_data_has_the_same_values_as_the_input(self):
        input = [
            {
                key_timestamp: 0,
                key_power: 1,
                key_supply: 2,
                key_outdoor: 3,
            },
            {
                key_timestamp: 4,
                key_power: 5,
                key_supply: 6,
                key_outdoor: 7,
            }
        ]

        output = wrangle_power_data(input)

        for k1, k2 in zip(
            [key_wrangled_timestamp, key_wrangled_power,
                key_wrangled_temperature_supply, key_wrangled_temperature_outdoor],
                [key_timestamp, key_power, key_supply, key_outdoor]):
            assert output[k1][0] == input[0][k2]

    def test_wrangled_data_has_nones_instead_of_error_strings(self):
        input = [
            {
                key_timestamp: 'error',
                key_power: 'error',
                key_supply: 'error',
                key_outdoor: 'error',
            },
        ]

        output = wrangle_power_data(input)
        assert output[key_wrangled_timestamp][0] == None
        assert output[key_wrangled_power][0] == None
        assert output[key_wrangled_temperature_supply][0] == None
        assert output[key_wrangled_temperature_outdoor][0] == None


class TestDataFrameWrangling:
    input = [
        {
            key_timestamp: '2022-10-19T19:40:00+00:00',
            key_supply: 42,
            key_outdoor: 4,
            key_power: 17
        },
        {
            key_timestamp: '2022-10-19T18:10:00+00:00',
            key_supply: 34,
            key_outdoor: 3,
            key_power: 9
        },
    ]
    input_wrangled = wrangle_power_data(input)

    def test_data_frame_is_sorted_by_timestamp_ascending(self):
        df = create_filtered_and_sorted_data_frame(self.input_wrangled)
        assert df[key_wrangled_power].iloc[0] == self.input_wrangled[key_wrangled_power][1]

    def test_nans_are_dropped_from_generated_data_frame(self):
        input_wrangled = wrangle_power_data([
            {
                key_timestamp: None,
                key_supply: 34,
                key_outdoor: 3,
                key_power: 9
            },
            {
                key_timestamp: '2022-10-20T18:10:00+00:00',
                key_supply: None,
                key_outdoor: 3,
                key_power: 9
            },
            {
                key_timestamp: '2022-10-20T18:15:00+00:00',
                key_supply: 34,
                key_outdoor: None,
                key_power: 9
            },
            {
                key_timestamp: '2022-10-19T18:10:00+00:00',
                key_supply: 34,
                key_outdoor: 3,
                key_power: None
            },
        ])
        df = create_filtered_and_sorted_data_frame(input_wrangled)
        assert len(df) == 0

    def test_negative_powers_are_dropped_from_generated_data_frame(self):
        input_wrangled = wrangle_power_data([
            {
                key_timestamp: '2022-10-19T18:10:00+00:00',
                key_supply: 34,
                key_outdoor: 3,
                key_power: -9
            },
        ])
        df = create_filtered_and_sorted_data_frame(input_wrangled)
        assert len(df) == 0

    def test_over_100_kw_powers_are_dropped_from_generated_data_frame(self):
        input_wrangled = wrangle_power_data([
            {
                key_timestamp: '2022-10-19T18:10:00+00:00',
                key_supply: 34,
                key_outdoor: 3,
                key_power: 101
            },
        ])
        df = create_filtered_and_sorted_data_frame(input_wrangled)
        assert len(df) == 0

    def test_below_absolute_zero_temperatures_are_dropped_from_generated_data_frame(self):
        input_wrangled = wrangle_power_data([
            {
                key_timestamp: '2022-10-19T18:10:00+00:00',
                key_supply: -274,
                key_outdoor: 3,
                key_power: 5
            },
            {
                key_timestamp: '2022-10-19T18:15:00+00:00',
                key_supply: 5,
                key_outdoor: -999,
                key_power: 5
            },
        ])
        df = create_filtered_and_sorted_data_frame(input_wrangled)
        assert len(df) == 0

    def test_above_120_celsius_temperatures_are_dropped_from_generated_data_frame(self):
        input_wrangled = wrangle_power_data([
            {
                key_timestamp: '2022-10-19T18:10:00+00:00',
                key_supply: 121,
                key_outdoor: 3,
                key_power: 5
            },
            {
                key_timestamp: '2022-10-19T18:15:00+00:00',
                key_supply: 5,
                key_outdoor: 555,
                key_power: 5
            },
        ])
        df = create_filtered_and_sorted_data_frame(input_wrangled)
        assert len(df) == 0
