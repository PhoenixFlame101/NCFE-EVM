# This file handles all the admin functions

import database_linker
import sec_code


def reset_pass(old_pass, new_pass, confirm_new_pass):
	if sec_code.pass_check(old_pass):
		if new_pass == confirm_new_pass:
			sec_code.pass_set(new_pass)
		else:
			raise ValueError('Passwords do not match')
	else:
		raise ValueError('Your old password is not correct')


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
