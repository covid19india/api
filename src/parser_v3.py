#!/usr/bin/env python3

import csv
import logging
import json
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Set logging level
logging.basicConfig(stream=sys.stdout,
                    format='%(message)s',
                    level=logging.INFO)

# Current date in India
INDIA_DATE = datetime.strftime(
    datetime.utcnow() + timedelta(hours=5, minutes=30), '%Y-%m-%d')

INPUT_DIR = Path('tmp')
# Contains state codes to be used as API keys
STATE_META_DATA = INPUT_DIR / 'misc.json'
# Contains list of geographical districts
DISTRICT_LIST = INPUT_DIR / 'csv' / 'latest' / 'district_list.csv'
# All raw_data's
RAW_DATA = 'raw_data{n}.json'
# Contains deaths and recoveries for entries in raw_data1 and raw_data2
OUTCOME_DATA = 'deaths_recoveries{n}.json'
# Contains district data on 26th April
DISTRICT_DATA_GOSPEL = INPUT_DIR / 'csv' / 'latest' / 'districts_26apr_gospel.csv'
GOSPEL_DATE = '2020-04-26'
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
OUTPUT_DATA_PREFIX = 'data'
OUTPUT_TIMESERIES_FILENAME = 'timeseries'

# Two digit state codes
STATE_CODES = {}
DISTRICTS_DICT = defaultdict(dict)
# Some additional expected districts based on state bulletins
# These won't show up as Unexpected districts in the log
DISTRICTS_ADDITIONAL = {
    'bsf camp': 'BSF Camp',
    'italians': 'Italians',
    'other state': 'Other State',
    'other region': 'Other Region',
    'railway quarantine': 'Railway Quarantine',
    'airport quarantine': 'Airport Quarantine',
    'evacuees': 'Evacuees',
    'foreign evacuees': 'Foreign Evacuees',
    'unassigned': 'Unassigned',
}

PRIMARY_STATISTICS = ['confirmed', 'deceased', 'recovered']

RAW_DATA_MAP = {
    'hospitalized': 'confirmed',
    'deceased': 'deceased',
    'recovered': 'recovered',
    'migrated_other': 'migrated',
}

PRINT_WIDTH = 70

# Nested default dict of dict
ddict = lambda: defaultdict(ddict)
data = ddict()
timeseries = ddict()


def parse_state_codes(raw_data):
    for entry in raw_data['state_meta_data']:
        STATE_CODES[entry['stateut'].strip().lower(
        )] = entry['abbreviation'].strip().upper()


def parse_district_list(reader):
    for i, row in enumerate(reader):
        state_name = row['State'].strip().lower()
        if state_name not in STATE_CODES:
            logging.warning('[{}] [Bad state: {}]'.format(i, row['State']))
            continue
        district = row['District'].strip()
        DISTRICTS_DICT[STATE_CODES[state_name]][district.lower()] = district


def inc(ref, key, count):
    if not isinstance(ref[key], int):
        ref[key] = 0
    ref[key] += count


