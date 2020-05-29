#!/usr/bin/env python3

import csv
import json
import requests
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta
from pathlib import Path

RESOURCE_DIR = Path('lib')
# Contains list of districts
DISTRICT_LIST = RESOURCE_DIR / 'district_list.csv'
# Contains district data on 26th April
OLD_DISTRICT_DATA = RESOURCE_DIR / 'districts_26apr_gospel.csv'
DATE_END_OLD = '2020-04-26'

INPUT_DIR = Path('tmp')
# All raw_data's
RAW_DATA = 'raw_data{n}.json'
# Contains deaths and recoveries for entries in raw_data1 and raw_data2
OUTCOME_DATA = 'deaths_recoveries{n}.json'
# India testing data
ICMR_TEST_DATA = INPUT_DIR / 'data.json'
# States testing data
STATE_TEST_DATA = INPUT_DIR / 'state_test_data.json'
## For adding metadata
# For state notes and last updated
STATE_WISE = INPUT_DIR / 'data.json'
# For district notes
DISTRICT_WISE = INPUT_DIR / 'state_district_wise.json'

OUTPUT_DIR = Path('tmp', 'v3')
OUTPUT_MIN_DIR = OUTPUT_DIR / 'min'
OUTPUT_DATA_FILENAME = 'data'
OUTPUT_TIMESERIES_FILENAME = 'timeseries'

STATE_CODES = {
    'Andhra Pradesh': 'AP',
    'Arunachal Pradesh': 'AR',
    'Assam': 'AS',
    'Bihar': 'BR',
    'Chhattisgarh': 'CT',
    'Goa': 'GA',
    'Gujarat': 'GJ',
    'Haryana': 'HR',
    'Himachal Pradesh': 'HP',
    'Jharkhand': 'JH',
    'Karnataka': 'KA',
    'Kerala': 'KL',
    'Madhya Pradesh': 'MP',
    'Maharashtra': 'MH',
    'Manipur': 'MN',
    'Meghalaya': 'ML',
    'Mizoram': 'MZ',
    'Nagaland': 'NL',
    'Odisha': 'OR',
    'Punjab': 'PB',
    'Rajasthan': 'RJ',
    'Sikkim': 'SK',
    'State Unassigned': 'UN',
    'Tamil Nadu': 'TN',
    'Telangana': 'TG',
    'Tripura': 'TR',
    'Uttarakhand': 'UT',
    'Uttar Pradesh': 'UP',
    'West Bengal': 'WB',
    'Andaman and Nicobar Islands': 'AN',
    'Chandigarh': 'CH',
    'Dadra and Nagar Haveli and Daman and Diu': 'DN',
    'Delhi': 'DL',
    'Jammu and Kashmir': 'JK',
    'Ladakh': 'LA',
    'Lakshadweep': 'LD',
    'Puducherry': 'PY',
    'Total': 'TT',
    # To accomodate for improper entries in old data
    'Dadra and Nagar Haveli': 'DN',
    'Daman And Diu': 'DN',
}

DISTRICTS_DICT = defaultdict(dict)
DISTRICTS_ADDITIONAL = {
    'bsf camp': 'BSF Camp',
    'italians': 'Italians',
    'other state': 'Other State',
    'railway quarantine': 'Railway Quarantine',
    'airport quarantine': 'Airport Quarantine',
    'evacuees': 'Evacuees',
    'foreign evacuees': 'Foreign Evacuees',
    'unassigned': 'Unassigned',
}

PRINT_WIDTH = 60

ddict = lambda: defaultdict(ddict)
data = ddict()
timeseries = ddict()


def inc(ref, key, count):
    if not isinstance(ref[key], int):
        ref[key] = 0
    ref[key] += count


