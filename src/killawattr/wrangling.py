import pandas as pd

key_timestamp = 'time_stamp'
key_power = 'Power-sum kW'
key_supply = 'Supply temp °C'
key_outdoor = 'Outdoor temperature °C'

key_wrangled_timestamp = 'timestamp'
key_wrangled_power = 'power'
key_wrangled_temperature_supply = 'temperature_supply'
key_wrangled_temperature_outdoor = 'temperature_outdoor'


def extract_dict_value_or_none(d, key):
    # for some reason, even timestamps are sometimes missing
    try:
        value = d[key]

        # a special feature in the json
        # sometimes there's 'error' instead of a value
        if value == 'error':
            return None
        else:
            return value
    except KeyError as e:
        print(f'[!] Missing key \'{key}\'')
        return None


# We need this so we can get the data wrangled into a more suitable format
def wrangle_power_data(data):
    timestamps = []
    powers = []
    temperature_supplys = []
    temperature_outdoors = []

    # Let's extract only what we need
    # We could also extract everything and then later just filter
    # out the stuff we don't need
    for d in data:
        timestamps.append(extract_dict_value_or_none(d, key_timestamp))
        powers.append(extract_dict_value_or_none(d, key_power))
        temperature_supplys.append(
            extract_dict_value_or_none(d, key_supply))
        temperature_outdoors.append(
            extract_dict_value_or_none(d, key_outdoor))

    d = {key_wrangled_timestamp: timestamps,
         key_wrangled_power: powers,
         key_wrangled_temperature_supply: temperature_supplys,
         key_wrangled_temperature_outdoor: temperature_outdoors,
         }
    return d


def create_filtered_and_sorted_data_frame(d):
    power_minimum = 0
    power_maximum = 100
    temperature_minimum = -273.15
    temperature_maximum = 120

    df = pd.DataFrame.from_dict(d)
    # for some reason the values aren't even sorted in the api
    df.sort_values(by=[key_wrangled_timestamp], inplace=True)

    # 'In case there are missing or fraudulent readings in the dataset, please somehow indicate the user of their existence'
    print('[!] Dropping the following rows with missing data:')
    print(df[df.isna().any(axis=1)])

    # remove nans
    # it would be possible to interpolate some values here instead of just dropping them
    # works for graphs maybe, but making up data is not very cool
    df.dropna(inplace=True)

    df.set_index(key_wrangled_timestamp, inplace=True)

    # there's probably not an easy to way to print what will be/was removed
    # so I guess you could just print the rows and then drop them

    # remove negative powers
    rows = df[df.power < power_minimum].index
    if rows.any():
        print(f'[!] Removing {len(rows)} negative powers')
    df.drop(rows, inplace=True)

    # remove > 100 kW (whatever is the maximum?)
    rows = df[df.power > power_maximum].index
    if rows.any():
        print(f'[!] Removing {len(rows)} too high powers')
    df.drop(rows, inplace=True)

    # remove unpossibly negative temperatures
    rows = df[df.temperature_supply < temperature_minimum].index
    if rows.any():
        print(f'[!] Removing {len(rows)} too low supply temperatures')
    df.drop(rows, inplace=True)

    rows = df[df.temperature_outdoor < temperature_minimum].index
    if rows.any():
        print(f'[!] Removing {len(rows)} too low outdoor temperatures')
    df.drop(rows, inplace=True)

    # remove possibly impossibly high temperatures
    rows = df[df.temperature_supply > temperature_maximum].index
    if rows.any():
        print(f'[!] Removing {len(rows)} too high supply temperatures')
    df.drop(rows, inplace=True)

    rows = df[df.temperature_outdoor > temperature_maximum].index
    if rows.any():
        print(f'[!] Removing {len(rows)} too high outdoor temperatures')
    df.drop(rows, inplace=True)

    return df