def parse(raw_data, i):
    for j, entry in enumerate(raw_data['raw_data']):
        state_name = entry['detectedstate'].strip().lower()
        try:
            state = STATE_CODES[state_name]
        except KeyError:
            # Entries with empty state names are discarded
            if state_name:
                # Unrecognized state entries are discarded and logged
                logging.warning('[V{}: L{}] [{}] [Bad state: {}] {}'.format(
                    i, j + 2, entry['dateannounced'], entry['detectedstate'],
                    entry['numcases']))
            continue

        try:
            fdate = datetime.strptime(entry['dateannounced'].strip(),
                                      '%d/%m/%Y')
            date = datetime.strftime(fdate, '%Y-%m-%d')
            if date > INDIA_DATE:
                # Entries from future dates will be ignored
                logging.warning(
                    '[V{}: L{}] [Future date: {}] {}: {} {}'.format(
                        i, j + 2, entry['dateannounced'],
                        entry['detectedstate'], entry['detecteddistrict'],
                        entry['numcases']))
                continue
        except ValueError:
            # Bad date
            logging.warning('[V{}: L{}] [Bad date: {}] {}: {} {}'.format(
                i, j + 2, entry['dateannounced'], entry['detectedstate'],
                entry['detecteddistrict'], entry['numcases']))
            continue

        district = entry['detecteddistrict'].strip()
        if not district:
            district = 'Unassigned'
        elif district.lower() in DISTRICTS_DICT[state]:
            district = DISTRICTS_DICT[state][district.lower()]
        elif district.lower() in DISTRICTS_ADDITIONAL:
            district = DISTRICTS_ADDITIONAL[district.lower()]
        else:
            # Print unexpected district names
            logging.warning(
                '[V{}: L{}] [{}] [Unexpected district: {}] {}'.format(
                    i, j + 2, date, district, state))

        try:
            count = int(entry['numcases'].strip())
        except ValueError:
            logging.warning('[V{}: L{}] [{}] [Bad numcases: {}] {}: {}'.format(
                i, j + 2, date, entry['numcases'], state, district))
            continue

        try:
            # All rows in v1 and v2 are confirmed cases
            statistic = 'confirmed' if i < 3 else RAW_DATA_MAP[
                entry['currentstatus'].strip().lower()]

            inc(data[date]['TT']['delta'], statistic, count)
            inc(data[date][state]['delta'], statistic, count)
            # Don't parse old district data since it's unreliable
            if i > 2:
                inc(data[date][state]['districts'][district]['delta'],
                    statistic, count)

        except KeyError:
            # Unrecognized status
            logging.warning(
                '[V{}: L{}] [{}] [Bad currentstatus: {}] {}: {} {}'.format(
                    i, j + 2, date, entry['currentstatus'], state, district,
                    entry['numcases']))


def parse_outcome(outcome_data, i):
    for j, entry in enumerate(outcome_data['deaths_recoveries']):
        state_name = entry['state'].strip().lower()
        try:
            state = STATE_CODES[state_name]
        except KeyError:
            # Entries with empty state names are discarded
            if state_name:
                # Unrecognized state entries are discarded and logged
                logging.warning('[V{}: L{}] [{}] [Bad state: {}]'.format(
                    i, j + 2, entry['date'], entry['state']))
            continue

        try:
            fdate = datetime.strptime(entry['date'].strip(), '%d/%m/%Y')
            date = datetime.strftime(fdate, '%Y-%m-%d')
            if date > INDIA_DATE:
                # Entries from future dates will be ignored
                logging.warning('[V{}: L{}] [Future date: {}] {}'.format(
                    i, j + 2, entry['date'], state))
                continue
        except ValueError:
            # Bad date
            logging.warning('[V{}: L{}] [Bad date: {}] {}'.format(
                i, j + 2, entry['date'], state))
            continue

        district = entry['district'].strip()
        if not district:
            district = 'Unassigned'
        elif district.lower() in DISTRICTS_DICT[state]:
            district = DISTRICTS_DICT[state][district.lower()]
        elif district.lower() in DISTRICTS_ADDITIONAL:
            district = DISTRICTS_ADDITIONAL[district.lower()]
        else:
            # Print unexpected district names
            logging.warning(
                '[V{}: L{}] [{}] [Unexpected district: {}] {}'.format(
                    i, j + 2, date, district, state))

        try:
            statistic = RAW_DATA_MAP[entry['patientstatus'].strip().lower()]

            inc(data[date]['TT']['delta'], statistic, 1)
            inc(data[date][state]['delta'], statistic, 1)
            ## Don't parse old district data since it's unreliable
            #  inc(data[date][state]['districts'][district]['delta'], statistic,
            #      1)
        except KeyError:
            # Unrecognized status
            logging.warning(
                '[V{}: L{}] [{}] [Bad patientstatus: {}] {}: {}'.format(
                    i, j + 2, date, entry['patientstatus'], state, district))


def parse_district_gospel(reader):
    for i, row in enumerate(reader):
        state = row['State_Code'].strip().upper()
        if state not in STATE_CODES.values():
            logging.warning('[{}] [Bad state: {}]'.format(i, state))
            continue
        district = row['District'].strip()
        if district.lower() in DISTRICTS_DICT[state]:
            district = DISTRICTS_DICT[state][district.lower()]

        for statistic in PRIMARY_STATISTICS:
            if row[statistic.capitalize()]:
                try:
                    data[GOSPEL_DATE][state]['districts'][district]['total'][
                        statistic] = int(row[statistic.capitalize()])
                except ValueError:
                    logging.warning('[{}] [Bad value for {}] {} {}'.format(
                        i, statistic, state, district))