def parse(raw_data, i):
    for j, entry in enumerate(raw_data['raw_data']):
        state_name = entry['detectedstate']
        if not state_name:
            # Entries having no state name are discarded
            continue

        try:
            fdate = datetime.strptime(entry['dateannounced'], '%d/%m/%Y')
            date = datetime.strftime(fdate, '%Y-%m-%d')
        except ValueError:
            # Bad date
            print('[{}: {}] [Bad date: {}] {}: {} {}'.format(
                i, j + 2, entry['dateannounced'], entry['detectedstate'],
                entry['detecteddistrict'], entry['numcases']))
            continue

        state = STATE_CODES[state_name]
        district = entry['detecteddistrict']
        if not district:
            district = 'Unassigned'
        elif district.lower() in DISTRICTS_DICT[state]:
            district = DISTRICTS_DICT[state][district.lower()]
        elif district.lower() in DISTRICTS_ADDITIONAL:
            district = DISTRICTS_ADDITIONAL[district.lower()]
        else:
            # Print unexpected district names
            print('[{}: {}] [{}] [Unexpected district: {}] {}'.format(
                i, j + 2, date, district, state))

        try:
            count = int(entry['numcases'])
        except ValueError:
            print('[{}: {}] [{}] [Bad numcases: {}] {}: {}'.format(
                i, j + 2, date, entry['numcases'], state, district))
            continue

        if entry['currentstatus'] == 'Hospitalized' or i < 3:
            inc(data[date]['TT']['delta'], 'confirmed', count)
            inc(data[date][state]['delta'], 'confirmed', count)
            # Don't parse old district data since it's unreliable
            if i > 2:
                inc(data[date][state]['districts'][district]['delta'],
                    'confirmed', count)
        elif entry['currentstatus'] == 'Recovered':
            inc(data[date]['TT']['delta'], 'recovered', count)
            inc(data[date][state]['delta'], 'recovered', count)
            # Don't parse old district data unreliable since it's unreliable
            if i > 2:
                inc(data[date][state]['districts'][district]['delta'],
                    'recovered', count)
        elif entry['currentstatus'] == 'Deceased':
            inc(data[date]['TT']['delta'], 'deceased', count)
            inc(data[date][state]['delta'], 'deceased', count)
            # Don't parse old district data unreliable since it's unreliable
            if i > 2:
                inc(data[date][state]['districts'][district]['delta'],
                    'deceased', count)


def parse_outcome(outcome_data, i):
    for j, entry in enumerate(outcome_data['deaths_recoveries']):
        state_name = entry['state']
        if not state_name:
            # Entries having no state name are discarded
            continue
        state = STATE_CODES[state_name]

        try:
            fdate = datetime.strptime(entry['date'], '%d/%m/%Y')
            date = datetime.strftime(fdate, '%Y-%m-%d')
        except ValueError:
            # Bad date
            print('[{}: {}] [Bad date: {}] {}'.format(i, j + 2, entry['date'],
                                                      state))
            continue

        district = entry['district']
        if not district:
            district = 'Unassigned'
        elif district.lower() in DISTRICTS_DICT[state]:
            district = DISTRICTS_DICT[state][district.lower()]
        elif district.lower() in DISTRICTS_ADDITIONAL:
            district = DISTRICTS_ADDITIONAL[district.lower()]
        else:
            # Print unexpected district names
            print('[{}: {}] [{}] [Unexpected district: {}] {}'.format(
                i, j + 2, date, district, state))

        if entry['patientstatus'] == 'Recovered':
            inc(data[date]['TT']['delta'], 'recovered', 1)
            inc(data[date][state]['delta'], 'recovered', 1)
            ## Don't parse old district data since it's unreliable
            #  inc(data[date][state]['districts'][district]['delta'], 'recovered',
            #      1)
        elif entry['patientstatus'] == 'Deceased':
            inc(data[date]['TT']['delta'], 'deceased', 1)
            inc(data[date][state]['delta'], 'deceased', 1)
            ## Don't parse old district data since it's unreliable
            #  inc(data[date][state]['districts'][district]['delta'], 'deceased',
            #      1)


