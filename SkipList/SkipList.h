#include <string>
#include <vector>

typedef std::string Key;
typedef std::string Value;

class SkipList {
    public:
	class Entry {
	    public:
		Key& getKey() {return key;}
		Value& getValue() {return value;}

	    private:
		Entry(Key k, Value v) : key(k), value(v) {}
		Key key;
		Value value;
	    friend class SkipList;
	};

	SkipList();

	Entry* find(Key k);
	void print();
        void insert(Key k, Value v);
        void remove(Key k);
	Entry* ceilingEntry(Key k);
	Entry* floorEntry(Key k);
	Entry* greaterEntry(Key k);
	Entry* lesserEntry(Key k);

    private:
	class Quad {
	    private:
	        Quad* prev;
	        Quad* next;
	        Quad* above;
	        Quad* below;

		Entry* entry;

		Quad(Entry* e) : entry(e) {}
	    friend class SkipList;
	};

	std::vector<Quad*> listHeads;
	void makeNewLevelList();
	void printOneList(int listNum);

	std::vector<Quad*>* findWithTrail(Key k);

};
