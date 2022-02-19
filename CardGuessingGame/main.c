/*
CMPT 125 Assignment 4 Game
Author: Jared Matthew Tweed
Student ID: 301439536, jmt25
SFU email: jared_tweed@sfu.ca
Academic honesty statement: I hereby confirm that this is my own work and I have
not violated any of SFU’s Code of Academic Integrity and Good Conduct (S10.01).
Description: This is the source code for the game. In implements the main
function that is the driver of the program. In also includes a clear function
that attemps to "push" the face up print up beyond the screen.
*/

#include <stdio.h>
#include <stdlib.h> //for the use of system and srand and rand
#include "gameObjects.h"
#include "gameFunctions.h"

#define MAX_CHAR_NUMBER 16 //each input should have at most 15 characters

//a helper function that clears the screen, works for both unix and Windows,
//though behaviour might be different.
//reference: https://stackoverflow.com/questions/2347770/
//            how-do-you-clear-the-console-screen-in-c
void clear() {
  #if defined(__linux__) || defined(__unix__) || defined(__APPLE__)
    system("printf '\33[H\33[2J'");
  #endif

  #if defined(_WIN32) || defined(_WIN64)
    system("cls");
  #endif
}

int main() {
  //set the random seed to 0, it'll generate the same sequence
  //normally it is srand(time(NULL)) so the seed is different in every run
  //using 0 makes it deterministic so it is easier to mark
  //do not change it
  srand(0);

  //variables to store user input
  /*char userInput1[MAX_CHAR_NUMBER];
  char userInput2[MAX_CHAR_NUMBER];
  int whereInDeck = 0; //handy for indexing which card based on user input*/

  //set up the players
  Player player1, player2;
  initializePlayer(&player1, "Player 1");
  initializePlayer(&player2, "Player 2");
  Player* currentPlayer = &player1; //this pointer remembers who's turn it is

  //set up the deck: initalize & shuffle
  Deck myDeck;
  initializeDeck(&myDeck, "Bicycle");
  shuffleDeck(&myDeck);
  
  printDeck(&myDeck, true); //print the shuffled deck, face up
  printf("\n");
  clear(); //clear the screen

  /*
  Implement this part for the game to work.
  It is essentially a do-while loop that repeatedly print the deck,
  ask for user inputs, and do some checking. Ends if someone wins.
  */
  do {
    /////////////////////
    // 1 Round
    ////////////////////
    //Step 1: print the shuffled deck, face down
    printDeck(&myDeck, false);


    //Step 2: print who's turn it is by showing the player's name
    printf("%s's turn.\n", currentPlayer->name);


    //Step 3.1 get first input from player,
    // keep asking until the input is valid (hint: use a do-while loop)
    // you can assume that the format is correct (a digit<space>a letter)
    char firstRow, firstCol; 
    do {
      printf("Pick the first card you want to turn (e.g., 0 a) then press enter: ");
      scanf(" %c %c", &firstRow, &firstCol);
    } while (!checkPlayerInput(&myDeck, currentPlayer, firstRow, firstCol));

    //Step 3.2: get second input from player,
    // keep asking until the input is valid (hint: use a do-while loop)
    // you can assume that the format is correct (a digit<space>a letter)
    char secondRow, secondCol;
    do {
      printf("Pick the second card you want to turn (e.g., 1 b) then press enter: ");
      scanf(" %c %c", &secondRow, &secondCol);
    } while (!checkPlayerInput(&myDeck, currentPlayer, secondRow, secondCol));
    
    printf("\n");


    //Step 4: print the 2 cards the player picks
    
    //getting the index for the two chosen cards.
    unsigned int index1 = (firstCol - 'a') + (firstRow - '0')*13;
    unsigned int index2 = (secondCol - 'a') + (secondRow - '0')*13;
    
    //prints the value of the first card.
    printf("First card picked: %c", myDeck.cards[index1].value);
    //prints the suit of the first card.
    if (myDeck.cards[index1].suit == Spades) {
      printf("\u2660\n"); //prints the spades symbol
    } else if (myDeck.cards[index1].suit == Hearts) {
      printf("\u2661\n"); //prints the hearts symbol
    } else if (myDeck.cards[index1].suit == Diamonds) {
      printf("\u2662\n"); //prints the diamonds symbol
    } else if (myDeck.cards[index1].suit == Clubs) {
      printf("\u2663\n"); //prints the clubs symbol
    }
    
    //prints the value of the second card.
    printf("Second card picked: %c", myDeck.cards[index2].value);
    //prints the suit of the second card.
    if (myDeck.cards[index2].suit == Spades) {
      printf("\u2660\n"); //prints the spades symbol
    } else if (myDeck.cards[index2].suit == Hearts) {
      printf("\u2661\n"); //prints the hearts symbol
    } else if (myDeck.cards[index2].suit == Diamonds) {
      printf("\u2662\n"); //prints the diamonds symbol
    } else if (myDeck.cards[index2].suit == Clubs) {
      printf("\u2663\n"); //prints the clubs symbol
    }
    
    
    //Step 5: call the checkForMatch function to see if the player has picked
    // a matching pair. If so, print the corresponding message and add the cards
    // to the player's winning pile (Player.winPile).
    // Keep the current player as a match leads to an extra round.
    // Otherwise, print the corresponding message and switch player.
    if(checkForMatch(&myDeck, currentPlayer, firstRow, firstCol, secondRow, secondCol)){
      printf("%s has found a match! Earns an extra turn.\n", currentPlayer->name);
      
      //Adding both selected cards to the player's winPile.
      addCardToPlayer(currentPlayer, &myDeck.cards[index1]);
      addCardToPlayer(currentPlayer, &myDeck.cards[index2]);
    } else {
      printf("%s has not found a match.\n", currentPlayer->name);
      
      //Switching the current player.
      if(currentPlayer == &player1){
        currentPlayer = &player2;
      } else {
        currentPlayer = &player1;
      }
    }
    
    
  } while (!checkForWinner(&myDeck));
  
  printf("\n");

  
  //Step 6: find out who won the game and announce the winner
  
  //Stating the amount of cards won by each player.
  printf("%s has won %d cards.\n", player1.name, player1.cardsWon); 
  printf("%s has won %d cards.\n", player2.name, player2.cardsWon); 
  
  //Announcing the player that has more cards.
  if(player1.cardsWon > player2.cardsWon){
    printf("%s has won!\n", player1.name);
  } else if (player1.cardsWon == player2.cardsWon){
    printf("Tie game!\n");
  } else {
    printf("%s has won!\n", player2.name);
  }


  //Step 7: clean up player's winning piles
  clearPlayer(&player1);
  clearPlayer(&player2);


  return 0;
}
