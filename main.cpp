/*

    This is the main file that controls the backend.

*/

#include <stdio.h>
#include <iostream>
using namespace std;

int main () {
    
	int vote;	    	// vote is the vote cast by the user
	int c1, c2, c3;		// c1, c2 and c3 are the candidates

    cout << "Enter a number from 1 to 3";		// user votes for either candidate 1, 2 or 3
    cin >> vote;								// vote is accounted for

    if(vote = 1)
    {
        c1++;		// candidate 1 gets the vote
    }

    else if(vote = 2)
    {
        c2++;		// candidate 2 gets the vote
    }

    else if(vote = 3)
    {
        c3++;		// candidate 3 gets the vote
    }
    
    if(c1 > c2 && c1 > c3)			// candidate 1 gets the most votes
    {
    	cout << "Cadidate 1 has won the election";
    }

    else if(c2 > c1 && c2 > c3)		// candidate 2 gets the most votes
    {
    	cout << "Cadidate 2 has won the election";
    }

    else if(c3 > c1 && c3 > c2)		// candidate 3 gets the most votes
    {
    	cout << "Cadidate 3 has won the election";
    }

}