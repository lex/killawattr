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
        # sometimes there's "error" instead of a value
        if value == 'error':
            return None
        else:
            return value
    except KeyError as e:
        print(f'[!] Missing key "{key}"')
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