def parse_icmr(icmr_data):
    for j, entry in enumerate(icmr_data['tested']):
        try:
            fdate = datetime.strptime(entry['updatetimestamp'].strip(),
                                      '%d/%m/%Y %H:%M:%S')
            date = datetime.strftime(fdate, '%Y-%m-%d')
            if date > INDIA_DATE:
                # Entries from future dates will be ignored
                logging.warning('[L{}] [Future timestamp: {}]'.format(
                    j + 2, entry['updatetimestamp']))
                continue
        except ValueError:
            # Bad timestamp
            logging.warning('[L{}] [Bad timestamp: {}]'.format(
                j + 2, entry['updatetimestamp']))
            continue

        count_str = entry['totalsamplestested'].strip()
        try:
            count = int(count_str)
        except ValueError:
            logging.warning('[L{}] [{}] [Bad totalsamplestested: {}]'.format(
                j + 2, entry['updatetimestamp'], entry['totalsamplestested']))
            continue

        data[date]['TT']['total']['tested'] = count
        data[date]['TT']['meta']['tested']['source'] = entry['source'].strip()
        data[date]['TT']['meta']['tested']['last_updated'] = date


def parse_state_test(state_test_data):
    for j, entry in enumerate(state_test_data['states_tested_data']):
        try:
            fdate = datetime.strptime(entry['updatedon'].strip(), '%d/%m/%Y')
            date = datetime.strftime(fdate, '%Y-%m-%d')
            if date > INDIA_DATE:
                # Entries from future dates will be ignored
                logging.warning('[L{}] [Future date: {}] {}'.format(
                    j + 2, entry['updatedon'], entry['state']))
                continue
        except ValueError:
            # Bad date
            logging.warning('[L{}] [Bad date: {}] {}'.format(
                j + 2, entry['updatedon'], entry['state']))
            continue

        state_name = entry['state'].strip().lower()
        try:
            state = STATE_CODES[state_name]
        except KeyError:
            # Entries having unrecognized state names are discarded
            logging.warning('[L{}] [{}] [Bad state: {}]'.format(
                j + 2, entry['updatedon'], entry['state']))
            continue

        count_str = entry['totaltested'].strip()
        try:
            count = int(count_str)
        except ValueError:
            logging.warning('[L{}] [{}] [Bad totaltested: {}] {}'.format(
                j + 2, entry['updatedon'], entry['totaltested'],
                entry['state']))
            continue

        data[date][state]['total']['tested'] = count
        data[date][state]['meta']['tested']['source'] = entry['source1'].strip(
        )
        data[date][state]['meta']['tested']['last_updated'] = date


def fill_tested():
    dates = sorted(data)
    for i, date in enumerate(dates):
        curr_data = data[date]

        # Initialize today's delta with today's cumulative
        for state, state_data in curr_data.items():
            if 'total' in state_data:
                if 'tested' in state_data['total']:
                    state_data['delta']['tested'] = state_data['total'][
                        'tested']

        if i > 0:
            prev_date = dates[i - 1]
            prev_data = data[prev_date]
            for state, state_data in prev_data.items():
                if 'tested' in state_data['total']:
                    if 'tested' in curr_data[state]['total']:
                        # Subtract previous cumulative to get delta
                        curr_data[state]['delta']['tested'] -= state_data[
                            'total']['tested']
                    else:
                        # Take today's cumulative to be same as yesterday's
                        # cumulative if today's cumulative is missing
                        curr_data[state]['total']['tested'] = state_data[
                            'total']['tested']
                        curr_data[state]['meta']['tested'][
                            'source'] = state_data['meta']['tested']['source']
                        curr_data[state]['meta']['tested'][
                            'last_updated'] = state_data['meta']['tested'][
                                'last_updated']


