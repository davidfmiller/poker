#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import operator
import copy

ACE = 14
KING = 13
QUEEN = 12
JACK = 11

CLUBS = '♣'
HEARTS = '♥'
SPADES = '♠'
DIAMONDS = '♦'

SUITS = [CLUBS, HEARTS, SPADES, DIAMONDS]

# http://en.wikipedia.org/wiki/List_of_poker_hands


# straight flush
# four of a kind
# full house
# flush
# straight
# three of a kind
# two pair
# one pair
# high card

class Card:
  """
  
  """

  def __init__(self, rank, suit):
    """

    @param rank (int) - 
    @param suit (string) - one of card.CLUBS ('♣'), card.HEARTS ('♥'), card.SPADES ('♠'), card.DIAMONDS ('♦')
    """
    if not suit in SUITS:
      raise Exception, str(suit) + ' is an invalid suit'

    # handle chars for card ranks
    if not isinstance(rank, int):
      rank = rank.upper()
      rank = {'A' : 14, 'K' : 13, 'Q' : 12, 'J' : 11 }.get(rank)

    # force ace to be high for now
    if rank == 1:
      rank = 14

    # enforce valid rank
    range(2,14 + 1).index(rank)

    self.rank = rank
    self.suit = suit


  def __eq__(self, other):
    """

    @param other (Card,int)
    """
    return isinstance(other, int) and self.rank == other or self.rank == other.rank 


  def __cmp__(self, other):
    """
    
    @param other (Card)
    """
    if isinstance(other, int):
      return self.rank - other
    else:
      return self.rank - other.rank


  def __str__(self):
    """
    
    @return string
    """
  
    r = self.rank
    if (r > 10):
      r = {
        '14' : 'A',
        '13' : 'K',
        '12' : 'Q',
        '11' : 'J',
        '1' : 'A',
      }.get(str(r))

    return str(r) + self.suit


  def __cmp__(self, other):
    """
    
    @param other
    """
    return cmp(self.rank, other.rank)



class Hand:
  """
  
  """
  def __init__(self, cards):
    """
    
    """
    if len(cards) != 5:
      raise Exception, 'Hand ' + str(cards) + ' is missing a card or two'

    self.cards = sorted(cards, reverse=True)


  def __str__(self):
    """
    @return (string) - ex: A string representation of the hand, ex: 
    """
    buf = ''
    
    rev = self.cards[::-1]

    for card in rev:
      buf += (buf and ',' or '') + str(card)

    return buf


  def hasStraightFlush(self):
    """
    @return (mixed) - the list of cards in descending order if a straight flush; False if no straight flush exists

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
    for i in self.cards:
      if not last:
        last = i
      elif i.suit != last.suit:
        return False

    return self.cards


  def __sequence(self, hand=None):
    """
    Determine if a hand's cards are in decreasing sequential order
    
    @param (hand, optional) - the hand of cards to check 
    @return (mixed) - False if the hand does not have a straight (
    """

    if not hand:
      hand = self.cards

    last = None
    for i in hand:
      if not last:
        last = i
      elif (i.rank != last.rank - 1):
        return False
      else:
        last = i

    return hand[0]


  def __cmpList(self, a, b):
    """
      Find which list is greater than another
    """
    i = 0
    while i < len(a):
      if a[i] != b[i]:
        return a[i] - b[i]
      i += 1

    return 0 # they're equal


  def __tuples(self):

    bucket = {}

    for i in self.cards:
      r = i.rank
      if r in bucket:
        bucket[r] += 1
      else:
        bucket[r] = 1

    return sorted(bucket.items(), key=operator.itemgetter(1), reverse=True)


  def hasStraight(self):
    """
    @return the highest rank in the straight if it exists; False if not
    """

    if self.__sequence():
      return self.cards[0].rank

    # if there's no ace then there's no chance for a low straight
    if self.cards[0].rank != ACE:
      return False

    # have an ace, check to see if we have a low straight
    cards = copy.copy(self.cards)
    cards[0].rank = 1
    mycards = sorted(cards, reverse=True)
    last = None
    return self.__sequence(mycards)


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

    @return 
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

    @return (mixed) an array containing the rank of the high pair, low pair, and remaining card (in descending order); or False if two pairs don't exist
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
    @return 
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
    
    """
    return self.cards


  def __cmp__(self, other):
    """
    @return int (self - other)
    """

    mf = mine.hasFlush()
    of = other.hasFlush()

    ms = mine.hasStraight()
    os = other.hasStraight()

    mt = self.__tuples()
    ot = other.__tuples()

    # straight flush
    if mf and sf:
      if os and of: # if they also have one, choose high card
        return self.cards[0].rank - other.cards[0].rank
      else:
        return 1
    elif os and of: # if they have straight flush we lose
        return -1

    # four of a kind
    if len(mt) == 2:
      if len(ot) > 2: # they don't have four of a kind
        return 1 
      else:
        return mt[1][0] - ot[1][0] # determine higher four of a kind
    elif len(ot) == 2: # if they have four of a kind we lose
      return -1

    # full house
    elif len(mt) == 2 and mt[0][1] == 3:
      if len(ot) > 3:
        return 1
      else:  
        return self.__cmpList(mt, ot)
    elif len(ot) == 2 and ot[0][1] == 3:
      return -1

    # flush
    if mf:
      if not of:
        return 1
      else:
        return self.__cmpList(mf, of)
    elif of:
      return -1

    # straight
    if ms:
      if not os:
        return 1
      else:
        return ms - os
    elif os:
      return -1

    if len(mt) == 3: # three of a kind or two pairs

      if len(ot) > 3:
        return 1

      if mt[0][1] == 3: # three of a kind     
        if ot[0][1] != 3:
          return 1
        else:
          return self.__cmpList(self.cards, other.cards)
      elif len(ot) == 3 and ot[0][1] == 3:
        return -1

      if mt[0][1] == 2: # two pairs
        if len(ot) != 3 or ot[0][1] != 2:
          return 1
        else:
          return self.__cmpList(self.cards, other.cards)
      elif len(ot) == 3 and ot[0][0] == 2 and ot[0][1] == 2:
        return -1

    elif len(ot) <= 3:
      return -1

    # single pair
    if len(mt) == 4:
      if len(ot) != 4:
        return 1
      else:
        return self.__cmpList(self.cards, other.cards)
    elif len(ot) <= 4: # they have a pair, we lose
      return -1

    # high card
    return self.__cmpList(self.cards, other.cards)
