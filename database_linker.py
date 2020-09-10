# This module connects the program to the Mongo database

from pymongo import MongoClient
from fpdf import FPDF
from local_functions import get_db_uri

# Connecting to the database from the host computer
client = MongoClient('mongodb://localhost:27017/')
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
		cands = []
		for key, value in post.items():
			if key == '_id':
				post_name = '_'.join(value.split()).lower()
			else:
				cands.append(key)
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
	collection.drop()


# Functions to facilitate db actions in sec_code.py
def add_password_to_db(password):
	db.admin.drop()
	db.admin.insert_one({'_id': 'password', 'password': password})
def add_codes_to_db(codes):
	db.codes.delete_one({'_id': 'codes'})
	db.codes.insert_one({'_id': 'codes', 'codes': codes})
def add_codes_to_used(codes):
	db.codes.delete_one({'_id': 'used_codes'})
	db.codes.insert_one({'_id': 'used_codes', 'used_codes': codes})
def get_password_from_db():
	return db.admin.find({})[0]['password']
def get_codes_from_db():
	return db.codes.find_one({'_id': 'codes'})['codes']
def get_used_codes():
	return db.codes.find_one({'_id': 'used_codes'})['used_codes']


'''
posts = {'head_boy','head_girl','assistant_head_boy','assistant_head_girl',
'cultural_captain','cultural_vice_captain','sports_captain','sports_vice_captain',
'kingfisher_captain','kingfisher_vice_captain','flamingo_captain',
'flamingo_vice_captain','falcon_captain','falcon_vice_captain',
'eagle_captain','eagle_vice_captain'}
temp_cands = {'A','B','C','D'}
x = {}
for post in posts:
	x[post] = temp_cands
initializing(x)'''

# results_print()
