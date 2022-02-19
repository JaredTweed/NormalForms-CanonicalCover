#include <time.h>
#include <vector>
#include <string>
#include <iostream>
#include "SkipList.h"

std::string randomKey() {
    char letter1 = (rand()%26) + 'A';
    char letter2 = (rand()%26) + 'a';
    return {letter1, letter2};
}
std::string randomValue() {
    char letter1 = (rand()%26) + 'a';
    char letter2 = (rand()%26) + 'a';
    char letter3 = (rand()%26) + 'a';
    char letter4 = (rand()%26) + 'a';

    return {letter1, letter2, letter3, letter4};
}

int main(int argc, char** argv) {
	unsigned seed = (unsigned)time(NULL);
	std::srand(seed);
	std::cout << "seed: " << seed << std::endl << std::endl;

	SkipList map;

	map.print();
	std::cout << std::endl;

	int n = 10;
	std::string key[n];

	for(int i=0; i<n; i++) {
	    key[i] = randomKey();
	    map.insert(key[i], randomValue());
	}

	map.print();
	std::cout << std::endl;

	for(int i=0; i<2; i++) {
		int index = rand() % n;
		map.remove(key[index]);
		key[index] = key[n-1];
		n--;
	}
	
	map.print();
	return 0;
}

