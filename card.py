#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

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

    @param other (Card)
    """
    return self.rank == other.rank and self.suit == other.suit

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

  def hasFlush(self):
    """
    @return 
    """
    last = None
    for i in self.cards:
      if not last:
        last = i
      elif i.suit != last.suit:
        return False

    return self.cards[-1].rank

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

    # have an ace
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

  def __bucket(self):
    bucket = {}

    for i in self.cards:
      r = str(i.rank)
      if r in bucket:
        bucket[r] += 1
      else:
        bucket[r] = 1

    return bucket

  def hasFullhouse(self):
    """
    @return 
    """
    return False

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
    b = self.__bucket()
#    keys = b.keys()
    if len(b) != 3:
      return False
    pass

  def hasPair(self):
    """
    @return 
    """

    b = self.__bucket()
    if len(b) != 4:
      return False 

    return True

  def hasHighCard(self):
    """
    
    """
    return self.cards[-1]

  def __cmp__(self, other):
    """
    
    """
    return 1
