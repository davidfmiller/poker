#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""


import sys
import operator
import copy
import random

ACE = 14
KING = 13
QUEEN = 12
JACK = 11

CLUBS = '♣'
HEARTS = '♥'
SPADES = '♠'
DIAMONDS = '♦'

SUITS = [CLUBS, HEARTS, SPADES, DIAMONDS]
RANKS = [1,2,3,4,5,6,7,8,9,10,JACK, QUEEN, KING, ACE]

class Card:
  """
  Represents a single playing card, storing its rank and suit
  """

  def __init__(self, rank, suit):
    """
    Create a new card

    @param rank (int) - A integer between 1 and 14 (inclusive), where an Ace is `1` or `14`, a Jack `11`, a Queen `12`, and a King `13`
    @param suit (string) - one of card.CLUBS ('♣'), card.HEARTS ('♥'), card.SPADES ('♠'), card.DIAMONDS ('♦')
    """
    if not suit in SUITS:
      raise Exception, str(suit) + ' is an invalid suit'

    # handle chars for card ranks
    if not isinstance(rank, int):
      rank = rank.upper()
      rank = {'A' : ACE, 'K' : KING, 'Q' : QUEEN, 'J' : JACK }.get(rank)

    # force ace to be high for now
    if rank == 1:
      rank = ACE

    # enforce valid rank
    range(2,ACE + 1).index(rank)

    self.__rank = rank
    self.__suit = suit


  def highlow(self):
    """
    Toggle high/low value if this card is an ace
    """
    if self.__rank == ACE:
      self.__rank = 1
    elif self.__rank == 1:
      self.__rank = ACE


  def rank(self):
    """
    @return int
    """
    return self.__rank


  def suit(self):
    """
    @return string    
    """
    return self.__suit


  def __eq__(self, other):
    """
    Determine is two cards are of the same rank
    @param other (Card,int)
    """
    return isinstance(other, int) and self.rank() == other or self.rank() == other.rank()


  def __cmp__(self, other):
    """
    Determine which card has a higher rank

    @param other (Card,int)
    @return int
    """
    if isinstance(other, int):
      return self.rank() - other
    else:
      return self.rank() - other.rank()


  def __str__(self):
    """
    Retrieve a string representation of the card, ex: 'A♣', '2♥'

    @return string
    """
  
    r = self.rank()
    if (r > 10):
      r = {
        str(ACE)   : 'A',
        str(KING)  : 'K',
        str(QUEEN) : 'Q',
        str(JACK)  : 'J'
      }.get(str(r))

    return str(r) + self.suit()


  def __sub__(self, other):
    """
    Subtract one card from another, used to determine their relative rank

    @param other (int, Card)
    @return int
    """
    if isinstance(other, int):
      return self.rank() - other

    return self.rank() - other.rank()

class Deck:
  """
  Object that stores a deck of (52) playing cards
  """

  def __init__(self):
    """
    Create a new deck of (52) sequential cards
    """

    self.__cards = []

    for suit in SUITS:
      for rank in RANKS:
        self.__cards.append(Card(rank, suit))

  def shuffle(self):
    """
    Shuffle the cards' positions within the deck
    """
    random.shuffle(self.__cards)

  def deal(self):
    """
    Pop a Card off the top of the deck and return it

    @return Card, or None if the deck is empty
    """
    return len(self.__cards) > 0 and self.__cards.pop() or None

  def __str__(self):
    """
    Retrieve a string representation of the deck

    @return string
    """
    buf = ''
    for i in self.__cards:
      buf += str(i) + " "
    return buf.strip()


