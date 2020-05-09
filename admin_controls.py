# This file handles all the admin functions

import database_linker


def cand_input(*args):
	""" Runs a GUI window that returns the input as {post:{cand1, cnad2, ...}}
		This input is then used to update the database with {cand_name:num_votes} """

	# GUI window code that gives input
	_input = args[0]  # Placeholder

	# Updates database with the names of candidates
	database_linker.initializing(_input)


def results():
	""" Runs a GUI window that takes {_id:post, cand1:votes, cand2:votes} as input
		and displays the output as the final results """

	final_results = {}

	for result in database_linker.results_data():
		temp = dict(result); del temp['_id']
		final_results[result.get('_id')] = temp

	return final_results
