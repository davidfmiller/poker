#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import operator

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
    @param suit (int) - one of CLUBS, HEARTS, SPADES, DIAMONDS
    """
    if not suit in [CLUBS, HEARTS, SPADES, DIAMONDS]:
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
    return self.rank == other.rank

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

    self.cards = sorted(cards)
#    pass

  def __str__(self):
    """
    
    """
    buf = ''
    for card in self.cards:
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

    # cards in reversed order
    rev = self.cards[::-1]
    return rev

#  def __straight(self, cards):
#    pass

  def hasStraight(self):
    """
    @return the highest rank in the straight if it exists; False if not
    """

    hasAce = self.cards[-1].rank == ACE
    broken = False

    cards = self.cards

    last = None
    for i in cards:
      if not last:
        last = i
      elif (i.rank != last.rank + 1):
        if not hasAce:
          return False
        else:
          broken = True
          break
      else:
        last = i

    if not broken:
      return last.rank

    # have an ace, check to see if we have a low straight
    cards[-1].rank = 1
    mycards = sorted(cards)
    last = None

    for i in mycards:

      if not last:
        last = i
      elif (i.rank != last.rank + 1):
        return False
      else:
        last = i

    return last.rank

  def __tuples(self):
    # return

    bucket = {}

    for i in self.cards:
      r = i.rank
      if r in bucket:
        bucket[r] += 1
      else:
        bucket[r] = 1

    return sorted(bucket.items(), key=operator.itemgetter(1), reverse=True)

  def hasFullhouse(self):
    """
    
    @return (mixed) - a two-item array whose first item is the 3-of-a-kind rank & second item is the pair rank; False if no full house exists
    @see hasThreeOfAKind
    @see hasPair
    """

    t = self.hasThreeOfAKind()
    p = self.hasPair()

    if not t or not p:
      return False

    return [t[0], p[0]]

  def hasFourOfAKind(self):
    """

    @return 
    """
    b = self.__bucket()
    if len(b) != 2:
      return True

    return False

  def hasThreeOfAKind(self):
    """

    @return 
    """
    b = self.__tuples()

    if len(b) != 3:
      return False

    # grab the 3 of a kind rank
    three, nil = b[0]
    b.pop(0)

    # sort the remaining cards
    tuples = sorted(b, key=operator.itemgetter(0), reverse=True)
    high, nil = tuples[0]
    low, nil = tuples[1]

    return [three, high, low]

  def hasPair(self):
    """
    @return 
    """

    b = self.__tuples()
    if len(b) != 4:
      return False

    pair, nil = b[0]
    b.pop(0)

    tuples = sorted(b, key=operator.itemgetter(0), reverse=True)
    high, nil = tuples[0]
    med, nil = tuples[1]
    low, nil = tuples[2]

    return [pair, high, med, low]

  def highCard(self):
    """
    
    """
    rev = self.cards[::-1]
    return rev

  def __cmp__(self, other):
    """
    
    """
    return 1
