# This program connects the program to the Mongo database

from pymongo import MongoClient

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
		candidates = [i for i in tup[1].items()]
		record = dict([[i, 0] for i in candidates])
		record['_id'] = post_name
		id = collection.insert_one(record)


def add_votes_to_db(pointers):
	""" Used to increment the votes of the candidates who where voted for
		Is run after each person casts their vote """
	for vote in pointers.values():
		post_name, cand_name = vote[0], vote[1]
		collection.update_one(
			{'_id': post_name},
			{'$inc': {cand_name: 1}},
			upsert=False
		)


def results_data():
	return list(collection.find({}))