def accumulate():
    dates = sorted(data)
    for i, date in enumerate(dates):
        curr_data = data[date]

        if i > 0:
            # Initialize today's cumulative with previous available
            prev_date = dates[i - 1]
            prev_data = data[prev_date]
            for state, state_data in prev_data.items():
                for statistic in RAW_DATA_MAP.values():
                    if statistic in state_data['total']:
                        inc(curr_data[state]['total'], statistic,
                            state_data['total'][statistic])

                if state == 'TT' or date <= GOSPEL_DATE:
                    # Total state has no district data
                    # Old district data is already accumulated
                    continue

                for district, district_data in state_data['districts'].items():
                    for statistic in RAW_DATA_MAP.values():
                        if statistic in district_data['total']:
                            inc(
                                curr_data[state]['districts'][district]
                                ['total'], statistic,
                                district_data['total'][statistic])

        # Add today's dailys to today's cumulative
        for state, state_data in curr_data.items():
            if 'delta' in state_data:
                for statistic in RAW_DATA_MAP.values():
                    if statistic in state_data['delta']:
                        inc(state_data['total'], statistic,
                            state_data['delta'][statistic])

                if state == 'TT' or date <= GOSPEL_DATE:
                    # Total state has no district data
                    # Old district data is already accumulated
                    continue

                for district, district_data in state_data['districts'].items():
                    if 'delta' in district_data:
                        for statistic in RAW_DATA_MAP.values():
                            if statistic in district_data['delta']:
                                inc(district_data['total'], statistic,
                                    district_data['delta'][statistic])


def generate_timeseries(districts=False):
    for date in sorted(data):
        curr_data = data[date]

        for state, state_data in curr_data.items():
            for stype in ['total', 'delta']:
                if stype in state_data:
                    for statistic, value in state_data[stype].items():
                        timeseries[state][date][stype][statistic] = value

            if not districts or state == 'TT' or date <= GOSPEL_DATE:
                # Total state has no district data
                # District timeseries starts only from 26th April
                continue

            for district, district_data in state_data['districts'].items():
                for stype in ['total', 'delta']:
                    if stype in district_data:
                        for statistic, value in district_data[stype].items():
                            timeseries[state]['districts'][district][date][
                                stype][statistic] = value


def add_state_meta(raw_data):
    last_data = data[sorted(data)[-1]]
    for j, entry in enumerate(raw_data['statewise']):
        state = entry['statecode'].strip().upper()
        if state not in STATE_CODES.values():
            # Entries having unrecognized state codes are discarded
            logging.warning('[L{}] [{}] [Bad state: {}]'.format(
                j + 2, entry['lastupdatedtime'], entry['statecode']))
            continue

        try:
            fdate = datetime.strptime(entry['lastupdatedtime'].strip(),
                                      '%d/%m/%Y %H:%M:%S')
        except ValueError:
            # Bad timestamp
            logging.warning('[L{}] [Bad timestamp: {}] {}'.format(
                j + 2, entry['lastupdatedtime'], state))
            continue

        last_data[state]['meta']['last_updated'] = fdate.isoformat() + '+05:30'
        if entry['statenotes']:
            last_data[state]['meta']['notes'] = entry['statenotes'].strip()


def add_district_meta(raw_data):
    last_data = data[sorted(data)[-1]]
    for j, entry in enumerate(raw_data.values()):
        state = entry['statecode'].strip().upper()
        if state not in STATE_CODES.values():
            # Entries having unrecognized state codes are discarded
            logging.warning('[L{}] [Bad state: {}]'.format(
                j + 2, entry['statecode']))
            continue

        for district, district_data in entry['districtData'].items():
            district = district.strip()
            if district == 'Unknown':
                district = 'Unassigned'
            if district_data['notes']:
                last_data[state]['districts'][district]['meta'][
                    'notes'] = district_data['notes'].strip()


