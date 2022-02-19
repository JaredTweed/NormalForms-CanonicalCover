/*
CMPT 125 Assignment 4 Game
Author: Jared Matthew Tweed
Student ID: 301439536, jmt25
SFU email: jared_tweed@sfu.ca
Academic honesty statement: I hereby confirm that this is my own work and I have
not violated any of SFU’s Code of Academic Integrity and Good Conduct (S10.01).
Description: These files implement a linked list structure where each node 
stores the address of a card from the Deck.
*/

#include"card_LList.h"

Card_LList* createCard_LList(){
  
  //Create the list
  Card_LList* myLst = malloc(sizeof(Card_LList));
  if(myLst == NULL){
    exit(0);
  }
  
  //This sets the head and tail to NULL
  myLst->head = NULL;
  myLst->tail = NULL;
  
  return myLst;
}

void clearCard_LList(Card_LList* theList){
  
  Card_Node* tmp;
  
  //This frees each node that is under the alias of tmp (i.e., every node).
  while(theList->head != NULL){
    tmp = theList->head;
    theList->head = theList->head->next;
    free(tmp);
    tmp = NULL;
  }
}

/*This checks if the list is empty by checking 
whether the head and tail are null.*/
bool isEmptyCard_LList(Card_LList* theList){
  if(theList->head == NULL && theList->tail == NULL){
    return true;
  } else {
    return false;
  }
}

void insertFrontCard_LList(Card_LList* theList, Card* theCard){
  //Create Node
  Card_Node* newNode = malloc( sizeof(Card_Node) );
  if(newNode == NULL){
    exit(0);
  }
  newNode->card = theCard; 
  
  //Set the new node to the tail if it is an empty list.
  if( theList->tail == NULL ){
    theList->tail = newNode;
  }
  
  //Set the previous first node to come after our new Node.
  if( theList->head != NULL ){
    newNode->next = theList->head;
  }
  
  //Make the new node be the head.
  theList->head = newNode;
}

void insertEndCard_LList(Card_LList* theList, Card* theCard){
  //Create Node (and return if malloc fails)
  Card_Node* newNode = malloc( sizeof(Card_Node) );
  if(newNode == NULL){
    exit(0);
  }
  
  //Assign the new node's variables.
  newNode->card = theCard; 
  newNode->next = NULL; 
  
  //Set the new node to the head if it is an empty list.
  if( theList->head == NULL ){ 
    theList->head = newNode;
  } 
  
  //sets the newNode after the tail if the tail exists (and list isn't empty).
  if( theList->tail != NULL ) {
    theList->tail->next = newNode;
  }
  
  //makes newnode to be the new tail.
  theList->tail = newNode;
}

Card* removeFrontCard_LList(Card_LList* theList){
  /*this moves the head to be the second item in the list and creates an alias
  by which the previous head can be deleted*/
  Card_Node* tmp = theList->head;
  theList->head = theList->head->next;
  
  //this deletes the previous head's connection to the rest of the list.
  tmp->next = NULL;
  
  /*This assigns the cards suit and values to a variable (which will be 
  returned) so that tmp can be freed*/
  Card* tmpCard = tmp->card;
  free(tmp);
  tmp = NULL;
  
  //This returns the previous head.
  return tmpCard;
}

Card* removeEndCard_LList(Card_LList* theList){
  //this finds the new tail node.
  Card_Node* newTail = theList->head;
  while(newTail->next != theList->tail){
    newTail = newTail->next;
  }
  
  //this disconnects the previous tail from the list.
  newTail->next = NULL;
  
  //Collects removed data.
  Card* returnedData = theList->tail->card;
  
  //Frees the old tail
  free(theList->tail);
  
  //Sets the new tail node to be the new tail.
  theList->tail = newTail;
  
  //this returns the removed tail.
  return returnedData;
}

