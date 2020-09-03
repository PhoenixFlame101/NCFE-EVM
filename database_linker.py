# This module connects the program to the Mongo database

from pymongo import MongoClient
from fpdf import FPDF
from local_functions import get_db_uri

# Connecting to the database from the host computer
client = MongoClient(get_db_uri())
db = client.EVM
collection = db.voting_results


def initializing(_input):
	""" Used to add the candidates standing for the election to the DB
		Is run before the voting begins """

	collection.drop()

	# Takes _input in the form {post:{cand1, cand2, ...}}
	for tup in _input.items():
		post_name = ' '.join(tup[0].split('_')).title()
		candidates = list(map(lambda x: x.title(), tup[1]))
		record = dict([[i, 0] for i in candidates])
		record['_id'] = post_name
		collection.insert_one(record)


def get_cands_from_db():
	""" Gets the candidate names from the database for the GUI """

	temp = {}  # Dictionary that will be returned

	values = list(collection.find({}))
	for post in values:
		cands = set()
		for key, value in post.items():
			if key == '_id':
				post_name = '_'.join(value.split()).lower()
			else:
				cands.add(key)
		else:
			temp[post_name] = cands

	# Return value is of the type {post:{cand1, cand2, ...}}
	return temp


def add_votes_to_db(pointers):
	""" Used to increment the votes of the candidates who where voted for
		Is run after each person casts their vote """

	for vote in pointers.items():
		post_name, cand_name = vote[0], vote[1]
		post_name, cand_name = ' '.join(post_name.split('_')[:-1]).title(), cand_name.title()
		print(post_name, cand_name)
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
	for post in results:  # The results list is a list of MongoDB documents
		for key, value in post.items():
			# If the current value contans the post name, use it as a heading
			if key == '_id':
				pdf.set_font("Arial", 'U', size=14)
				pdf.cell(200, 10, txt=value, align='C')
				pdf.ln(7)
			else:
				pdf.set_font("Arial", size=12)
				pdf.cell(55, 10)
				pdf.cell(75, 10, txt=key, align='L')
				pdf.cell(10, 10, txt=str(value), align='C')
				pdf.ln(7)
		else:
			pdf.ln()
	pdf.output('results.pdf')

	# Drops colleciton after voting is over
	#collection.drop()


# Functions to facilitate db actions in sec_code.py
def add_password_to_db(password):
	db.admin.drop()
	db.admin.insert_one({'_id': 'password', 'password': password})
def add_codes_to_db(codes):
	db.codes.drop()
	db.codes.insert_one({'_id': 'codes', 'codes': codes})
def get_password_from_db():
	return db.admin.find({})[0]['password']
def get_codes_from_db():
	return db.codes.find({})[0]['codes']


'''
initializing({'head_boy': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'head_girl': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'assistant_head_boy': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'assistant_head_girl': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'cultural_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'cultural_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'sports_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'sports_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'kingfisher_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'kingfisher_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'flamingo_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'flamingo_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'falcon_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'falcon_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'eagle_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
'eagle_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'}})'''
# results_print()
