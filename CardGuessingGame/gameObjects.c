/*
CMPT 125 Assignment 4 Game
Author: Jared Matthew Tweed
Student ID: 301439536, jmt25
SFU email: jared_tweed@sfu.ca
Academic honesty statement: I hereby confirm that this is my own work and I have
not violated any of SFU’s Code of Academic Integrity and Good Conduct (S10.01).
Description: These files implement functions that manages the entities of the game.
*/

#include "gameObjects.h"

void initializeDeck(Deck* theDeck, char* brandName){
  //set the brand name.
  theDeck->brand = brandName;
    
  // sets the card values and suits each represented by a character.
  for (int i = 0; i < NUM_OF_CARDS_IN_DECK; i++){
    //the suit changes every 13 cards.
    theDeck->cards[i].suit = i/13;

    //sets the values depending on their position in the array.
    if (0 == (i%13)){
      theDeck->cards[i].value = 'A';
    } else if (1 <= (i%13) && (i%13) <= 8) {
      theDeck->cards[i].value = (i%13) + '1';
    } else if (9 == (i%13)) {
      theDeck->cards[i].value = 'T';
    } else if (10 == (i%13)) {
      theDeck->cards[i].value = 'J';
    } else if (11 == (i%13)) {
      theDeck->cards[i].value = 'Q';
    } else if (12 == (i%13)) {
      theDeck->cards[i].value = 'K';
    } else { //In case of error, there will be a joker
      theDeck->cards[i].value = 'j';
    }
  }
}

//This shuffles the deck with the given algorithm.
void shuffleDeck(Deck* theDeck){
  int n = 52;
  if (n > 1) {
    size_t i;
    for (i = 0; i < n - 1; i++) {
      size_t j = i + rand() / (RAND_MAX / (n - i) + 1);
      Card t = theDeck->cards[j];
      theDeck->cards[j] = theDeck->cards[i];
      theDeck->cards[i] = t;
    }
  }
}

void printDeck(const Deck* theDeck, bool faceUp){
  //print column letters
  printf("   a  b  c  d  e  f  g  h  i  j  k  l  m\n");
    
  //prints every card
  for (int i = 0; i < NUM_OF_CARDS_IN_DECK; i++){
        
    //prints row numbers
    if(i%13 == 0){
       printf("%c ", i/13 + '0');
    } else {
       printf(" ");
    }
        
        
    if(theDeck->cards[i].value == 0){
      //this prints a taken card.
      printf("  ");
    } else if(faceUp == true){
      //prints the value of the card
      printf("%c", theDeck->cards[i].value);
            
      //prints the suit of the card
      if (theDeck->cards[i].suit == Spades) {
        printf("\u2660"); //prints the spades symbol
      } else if (theDeck->cards[i].suit == Hearts) {
        printf("\u2661"); //prints the hearts symbol
      } else if (theDeck->cards[i].suit == Diamonds) {
        printf("\u2662"); //prints the diamonds symbol
      } else if (theDeck->cards[i].suit == Clubs) {
        printf("\u2663"); //prints the clubs symbol
      }            
    } else {
      //prints facedown cards.
      printf("%c\u218C", '?');
    }
        
    //The newline at the end of each row.
    if(i%13 == 12){
      printf("\n");
    }
  }
  printf("\n");
}

void initializePlayer(Player* thePlayer, char* theName){
  /*This assigns the players name and gives the 
  player an empty pile of cards won.*/
  thePlayer->name = theName;
  thePlayer->cardsWon = 0; 
  
  //createCard_LList() is not used because winPile is already created.
  //This assigns the winPile to have an empty/NULL head and tail.
  thePlayer->winPile.head = NULL;
  thePlayer->winPile.tail = NULL;
}

void clearPlayer(Player* thePlayer){
  /*This empties the player's pile of cards won, 
  and sets the number of cardsWon to 0.*/
  thePlayer->cardsWon = 0;
  clearCard_LList(&thePlayer->winPile);
}

