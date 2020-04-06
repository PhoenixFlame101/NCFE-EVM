# This is the program meant to run during the voting session


import admin_controls
# import sec_code
import database_linker
import gui

# Security code received by GUI
s_code = 'AES64'  # Placeholder

# We get the votes casts from the GUI after every session
# The dict is in the form {[post_name, candidate_voted_for]}
candidates = gui.main()

# We add the votes received per candidate to the votes of the resp. candidate in MongoDB
database_linker.add_votes_to_db(candidates)