def accumulate():
    for date in sorted(data):
        curr_data = data[date]

        fdate = datetime.strptime(date, '%Y-%m-%d')
        prev_date = datetime.strftime(fdate - timedelta(days=1), '%Y-%m-%d')

        if prev_date in data:
            prev_data = data[prev_date]
            for state, state_data in prev_data.items():
                for statistic in ['confirmed', 'deceased', 'recovered']:
                    if statistic in state_data['total']:
                        inc(curr_data[state]['total'], statistic,
                            state_data['total'][statistic])

                if state == 'TT' or date <= DATE_END_OLD:
                    # Total state has no district data
                    # Old district data is already accumulated
                    continue

                for district, district_data in state_data['districts'].items():
                    for statistic in ['confirmed', 'deceased', 'recovered']:
                        if statistic in district_data['total']:
                            inc(
                                curr_data[state]['districts'][district]
                                ['total'], statistic,
                                district_data['total'][statistic])

        for state, state_data in curr_data.items():
            if 'delta' in state_data:
                for statistic in ['confirmed', 'deceased', 'recovered']:
                    if statistic in state_data['delta']:
                        inc(state_data['total'], statistic,
                            state_data['delta'][statistic])

                if state == 'TT' or date <= DATE_END_OLD:
                    # Total state has no district data
                    # Old district data is already accumulated
                    continue

                for district, district_data in state_data['districts'].items():
                    if 'delta' in district_data:
                        for statistic in [
                                'confirmed', 'deceased', 'recovered'
                        ]:
                            if statistic in district_data['delta']:
                                inc(district_data['total'], statistic,
                                    district_data['delta'][statistic])


def parse_icmr(icmr_data):
    for j, entry in enumerate(icmr_data['tested']):
        try:
            fdate = datetime.strptime(entry['updatetimestamp'],
                                      '%d/%m/%Y %H:%M:%S')
            date = datetime.strftime(fdate, '%Y-%m-%d')
        except ValueError:
            # Bad timestamp
            print('[{}] [Bad timestamp: {}]'.format(j + 2,
                                                    entry['updatetimestamp']))
            continue

        if entry['totalsamplestested']:
            try:
                count = int(entry['totalsamplestested'])
            except ValueError:
                print('[{}] [{}] [Bad totalsamplestested: {}]'.format(
                    j + 2, entry['updatetimestamp'],
                    entry['totalsamplestested']))
                continue

            data[date]['TT']['total']['tested'] = count
            data[date]['TT']['meta']['tested']['source'] = entry['source']
            data[date]['TT']['meta']['tested']['last_updated'] = date


def parse_state_test(state_test_data):
    for j, entry in enumerate(state_test_data['states_tested_data']):
        try:
            fdate = datetime.strptime(entry['updatedon'], '%d/%m/%Y')
            date = datetime.strftime(fdate, '%Y-%m-%d')
        except ValueError:
            # Bad date
            print('[{}] [Bad date: {}] {}'.format(j + 2, entry['updatedon'],
                                                  entry['state']))
            continue

        state = STATE_CODES[entry['state']]

        if entry['totaltested']:
            try:
                count = int(entry['totaltested'])
            except ValueError:
                print('[{}] [{}] [Bad totaltested: {}] {}'.format(
                    j + 2, entry['updatedon'], entry['totaltested'],
                    entry['state']))
                continue

            data[date][state]['total']['tested'] = count
            data[date][state]['meta']['tested']['source'] = entry['source1']
            data[date][state]['meta']['tested']['last_updated'] = date


def fill_deltas_tested():
    for date in sorted(data):
        curr_data = data[date]

        fdate = datetime.strptime(date, '%Y-%m-%d')
        prev_date = datetime.strftime(fdate - timedelta(days=1), '%Y-%m-%d')

        for state, state_data in curr_data.items():
            if 'total' in state_data:
                if 'tested' in state_data['total']:
                    state_data['delta']['tested'] = state_data['total'][
                        'tested']

        if prev_date in data:
            prev_data = data[prev_date]
            for state, state_data in prev_data.items():
                if 'tested' in state_data['total']:
                    if 'tested' in curr_data[state]['total']:
                        # Subtract previous date's value to get diff
                        curr_data[state]['delta']['tested'] -= state_data[
                            'total']['tested']
                    else:
                        # Take today's value to be same as previous date's value
                        curr_data[state]['total']['tested'] = state_data[
                            'total']['tested']


