candidates = {1:0, 2:0, 3:0}
while True:
	try:
		vote = int(input())
	except:
		break
	candidates[vote] += 1
for x in candidates:
	print(f'Candidate {x} got {candidates[x]} votes')