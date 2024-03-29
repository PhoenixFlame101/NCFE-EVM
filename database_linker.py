""" This module connects the program to the Mongo database """

from pymongo import MongoClient
from fpdf import FPDF
from local_functions import get_db_uri

# Connecting to the database hosted on the main computer
client = MongoClient(get_db_uri())  # URI is stored in local_var.encrypted
db = client.EVM
collection = db.voting_results


def initializing(_input):
    """ Used to add the candidates standing for the election to the DB
        Is run before the voting begins """

    collection.drop()

    # Takes _input in the form {post:{cand1, cand2, ...}} and convets it to
    # the dict {'_id':post, cand1:0, cand2:0, ...} and adds it to the db
    for tup in _input.items():
        post_name = ' '.join(tup[0].split('_')).title()
        candidates = list(map(lambda x: x.title(), tup[1]))
        record = {i:0 for i in candidates}
        record['_id'] = post_name
        collection.insert_one(record)


def get_cands_from_db():
    """ Gets the candidate names from the database """

    temp = {}  # Dictionary that will be returned

    # 'values' is a list of documents (dictionaries) in the collections
    values = list(collection.find({}))
    for post_document in values:
        cands = []
        for key, value in post_document.items():
            if key == '_id':
                post_name = '_'.join(value.split()).lower()
            else:
                cands.append(key)
        temp[post_name] = cands

    # Return value is of the type {post:{cand1, cand2, ...}}
    return temp


def add_votes_to_db(pointers):
    """ Used to increment the votes of the candidates who where voted for d"""

    for vote in pointers.items():
        post_name, cand_name = ' '.join(vote[0].split('_')[:-1]).title(), vote[1].title()
        collection.update_one(
            {'_id': post_name},
            {'$inc': {cand_name: 1}},
            upsert=True
        )


def results_print():
    """ Used to print the results in PDF format """

    # Results are taken from the MongoDB database
    results = list(collection.find({}))

    # Writes the results to a PDF file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'BU', size=22)
    pdf.cell(200, 10, txt='RESULTS', align='C')
    pdf.ln(20)
    # 'results' is a list of MongoDB documents (dictionaries)
    for post in results:
        if len(post.items()) > 2:
            total_num_votes = sum(_ for _ in post.values() if isinstance(_, int))
            for key, value in post.items():
                # If the current value contains the post name, use it as a heading
                if key == '_id':
                    pdf.set_font("Arial", 'U', size=14)
                    pdf.cell(200, 10, txt=value, align='C')
                    pdf.ln(10)
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt='Total Votes: '+str(total_num_votes), align='C')
                    pdf.ln(7)
                else:
                    pdf.set_font("Arial", size=12)
                    pdf.cell(55, 10)
                    pdf.cell(75, 10, txt=key, align='L')
                    pdf.cell(10, 10, txt=str(value), align='C')
                    pdf.ln(7)
            pdf.ln()
    pdf.output('results.pdf')

    # Drops colleciton and codes after voting is over
    collection.drop()
    db.codes.drop()


def add_password_to_db(password):
    """ Adds password to database; called in pass_set() """
    db.admin.delete_one({'_id': 'password'})
    db.admin.insert_one({'_id': 'password', 'password': password})


def add_codes_to_db(codes, first_run=False):
    """ Adds codes to database; called in code_gen() if there are no codes """
    if first_run:
        if not get_codes_from_db():
            db.codes.delete_one({'_id': 'codes'})
            db.codes.insert_one({'_id': 'codes', 'codes': codes})
            return True
        return False
    else:
        db.codes.delete_one({'_id': 'codes'})
        db.codes.insert_one({'_id': 'codes', 'codes': codes})


def add_codes_to_used(codes):
    """ Moves codes from 'codes' to 'used_codes' in the database """
    db.codes.delete_one({'_id': 'used_codes'})
    db.codes.insert_one({'_id': 'used_codes', 'used_codes': codes})


