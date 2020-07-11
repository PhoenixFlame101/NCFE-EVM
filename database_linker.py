# This program connects the program to the Mongo database

from pymongo import MongoClient
from fpdf import FPDF

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
		post_name = tup[0]
		candidates = list(tup[1])
		record = dict([[i, 0] for i in candidates])
		record['_id'] = post_name
		id = collection.insert_one(record)


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
			upsert=False
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
				pdf.cell(200, 10, txt=f'{key}     {value}', align='C')
				pdf.ln(7)
		else:
			pdf.ln()
	pdf.output('results.pdf')

	# Drops database
	# client.drop_database('EVM')

# initializing({'Head Boy':{'Cat', 'Bat'}, 'Head Girl':{'Rat', 'Mat'}})
# results_print()