def tally_statewise(raw_data):
    last_data = data[sorted(data)[-1]]
    for j, entry in enumerate(raw_data['statewise']):
        state = entry['statecode'].strip().upper()
        if state not in STATE_CODES.values():
            # Entries having unrecognized state codes are discarded
            logging.warning('[L{}] [{}] [Bad state: {}]'.format(
                j + 2, entry['lastupdatedtime'], entry['statecode']))
            continue

        try:
            fdate = datetime.strptime(entry['lastupdatedtime'].strip(),
                                      '%d/%m/%Y %H:%M:%S')
        except ValueError:
            # Bad timestamp
            logging.warning('[L{}] [Bad timestamp: {}] {}'.format(
                j + 2, entry['lastupdatedtime'], state))
            continue

        for statistic in PRIMARY_STATISTICS:
            try:
                values = {
                    'total':
                    int(entry[statistic if statistic != 'deceased' else
                              'deaths'].strip()),
                    'delta':
                    int(entry['delta' + (statistic if statistic != 'deceased'
                                         else 'deaths').strip()])
                }
            except ValueError:
                logging.warning('[L{}] [{}] [Bad value for {}] {}'.format(
                    j + 2, entry['lastupdatedtime'], statistic, state))
                continue

            for stype in ['total', 'delta']:
                if values[stype]:
                    parsed_value = last_data[state][stype][statistic]
                    if not isinstance(parsed_value, int):
                        parsed_value = 0
                    if values[stype] != parsed_value:
                        # Print mismatch between statewise and parser
                        logging.warning(
                            '{} {} {}: (sheet: {}, parser: {})'.format(
                                state, statistic, stype, values[stype],
                                parsed_value))


def tally_districtwise(raw_data):
    last_data = data[sorted(data)[-1]]
    for j, entry in enumerate(raw_data.values()):
        state = entry['statecode'].strip().upper()
        if state not in STATE_CODES.values():
            # Entries having unrecognized state codes are discarded
            logging.warning('[L{}] [Bad state: {}]'.format(
                j + 2, entry['statecode']))
            continue

        for district, district_data in entry['districtData'].items():
            district = district.strip()
            if district == 'Unknown':
                district = 'Unassigned'

            for statistic in PRIMARY_STATISTICS:
                values = {
                    'total': district_data[statistic],
                    'delta': district_data['delta'][statistic]
                }
                for stype in ['total', 'delta']:
                    if values[stype]:
                        parsed_value = last_data[state]['districts'][district][
                            stype][statistic]
                        if not isinstance(parsed_value, int):
                            parsed_value = 0
                        if values[stype] != parsed_value:
                            # Print mismatch between districtwise and parser
                            logging.warning(
                                '{} {} {} {}: (sheet: {}, parser: {})'.format(
                                    state, district, statistic, stype,
                                    values[stype], parsed_value))