def add_state_meta(raw_data):
    last_data = data[sorted(data)[-1]]
    for j, entry in enumerate(raw_data['statewise']):
        state = entry['statecode']
        try:
            fdate = datetime.strptime(entry['lastupdatedtime'],
                                      '%d/%m/%Y %H:%M:%S')
        except ValueError:
            # Bad timestamp
            print('[{}] [Bad timestamp: {}] {}'.format(
                j + 2, entry['lastupdatedtime'], state))
            continue

        last_data[state]['meta']['last_updated'] = fdate.isoformat() + '+05:30'
        if entry['statenotes']:
            last_data[state]['meta']['notes'] = entry['statenotes']

        for statistic in ['confirmed', 'deceased', 'recovered']:
            try:
                values = {
                    'total':
                    int(entry[
                        statistic if statistic != 'deceased' else 'deaths']),
                    'delta':
                    int(entry['delta' + (
                        statistic if statistic != 'deceased' else 'deaths')])
                }
            except ValueError:
                print('[{}] [{}] [Bad value for {}] {}'.format(
                    j + 2, entry['lastupdatedtime'], statistic, state))
                continue

            for stype in ['total', 'delta']:
                if values[stype] and values[stype] != last_data[state][stype][
                        statistic]:
                    # Print mismatch between statewise and v3
                    print(state, statistic, stype, values[stype],
                          last_data[state][stype][statistic])


def add_district_meta(raw_data):
    last_data = data[sorted(data)[-1]]
    for j, entry in enumerate(raw_data.values()):
        state = entry['statecode']
        for district, district_data in entry['districtData'].items():
            if district == 'Unknown':
                district = 'Unassigned'
            if district_data['notes']:
                last_data[state]['districts'][district]['meta'][
                    'notes'] = district_data['notes']
            for statistic in ['confirmed', 'deceased', 'recovered']:
                try:
                    values = {
                        'total': int(district_data[statistic]),
                        'delta': int(district_data['delta'][statistic])
                    }
                except ValueError:
                    print('[{}] [Bad value for {}] {} {}'.format(
                        j + 2, statistic, state, district))
                    continue

                for stype in ['total', 'delta']:
                    if values[stype] and values[stype] != last_data[state][
                            'districts'][district][stype][statistic]:
                        # Print mismatch between districtwise and v3
                        print(
                            state, district, statistic, stype, values[stype],
                            last_data[state]['districts'][district][stype]
                            [statistic])


def parse_old_districts(reader):
    for row in reader:
        state = row['State_Code']
        district = row['District']
        if district.lower() in DISTRICTS_DICT[state]:
            district = DISTRICTS_DICT[state][district.lower()]

        for statistic in ['confirmed', 'deceased', 'recovered']:
            if row[statistic.capitalize()]:
                data[DATE_END_OLD][state]['districts'][district]['total'][
                    statistic] = int(row[statistic.capitalize()])


def parse_district_list(reader):
    for row in reader:
        DISTRICTS_DICT[STATE_CODES[row['State']]][
            row['District'].lower()] = row['District']


def generate_timeseries(districts=False):
    for date in sorted(data):
        curr_data = data[date]

        for state, state_data in curr_data.items():
            for stype in ['total', 'delta']:
                if stype in state_data:
                    for statistic, value in state_data[stype].items():
                        timeseries[state]['timeseries'][date][stype][
                            statistic] = value

            if not districts or state == 'TT' or date <= DATE_END_OLD:
                # Total state has no district data
                # District timeseries starts only from 26th April
                continue

            for district, district_data in state_data['districts'].items():
                for stype in ['total', 'delta']:
                    if stype in district_data:
                        for statistic, value in district_data[stype].items():
                            timeseries[state]['districts'][district][
                                'timeseries'][date][stype][statistic] = value


