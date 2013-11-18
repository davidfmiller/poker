#!/usr/bin/python
# -*- coding: utf-8 -*-

import card
import unittest

class TestCard(unittest.TestCase):

  def setUp(self):

#     self.deck = {}
#     for suit in card.SUITS:
#       self.deck[suit] = []
#       for rank in range(2,card.ACE + 1):
#         self.deck[suit] = card.Card(rank, suit)

    self.aceOfSpades = card.Card(card.ACE, card.SPADES)
    self.kingOfDiamonds = card.Card(card.KING, card.DIAMONDS)
    self.queenOfHearts = card.Card(card.QUEEN, card.HEARTS)
    self.jackOfClubs = card.Card(card.JACK, card.CLUBS)
    self.tenOfClubs = card.Card(10, card.CLUBS)

    self.aceOfClubs = card.Card(card.ACE, card.CLUBS)
    self.aceOfHearts = card.Card(card.ACE, card.HEARTS)
    self.aceOfDiamonds = card.Card(card.ACE, card.DIAMONDS)

    self.twoOfHearts = card.Card(2, card.HEARTS)
    self.threeOfHearts = card.Card(3, card.HEARTS)
    self.fourOfHearts = card.Card(4, card.HEARTS)
    self.fiveOfHearts = card.Card(5, card.HEARTS)

    self.sevenOfHearts = card.Card(7, card.HEARTS)
    self.nineOfHearts = card.Card(9, card.HEARTS)

    self.twoOfClubs = card.Card(2, card.CLUBS)

  def tearDown(self):
    pass

#  def testSetup(self):    
#    self.assertEqual(len(self.deck), 4)

  def testEq(self):

    self.assertEqual(self.aceOfSpades, 14)
    self.assertEqual(str(self.aceOfSpades), 'A' + card.SPADES)
    self.assertEqual(self.aceOfSpades, card.Card('a', card.SPADES))
    self.assertEqual(self.aceOfSpades, card.Card(14, card.SPADES))
    self.assertEqual(self.aceOfSpades, card.Card(1, card.SPADES))

    self.assertEqual(str(self.kingOfDiamonds), 'K' + card.DIAMONDS)
    self.assertEqual(self.kingOfDiamonds, card.Card('k', card.DIAMONDS))
    self.assertEqual(self.kingOfDiamonds, card.Card(13, card.DIAMONDS))

    self.assertEqual(str(self.queenOfHearts), 'Q' + card.HEARTS)
    self.assertEqual(self.queenOfHearts, card.Card('q', card.HEARTS))
    self.assertEqual(self.queenOfHearts, card.Card(12, card.HEARTS))

    self.assertEqual(str(self.jackOfClubs), 'J' + card.CLUBS)
    self.assertEqual(self.jackOfClubs, card.Card('j', card.CLUBS))
    self.assertEqual(self.jackOfClubs, card.Card(11, card.CLUBS))

    self.assertEqual(self.twoOfHearts, 2)
    self.assertEqual(str(self.twoOfHearts), '2' + card.HEARTS)

  def testCmp(self):
    self.assertGreater(self.aceOfSpades, self.kingOfDiamonds)
    self.assertGreater(self.kingOfDiamonds, self.queenOfHearts)
    self.assertGreater(self.queenOfHearts, self.jackOfClubs)
    self.assertGreater(self.jackOfClubs, self.twoOfHearts)

  def testStraight(self):
    """
    
    """
    highStraight = card.Hand([self.kingOfDiamonds, self.aceOfSpades, self.jackOfClubs, self.queenOfHearts, self.tenOfClubs])
    lowStraight = card.Hand([self.twoOfHearts, self.threeOfHearts, self.fourOfHearts, self.fiveOfHearts, self.aceOfSpades])

    self.assertEqual(highStraight.hasStraight(), 14)
    self.assertEqual(lowStraight.hasStraight(), 5)

#    self.assertFalse()

  def testFlush(self):

    flush = card.Hand([self.twoOfHearts, self.threeOfHearts, self.sevenOfHearts, self.nineOfHearts, self.queenOfHearts])
    noflush = card.Hand([self.jackOfClubs, self.threeOfHearts, self.sevenOfHearts, self.nineOfHearts, self.queenOfHearts])

    self.assertEqual(flush.hasFlush(), [12,9,7,3,2])
    self.assertFalse(noflush.hasFlush())

  def testStraightFlush(self):
    straightflush = card.Hand([card.Card(11, card.CLUBS), card.Card(10, card.CLUBS), card.Card(9, card.CLUBS), card.Card(8, card.CLUBS), card.Card(7, card.CLUBS)])
    self.assertEqual(straightflush.hasStraightFlush(), 11)

  def testThreeOfAKind(self):
    three = card.Hand([self.aceOfSpades, self.aceOfDiamonds, self.aceOfHearts, self.fiveOfHearts, self.twoOfHearts])
    self.assertEqual(three.hasThreeOfAKind(), [card.ACE, 5, 2])

  def testPair(self):

    pair = card.Hand([self.twoOfHearts, self.twoOfClubs, self.sevenOfHearts, self.nineOfHearts, self.queenOfHearts])
    self.assertEqual(pair.hasPair(), [2, card.QUEEN, 9, 7])

  def testHighCard(self):

    high = card.Hand([self.twoOfClubs, self.kingOfDiamonds, self.fiveOfHearts, self.sevenOfHearts, self.queenOfHearts])
    self.assertEqual(high.highCard(), [card.KING, card.QUEEN, 7, 5, 2])



    

if __name__ == '__main__':
  unittest.main()