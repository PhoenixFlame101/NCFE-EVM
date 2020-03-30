# This is the program meant to run during the voting session

import sec_code
import gui
import database_linker

# Security code received by GUI
s_code = 'AES64'  # Placeholder

candidates = {}

if sec_code.checks_code(s_code):
	# We get the votes casts from the GUI after every session
	# The dict is in the form {[post_name, candidate_voted_for]}
	candidates = gui.main()
	pass  # Placeholder

# We add the votes received per candidate to the votes of the resp. candidate in MongoDB
database_linker.add_votes_to_db(candidates)

# Results block
# print(results())