if __name__ == '__main__':
    print('-' * PRINT_WIDTH)
    print('{:{align}{width}}'.format('PARSER V3 START',
                                     align='^',
                                     width=PRINT_WIDTH))
    # Get all expected district names
    with open(DISTRICT_LIST, 'r') as f:
        reader = csv.DictReader(f)
        parse_district_list(reader)

    # Parse raw_data's
    print('-' * PRINT_WIDTH)
    print('Parsing raw_data...')
    i = 1
    while True:
        f = INPUT_DIR / RAW_DATA.format(n=i)
        if not f.is_file():
            break
        with open(f, 'r') as f:
            raw_data = json.load(f)
            parse(raw_data, i)
        i += 1
    print('Done!')

    # Parse additional deceased/recovered info not in raw_data 1 and 2
    print('-' * PRINT_WIDTH)
    print('Parsing deaths_recoveries...')
    for i in [1, 2]:
        f = INPUT_DIR / OUTCOME_DATA.format(n=i)
        with open(f, 'r') as f:
            raw_data = json.load(f)
            parse_outcome(raw_data, i)
    print('Done!')

    print('-' * PRINT_WIDTH)
    print('Adding district data for 26th April...')
    # Parse gospel district data for 26th April
    with open(OLD_DISTRICT_DATA, 'r') as f:
        reader = csv.DictReader(f)
        parse_old_districts(reader)
    print('Done!')

    print('-' * PRINT_WIDTH)
    print('Generating cumulative statistics...')
    # Generate total (cumulative) data points
    accumulate()
    print('Done!')

    print('-' * PRINT_WIDTH)
    print('Parsing ICMR test data for India...')
    f = ICMR_TEST_DATA
    with open(f, 'r') as f:
        raw_data = json.load(f, object_pairs_hook=OrderedDict)
        parse_icmr(raw_data)
    print('Done!')

    print('-' * PRINT_WIDTH)
    print('Parsing test data for all states...')
    f = STATE_TEST_DATA
    with open(f, 'r') as f:
        raw_data = json.load(f, object_pairs_hook=OrderedDict)
        parse_state_test(raw_data)
    print('Done!')

    print('-' * PRINT_WIDTH)
    print('Generating daily tested values...')
    fill_deltas_tested()
    print('Done!')

    print('-' * PRINT_WIDTH)
    print('Adding state/district meta data and tallying...')
    f = STATE_WISE
    with open(f, 'r') as f:
        raw_data = json.load(f, object_pairs_hook=OrderedDict)
        add_state_meta(raw_data)

    f = DISTRICT_WISE
    with open(f, 'r') as f:
        raw_data = json.load(f, object_pairs_hook=OrderedDict)
        add_district_meta(raw_data)
    print('Done!')

    print('-' * PRINT_WIDTH)
    print('Dumping APIs...')
    OUTPUT_MIN_DIR.mkdir(parents=True, exist_ok=True)

    # Dump prettified full data json
    with open((OUTPUT_DIR / OUTPUT_DATA_FILENAME).with_suffix('.json'),
              'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
    # Dump minified full data
    with open((OUTPUT_MIN_DIR / OUTPUT_DATA_FILENAME).with_suffix('.min.json'),
              'w') as f:
        json.dump(data, f, separators=(',', ':'), sort_keys=True)

    # Split data and dump separate json for each date
    for date in sorted(data):
        curr_data = data[date]
        with open((OUTPUT_DIR / date).with_suffix('.json'), 'w') as f:
            json.dump(curr_data, f, indent=2, sort_keys=True)
        # Minified
        with open((OUTPUT_MIN_DIR / date).with_suffix('.min.json'), 'w') as f:
            json.dump(curr_data, f, separators=(',', ':'), sort_keys=True)

    # Generate timeseries
    generate_timeseries(districts=False)

    # Dump timeseries json
    with open((OUTPUT_DIR / OUTPUT_TIMESERIES_FILENAME).with_suffix('.json'),
              'w') as f:
        json.dump(timeseries, f, indent=2, sort_keys=True)
    with open(
        (OUTPUT_MIN_DIR / OUTPUT_TIMESERIES_FILENAME).with_suffix('.min.json'),
            'w') as f:
        json.dump(timeseries, f, separators=(',', ':'), sort_keys=True)

    print('Done!')
    print('-' * PRINT_WIDTH)
    print('{:{align}{width}}'.format('PARSER V3 END',
                                     align='^',
                                     width=PRINT_WIDTH))
    print('-' * PRINT_WIDTH)
