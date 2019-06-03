
#    This is the main file that controls the backend.

vote = int(input("Enter vote: ")) # vote is cast by the user

c1 = 0
c2 = 0
c3 = 0

if (vote == 1):
	c1 += 1
elif (vote == 2):
	c2 += 1
elif (vote == 3):
	c3 += 1
else:
	print('Error: Invalid Vote.  Please Try Again.')

# if (c1 != 0) and (c2 != 0) and (c3 != 0):
if (c1 == c2) and (c1 != c3):
	print('Candidate 1 and 2 are tied with', c1, 'votes')
	print('Candidate 3 has got', c3, 'votes')

elif (c2 == c3) and (c2 != c1):
	print('Candidate 2 and 3 are tied with', c2, 'votes')
	print('Candidate 1 has got', c1, 'votes')

elif (c1 == c2) and (c2 == c3):
	print('Candidate 1 and 2 and 3 are tied with', c1, 'votes')	

elif (c1 > c2) and (c1 > c3):
	print('Candidate 1 has won the election with', c1, 'votes')
	print('Candidate 2 has got', c2, 'votes')
	print('Candidate 3 has got', c3, 'votes')

elif (c2 > c1) and (c2 > c3):
	print('Candidate 2 has won the election with', c2, 'votes')
	print('Candidate 1 has got', c1, 'votes')
	print('Candidate 3 has got', c3, 'votes')

elif (c2 > c1) and (c2 > c3):
	print('Candidate 3 has won the election with', c3, 'votes')
	print('Candidate 1 has got', c1, 'votes')
	print('Candidate 2 has got', c2, 'votes')

input('Press ENTER to exit')