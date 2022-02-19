/*
CMPT 125 Assignment 4 Game
Author: Jared Matthew Tweed
Student ID: 301439536, jmt25
SFU email: jared_tweed@sfu.ca
Academic honesty statement: I hereby confirm that this is my own work and I have
not violated any of SFU’s Code of Academic Integrity and Good Conduct (S10.01).
Description: These functions implement the core functionalities to make the 
game work.
*/

#include "gameFunctions.h"

void addCardToPlayer(Player* thePlayer, Card* theCard){
  //This adds the card to the end of the player's winpile list.
  insertEndCard_LList(&thePlayer->winPile, theCard);
  
  //updating the winpile size counter.
  thePlayer->cardsWon++;
  
  //This sets the card's value to 0 so that it can be recognized as taken.
  theCard->value = 0; 
}

bool checkPlayerInput(Deck* theDeck, Player* thePlayer, char row, char col){
  //transform the row, column, and index values into integers.
  unsigned int intRow = row - '0';
  unsigned int intCol = col - 'a';
  unsigned int index = intCol + intRow*13;
    
  /*This returns true if the row and columns are in a valid range 
  and the card is not already taken in a previous turn.*/
  if(intCol >= 13 || intRow >= 4){ 
    printf("Error: The card you picked has invalid index(es).\n");
    return false;
  } else if(theDeck->cards[index].value == 0){
    printf("Error: The card you picked is already taken.\n");
    return false;
  } else {
    return true;
  }
  //the player variable is not needed.
}

bool checkForMatch(Deck* theDeck, Player* thePlayer, char r1, char c1, char r2, char c2){
  //find the index values of both cards selected.
  unsigned int i1 = (c1 - 'a') + (r1 - '0')*13;
  unsigned int i2 = (c2 - 'a') + (r2 - '0')*13;
  
  /*This returns true if and only if both cards have the same value despite 
  being different cards with a different suit.*/
  if(i1 == i2){
    printf("Error: Both cards are the same.\n\n");
    return false;
  } else if(theDeck->cards[i1].value == theDeck->cards[i2].value){
    printf("\n");
    return true;
  } else {
    printf("\n");
    return false;
  }
}

bool checkForWinner(const Deck* theDeck){
  /*This scans all the cards in the deck and returns false if any card has 
  not been taken yet. Otherwise, it returns true.*/
  for(int i = 0; i < NUM_OF_CARDS_IN_DECK; i++){
    if(theDeck->cards[i].value != 0){
      return false;
    }
  }
  return true;
}