class Hand:
  """
  Represents a poker hand (of 5 cards)
  """
  def __init__(self, cards):
    """
    
    @param cards - a list of 5 cards   
    """
    if len(cards) != 5:
      raise Exception, 'Hand ' + str(cards) + ' doesn\'t contain 5 cards'

    self.__cards = sorted(cards, reverse=True)

  def __str__(self):
    """
    Retrieve a string representation of this Hand 

    @return (string) - ex: '7♣,8♣,9♥,10♣,J♦'
    """
    buf = ''

    rev = self.__cards[::-1]

    for card in rev:
      buf += (buf and ',' or '') + str(card)

    return buf


  def __sequence(self, hand=None):
    """
    Determine if a hand's cards are in decreasing sequential order (ie : a straight), ignoring the ace's high/low 

    @param (hand, optional) - the hand of cards to check 
    @return (mixed) - False if the hand does not have a straight (
    """

    if not hand:
      hand = self.__cards

    hand = copy.deepcopy(hand)

    last = None
    for i in hand:
      if not last:
        last = i
      elif (i.rank() != last.rank() - 1):
        return False
      else:
        last = i

    return hand[0]


  def __cmpList(self, a, b):
    """
      Find which list is greater than another

      @return int
      @param a (list)
      @param b (list)
      @see __cmp__
    """
    i = 0
    while i < len(a):
      if a[i] != b[i]:
        return a[i] - b[i]
      i += 1

    return 0 # they're equal


  def __tuples(self):
    """
    Return a list of tuples containing the card ranks and their frequency within the hand

    ex: 2♥,A♠,5♥,A♥,A♦ → [(14, 3), (2, 1), (5, 1)] 
    """
    bucket = {}

    for i in self.__cards:
      r = i.rank()
      if r in bucket:
        bucket[r] += 1
      else:
        bucket[r] = 1

    return sorted(bucket.items(), key=operator.itemgetter(1), reverse=True)


  def hasStraightFlush(self):
    """
    @return (mixed) - the highest rank of the card in the straight flush if the hand exists; False if no straight flush exists

    @see hashFlush
    @see hasStraight
    """
    f = self.hasFlush()
    if not f:
      return False

    return self.hasStraight()


  def hasFlush(self):
    """
    
    @return (mixed) - the list of cards in descending order if a flush; False if no flush exists
    """
    last = None
    for i in self.__cards:
      if not last:
        last = i
      elif i.suit() != last.suit():
        return False

    return copy.deepcopy(self.__cards)


  def hasStraight(self):
    """
    
    @return the highest rank in the straight if it exists; False if not
    """

    if self.__sequence():
      return self.__cards[0].rank()

    # if there's no ace then there's no chance for a low straight
    if self.__cards[0].rank() != ACE:
      return False

    # have an ace, check to see if we have a low straight
    cards = copy.deepcopy(self.__cards)
    cards[0].highlow()
    mycards = sorted(cards, reverse=True)
    last = None
    if self.__sequence(mycards):
      return mycards[0].rank()

    return False


  def hasFullhouse(self):
    """
    
    @return (mixed) - a two-item array whose first item is the 3-of-a-kind rank & second item is the pair rank; False if no full house exists
    @see hasThreeOfAKind
    @see hasPair
    """

    b = self.__tuples()
    if len(b) != 2 and b[0][1] != 3:
      return False

    return [b[0][0], b[1][0]]


  def hasFourOfAKind(self):
    """

    @return 
    """
    b = self.__tuples()
    if len(b) != 2:
      return False

    if b[0][1] != 4:
      return False

    return [b[0][0], b[1][0]]


  def hasThreeOfAKind(self):
    """

    @return a three-element array if the hand has a three of a kind; False if not
    """
    b = self.__tuples()

    if len(b) != 3:
      return False

    # ensure we don't have two pairs
    if b[0][1] != 3 or b[1][1] == 2:
      return False

    # grab the 3 of a kind rank
    three = b[0][0]
    b.pop(0)

    # sort the remaining cards
    b = sorted(b, key=operator.itemgetter(0), reverse=True)

    return [three, b[0][0], b[1][0]]


  def hasTwoPairs(self):
    """

    @return (mixed) an array containing the rank of the high pair, rank of the low pair, and remaining card (in descending order); or False if two pairs don't exist
    """
    b = self.__tuples()

    if len(b) != 3:
      return False

    if b[0][1] != 2:
      return False

    p1 = b[0][0]
    p2 = b[1][0]
    high = b[2][0]

    # ensure the two pair ranks are sorted in decreasing order
    l = sorted([p1, p2], reverse=True)
    l.append(high)

    return l


  def hasPair(self):
    """
    @return a four-element array containing the rank of the pair and then the remaining cards' ranks in descending order; or False if a pair
    """

    b = self.__tuples()
    if len(b) != 4:
      return False

    # remove the pair from the list
    pair = b[0][1]
    b.pop(0)

    # sort the remaining cards
    tuples = sorted(b, key=operator.itemgetter(0), reverse=True)
    high = tuples[0][0]
    med = tuples[1][0]
    low = tuples[2][0]

    return [pair, high, med, low]


  def highCard(self):
    """
    Return a list of cards in descending order if no higher hand exists; False otherwise

    @return list of 
    """

    b = self.__tuples()
    if self.hasFlush() or self.hasStraight() or len(b) < 5:
      return False

    return copy.deepcopy(self.__cards)


  def __eq__(self, other):
    """
    Determine if two hands are equal
    
    @return int
    @see __cmp__    
    """

    return self.__cmp__(other) == 0

  def __cmp__(self, other):
    """

    @param other (Card)
    @return int - an integer value indicating which hand is higher-ranking
    @see http://en.wikipedia.org/wiki/List_of_poker_hands
    """

    mf = self.hasFlush()
    of = other.hasFlush()

    ms = self.hasStraight()
    os = other.hasStraight()

    mt = self.__tuples()  # retrieve the distribution of ranks in my hand
    ot = other.__tuples() #                                ... in the other hand

    ml = len(mt) # ml contains the number of unique ranks in my hand
    ol = len(ot) #                                    ... in the other hand

    if mf and ms:      # we have a straight flush
      if os and of:    # if they also have one, winner has the high card
        return ms - os
      else:            # if they don't have one we win
        return 1
    elif os and of:    # if they have straight flush we lose
        return -1

    
    if ml == 2 and mt[0][1] == 4: # we have four of a kind
      if ol > 2 or ot[0][1] < 4:  # they don't have four of a kind we win
        return 1 
      else:              
        return self.__cmpList(mt, ot)    # they have one so we who has the better cards
    elif len(ot) == 2 and ot[0][1] == 4: # if they have four of a kind we lose
      return -1

    
    if ml == 2 and mt[0][1] == 3:     # we have a full house
      if ol > 2:                      # if they don't have one we win
        return 1
      else:  
        return self.__cmpList(mt, ot) # if they do see who has the better cards
    elif ol == 2 and ot[0][1] == 3:   # they have a full house and we don't we lose
      return -1
    
    if mf:         # we have a flush
      if not of:   # if they don't have a flush we win
        return 1
      else:
        return self.__cmpList(mf, of)
    elif of:                           # they have a flush and we don't we lose
      return -1

    
    if ms:              # we have a straight
      if not os:        # if they don't have one we win
        return 1
      else:
        return ms - os  # decide based on highest card
    elif os:
      return -1         # they have a straight so we lose


    if ml == 3: # three of a kind or two pairs

      if ol > 3: # if they have neither then we win
        return 1

      if mt[0][1] == 3:    # three of a kind
        if ot[0][1] != 3:  # if they don't have three of a kind we win
          return 1
        else:
          return self.__cmpList(self.__cards, other.__cards) # determine who has the better triples/remaining
      elif len(ot) == 3 and ot[0][1] == 3:                   # if they have three of a kind & we won't we lose
        return -1

      if mt[0][1] == 2:               # two pairs
        if ol != 3:  # if they don't have 2 pairs we win
          return 1
        else:
          return self.__cmpList(self.__cards, other.__cards) # determine who has the better pairs & orphan
      elif ol == 3 and ot[0][0] == 2 and ot[0][1] == 2:      # if they don't have two pairs we win
        return -1

    elif ol <= 3: # if they have two pairs or three of a kind and we have neither so we lose
      return -1

    
    if ml == 4:   # we have a single pair
      if ol != 4: # if they don't have a pair we win
        return 1
      else:
        return self.__cmpList(self.__cards, other.__cards) # see who has the highest pair & remaining cards
    elif ol <= 4:                                          # they have a pair we don'  so we lose
      return -1


    return self.__cmpList(self.__cards, other.__cards) # it boils down to high cards

if __name__ == '__main__':
    d = Deck()
    d.shuffle()
    print d.deal()