def set_voting_status(*args):
    """ Sets the voting status in the db; and returns it if no arguements are given """
    if args:
        db.admin.delete_one({'_id': 'voting_status'})
        db.admin.insert_one({'_id': 'voting_status', 'voting_status': args[0]})
    else:
        try:
            return db.admin.find_one({'_id': 'voting_status'})['voting_status']
        except IndexError:
            set_voting_status(False)
            return False


def set_voting_order(*args):
    """ Sets the voting order in the db; and returns it if no arguements are given """
    if args:
        db.admin.delete_one({'_id': 'voting_order'})
        db.admin.insert_one({'_id': 'voting_order', 'voting_order': args[0]})
    else:
        try:
            return db.admin.find_one({'_id': 'voting_order'})['voting_order']
        except IndexError:
            set_voting_order(['head_boy', 'head_girl', 'assistant_head_boy', 'assistant_head_girl',
                              'cultural_captain', 'cultural_vice_captain', 'sports_captain', 'sports_vice_captain'])
            return ['head_boy', 'head_girl', 'assistant_head_boy', 'assistant_head_girl',
                    'cultural_captain', 'cultural_vice_captain', 'sports_captain', 'sports_vice_captain']


def get_password_from_db():
    """ Returns admin password stored in the db; if it doesn't exist, 123 is the fallback """
    password = ''
    try:
        password = db.admin.find_one({'_id': 'password'})['password']
    except IndexError:
        password = b'gAAAAABfrRgTi_h2Iy9p46-yTy92DgCX6hmsyUSykA0CCPjl2Cx3rX_xOoe5XesGvy_IkQixVqrMcmmausv4S6aCbSnj_wcIug=='
        add_password_to_db(
            b'gAAAAABfrRgTi_h2Iy9p46-yTy92DgCX6hmsyUSykA0CCPjl2Cx3rX_xOoe5XesGvy_IkQixVqrMcmmausv4S6aCbSnj_wcIug==')
    return password


def get_codes_from_db():
    """ Returns unused codes from the db if available; called in code_is_valid() """
    try:
        return db.codes.find_one({'_id': 'codes'})['codes']
    except TypeError:
        return False

def get_used_codes():
    """ Returns used codes from the db; used to check if a code is reused """
    return db.codes.find_one({'_id': 'used_codes'})['used_codes']


'''
initializing({'head_boy': ['Apple', 'Banana', 'Orange', '123', '456'], 'kingfisher_captain': ['Mango', 'Cherry', 'Kiwi', 'Red Grapes', 'Red Stuff'], 'head_girl': ['789', 'A', 'B', 'C', 'Cereal Bowl'], 'sports_captain': ['D', 'E', 'Tomatoes', 'Strawberries'], 'cultural_captain': ['Long Boi', 'Salad', 'Q', 'W', 'F'], 'assistant_head_boy': [], 'assistant_head_girl': ['G', 'H', 'I', 'J', 'K'], 'sports_vice_captain': ['Sandwich', 'Spices', 
'S'], 'cultural_vice_captain': ['Z', 'Y', 'X', 'L'], 'flamingo_captain': ['W', 'Y', 'Garlic Bread'], 'falcon_captain': ['O', 'P', 'M', 'N'], 'eagle_captain': ['Ladybug', 'Lemon Slices', 'Heart Fruit'], 'kingfisher_vice_captain': ['Hacker', 'Cookies', 'Avacado', 'Pastry'], 'flamingo_vice_captain': ['Nuggets', 'Orange Bowl', 'Pineapple', 'Pink Pineapple'], 'falcon_vice_captain': ['Sliced Fruit', 'Lemon Tree', 'Lemon', 'Essential Oil', 'R'], 'eagle_vice_captain': ['T', 'U', 'Strawberry Boxes'], 'liaison': ['69420', 'Grapefruit'], 'vice_liaison': ['Sunflower'], 'kingfisher_prefect': ['Fruit Model', 'Lemon Egg'], 'falcon_prefect': ['Bob', 'Joe'], 'flamingo_prefect': ['Happy Boi', 'Egg Lemon'], 'eagle_prefect': ['Ur', 'Mother']})
'''
