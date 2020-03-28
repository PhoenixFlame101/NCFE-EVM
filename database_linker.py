# This program connects the program to the Mongo database

from pymongo import MongoClient

# Connecting to the database from the host computer
client = MongoClient('mongodb://localhost:27017/')
db = client.EVM
collection = db.voting_results


def initializing(post_name, candidates):
	""" Used to add the candidates standing for the election to the DB
		Is run before the voting begins """
	rec = dict([[i, 0] for i in candidates])
	rec['_id'] = post_name
	id = collection.insert_one(rec)


# initializing('Head Girl', ['Cat', 'Mat'])

def add_votes_to_db(pointers):
	""" Used to increment the votes of the candidates who where voted for
		Is run after each person casts their vote """
	for vote in pointers.items():
		collection.update_one(
			{'_id': vote[0]},
			{'$inc': {vote[1]: 1}},
			upsert=False
		)


def results():
	return (collection.find({}))

# add_votes_to_db({'Head Boy': 'Rat', 'Head Girl': 'Cat'})