if __name__ == '__main__':
    logging.info('-' * PRINT_WIDTH)
    logging.info('{:{align}{width}}'.format('PARSER V3 START',
                                            align='^',
                                            width=PRINT_WIDTH))

    # Get possible state codes
    logging.info('-' * PRINT_WIDTH)
    logging.info('Parsing state meta data...')
    with open(STATE_META_DATA, 'r') as f:
        raw_data = json.load(f)
        parse_state_codes(raw_data)
    logging.info('Done!')

    # Get all actual district names
    logging.info('-' * PRINT_WIDTH)
    logging.info('Parsing districts list...')
    with open(DISTRICT_LIST, 'r') as f:
        reader = csv.DictReader(f)
        parse_district_list(reader)
    logging.info('Done!')

    # Parse raw_data's
    logging.info('-' * PRINT_WIDTH)
    logging.info('Parsing raw_data...')
    i = 1
    while True:
        f = INPUT_DIR / RAW_DATA.format(n=i)
        if not f.is_file():
            break
        with open(f, 'r') as f:
            raw_data = json.load(f)
            parse(raw_data, i)
        i += 1
    logging.info('Done!')

    # Parse additional deceased/recovered info not in raw_data 1 and 2
    logging.info('-' * PRINT_WIDTH)
    logging.info('Parsing deaths_recoveries...')
    for i in [1, 2]:
        f = INPUT_DIR / OUTCOME_DATA.format(n=i)
        with open(f, 'r') as f:
            raw_data = json.load(f)
            parse_outcome(raw_data, i)
    logging.info('Done!')

    logging.info('-' * PRINT_WIDTH)
    logging.info('Adding district data for 26th April...')
    # Parse gospel district data for 26th April
    with open(DISTRICT_DATA_GOSPEL, 'r') as f:
        reader = csv.DictReader(f)
        parse_district_gospel(reader)
    logging.info('Done!')

    logging.info('-' * PRINT_WIDTH)
    logging.info('Parsing ICMR test data for India...')
    f = ICMR_TEST_DATA
    with open(f, 'r') as f:
        raw_data = json.load(f, object_pairs_hook=OrderedDict)
        parse_icmr(raw_data)
    logging.info('Done!')

    logging.info('-' * PRINT_WIDTH)
    logging.info('Parsing test data for all states...')
    f = STATE_TEST_DATA
    with open(f, 'r') as f:
        raw_data = json.load(f, object_pairs_hook=OrderedDict)
        parse_state_test(raw_data)
    logging.info('Done!')

    logging.info('-' * PRINT_WIDTH)
    logging.info('Generating daily tested values...')
    fill_tested()
    logging.info('Done!')

    logging.info('-' * PRINT_WIDTH)
    logging.info('Generating cumulative CRD values...')
    # Generate total (cumulative) data points
    accumulate()
    logging.info('Done!')

    # Generate timeseries
    logging.info('-' * PRINT_WIDTH)
    logging.info('Generating timeseries...')
    generate_timeseries(districts=False)
    logging.info('Done!')

    logging.info('-' * PRINT_WIDTH)
    logging.info('Adding state/district metadata...')
    f = STATE_WISE
    with open(f, 'r') as f:
        raw_data = json.load(f, object_pairs_hook=OrderedDict)
        add_state_meta(raw_data)

    f = DISTRICT_WISE
    with open(f, 'r') as f:
        raw_data = json.load(f, object_pairs_hook=OrderedDict)
        add_district_meta(raw_data)
    logging.info('Done!')

    logging.info('-' * PRINT_WIDTH)
    logging.info('Dumping APIs...')
    OUTPUT_MIN_DIR.mkdir(parents=True, exist_ok=True)

    # Dump prettified full data json
    fn = '{}-{}'.format(OUTPUT_DATA_PREFIX, 'all')
    with open((OUTPUT_DIR / fn).with_suffix('.json'), 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
    # Dump minified full data
    with open((OUTPUT_MIN_DIR / fn).with_suffix('.min.json'), 'w') as f:
        json.dump(data, f, separators=(',', ':'), sort_keys=True)

    # Split data and dump separate json for each date
    for i, date in enumerate(sorted(data)):
        curr_data = data[date]
        if i < len(data) - 1:
            fn = '{}-{}'.format(OUTPUT_DATA_PREFIX, date)
        else:
            fn = OUTPUT_DATA_PREFIX

        with open((OUTPUT_DIR / fn).with_suffix('.json'), 'w') as f:
            json.dump(curr_data, f, indent=2, sort_keys=True)
        # Minified
        with open((OUTPUT_MIN_DIR / fn).with_suffix('.min.json'), 'w') as f:
            json.dump(curr_data, f, separators=(',', ':'), sort_keys=True)

    # Dump timeseries json
    with open((OUTPUT_DIR / OUTPUT_TIMESERIES_FILENAME).with_suffix('.json'),
              'w') as f:
        json.dump(timeseries, f, indent=2, sort_keys=True)
    with open(
        (OUTPUT_MIN_DIR / OUTPUT_TIMESERIES_FILENAME).with_suffix('.min.json'),
            'w') as f:
        json.dump(timeseries, f, separators=(',', ':'), sort_keys=True)

    logging.info('Done!')

    # Tally final date counts with statewise API
    logging.info('-' * PRINT_WIDTH)
    logging.info('Tallying final date counts with statewise sheet...')
    f = STATE_WISE
    with open(f, 'r') as f:
        raw_data = json.load(f, object_pairs_hook=OrderedDict)
        tally_statewise(raw_data)
    logging.info('Done!')

    # Tally final date counts with districtwise API
    logging.info('-' * PRINT_WIDTH)
    logging.info('Tallying final date counts with districtwise sheet...')
    f = DISTRICT_WISE
    with open(f, 'r') as f:
        raw_data = json.load(f, object_pairs_hook=OrderedDict)
        tally_districtwise(raw_data)
    logging.info('Done!')

    logging.info('-' * PRINT_WIDTH)
    logging.info('{:{align}{width}}'.format('PARSER V3 END',
                                            align='^',
                                            width=PRINT_WIDTH))
    logging.info('-' * PRINT_WIDTH)
