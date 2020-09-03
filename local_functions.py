# This module contains functions that are device specific

def store_house_choice(choice):
    try:
        with open('local_vars.encrypted', 'r+') as f:
            uri = f.readlines()[-1]
            f.truncate(0)
            f.seek(0)
            f.writelines([f'House Choice: {choice.lower()}'+'\n', uri])
    except:
        with open('local_vars.encrypted', 'w+') as f:
            f.writelines([f'House Choice: {choice.lower()}'+'\n'])


def get_house_choice():
    with open('local_vars.encrypted', 'r+') as f:
        return f.readlines()[0][14:-1]


def store_db_uri(uri):
    try:
        with open('local_vars.encrypted', 'r+') as f:
            house_choice = f.readlines()[0]
            f.truncate(0)
            f.seek(0)
            f.writelines([house_choice, f'DB URI: {uri}'])
    except:
        with open('local_vars.encrypted', 'w+') as f:
            f.writelines(['\n', f'DB URI: {uri}'])


def get_db_uri():
    with open('local_vars.encrypted', 'r+') as f:
        return f.readlines()[1][8:]


store_house_choice('choice')
store_db_uri('uri')
