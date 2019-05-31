#include <stdio.h>
#include <iostream>
using namespace std;

int main () {
    
	int vote;
	int vf1, vf2, vf3;

    cout << "Enter a number from 1 to 3";
    cin >> vote;

    if(vote = 1)
    {
        vf1++;
    }

    else if(vote = 2)
    {
        vf2++;
    }

    else if(vote = 3)
    {
        vf3++;
    }
    
    if(vf1 > vf2 && vf1 > vf3)
    {
    	cout << "Cadidate 1";
    }

    else if(vf2 > vf1 && vf2 > vf3)
    {
    	cout << "Cadidate 2";
    }

    else if(vf3 > vf2 && vf3 > vf1)
    {
    	cout << "Cadidate 3";
    }

}