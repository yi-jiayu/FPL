import json
import logging
import os
import os.path
import sqlite3

from collections import OrderedDict

import requests

import tables as tables

# logging.basicConfig(level=logging.INFO)

files = {
    'bootstrap-static.json': 'https://fantasy.premierleague.com/drf/bootstrap-static',
    'fixtures.json': 'https://fantasy.premierleague.com/drf/fixtures/',
}
element_summaries_base_url = 'https://fantasy.premierleague.com/drf/element-summary/'


def download_bootstrap_files(dest):
    for basename, url in files.items():
        path = os.path.join(dest, basename)

        logging.info(f'Downloading "{url}" to "{path}"')
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)


def get_player_ids(conn):
    c = conn.cursor()
    c.execute('select id from players')
    rows = c.fetchall()

    return [r[0] for r in rows]


def download_element_summaries(dest, player_ids):
    total = len(player_ids)
    for i, pid in enumerate(player_ids):
        url = f'{element_summaries_base_url}{pid}'
        path = os.path.join(dest, f'{pid}.json')

        logging.info(f'Downloading "{url}" to "{path}" ({i} of {total})')
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)


def load_element_summaries(prefix, player_ids):
    element_summaries = []
    for pid in player_ids:
        path = os.path.join(prefix, f'{pid}.json')
        with open(path, encoding='utf-8') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
        history = data['history']
        element_summaries.append(history)
    return element_summaries


def create_events_table(conn, events, table_name='events'):
    column_constraints = {
        'id': 'primary key',
    }

    with conn:
        schema = tables.generate_table_schema(events, column_constraints=column_constraints)
        tables.create_table(conn, schema, table_name)
        tables.populate_table(conn, schema, table_name, events)


def create_roles_table(conn, roles, table_name='roles'):
    column_constraints = {
        'id': 'primary key',
    }

    with conn:
        schema = tables.generate_table_schema(roles, column_constraints=column_constraints)
        tables.create_table(conn, schema, table_name)
        tables.populate_table(conn, schema, table_name, roles)


def create_teams_table(conn, teams, table_name='teams'):
    column_constraints = {'id': 'primary key'}
    exclude_columns = {'current_event_fixture', 'next_event_fixture', 'form'}

    with conn:
        schema = tables.generate_table_schema(teams, exclude_columns=exclude_columns,
                                              column_constraints=column_constraints)
        tables.create_table(conn, schema, table_name)
        tables.populate_table(conn, schema, table_name, teams, exclude_columns=exclude_columns)


def create_fixtures_table(conn, fixtures, table_name='fixtures'):
    exclude_columns = {'stats'}
    column_constraints = {
        'id': 'primary key',
        'team_a': 'references teams(id)',
        'team_h': 'references teams(id)',
        'event': 'references events(id)'
    }

    with conn:
        schema = tables.generate_table_schema(fixtures, exclude_columns=exclude_columns,
                                              column_constraints=column_constraints)
        tables.create_table(conn, schema, table_name)
        tables.populate_table(conn, schema, table_name, fixtures, exclude_columns=exclude_columns)


def create_players_table(conn, players, table_name='players'):
    column_constraints = {
        'id': 'primary key',
        'team': 'references teams(id)',
        'element_type': 'references roles(id)'
    }

    with conn:
        schema = tables.generate_table_schema(players, column_constraints=column_constraints)
        tables.create_table(conn, schema, table_name)
        tables.populate_table(conn, schema, table_name, players)


def create_player_match_details_table(conn, element_summaries, table_name='player_match_details'):
    example = element_summaries[0]
    column_constraints = {
        'id': 'primary key',
        'fixture': 'references fixtures(id)',
        'element': 'references players(id)',
        'round': 'references events(id)',
        'opponent_team': 'references teams(id)'
    }

    with conn:
        schema = tables.generate_table_schema(example, column_constraints=column_constraints)
        tables.create_table(conn, schema, table_name)

        for e in element_summaries:
            tables.populate_table(conn, schema, table_name, e)


def main():
    database_file = 'fpl.sqlite'
    download_dir = 'downloads'

    try:
        os.mkdir(download_dir)

        print('Downloading bootstrap files...')
        download_bootstrap_files(download_dir)
    except FileExistsError:
        pass

    with open(os.path.join(download_dir, 'bootstrap-static.json'), encoding='utf-8') as f:
        bootstrap_static = json.load(f, object_pairs_hook=OrderedDict)

    events = bootstrap_static['events']
    roles = bootstrap_static['element_types']
    teams = bootstrap_static['teams']
    players = bootstrap_static['elements']

    with open(os.path.join(download_dir, 'fixtures.json'), encoding='utf-8') as f:
        fixtures = json.load(f, object_pairs_hook=OrderedDict)

    print('Using database file:', database_file)
    conn = sqlite3.connect(database_file)

    print('Creating events table...')
    create_events_table(conn, events)

    print('Creating roles table...')
    create_roles_table(conn, roles)

    print('Creating teams table...')
    create_teams_table(conn, teams)

    print('Creating players table...')
    create_players_table(conn, players)

    print('Creating fixtures table...')
    create_fixtures_table(conn, fixtures)

    print('Downloading element summaries...')
    player_ids = get_player_ids(conn)
    element_summaries_dir = os.path.join(download_dir, 'element-summaries')

    try:
        os.mkdir(element_summaries_dir)
        download_element_summaries(element_summaries_dir, player_ids)
    except FileExistsError:
        pass

    print('Loading element summaries...')
    element_summaries = load_element_summaries(element_summaries_dir, player_ids)

    print('Creating player_match_details table...')
    create_player_match_details_table(conn, element_summaries)

    conn.close()
    print('Done!')


if __name__ == '__main__':
    main()
