#!/usr/bin/python
# -*- coding: utf-8 -*-

import card
import unittest

class TestCard(unittest.TestCase):

  def setUp(self):

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

    self.twoOfClubs = card.Card(2, card.CLUBS)
    self.sevenOfClubs = card.Card(7, card.CLUBS)
    self.sevenOfHearts = card.Card(7, card.HEARTS)
    self.nineOfHearts = card.Card(9, card.HEARTS)

    self.twoOfClubs = card.Card(2, card.CLUBS)

    self.hands = {}

    # straight flush
    # four of a kind
    # full house
    # flush
    # straight
    # three of a kind
    # two pair
    # one pair
    # high card

    self.hands['straightflush'] = card.Hand([card.Card(11, card.CLUBS), card.Card(9, card.CLUBS), card.Card(10, card.CLUBS), card.Card(8, card.CLUBS), card.Card(7, card.CLUBS)])
    self.hands['twoPairs'] = card.Hand([self.twoOfHearts, self.twoOfClubs, self.sevenOfHearts, self.sevenOfClubs, self.queenOfHearts])
    self.hands['highStraight'] = card.Hand([self.kingOfDiamonds, self.aceOfSpades, self.jackOfClubs, self.queenOfHearts, self.tenOfClubs])
    self.hands['lowStraight'] = card.Hand([self.twoOfHearts, self.threeOfHearts, self.fourOfHearts, self.fiveOfHearts, self.aceOfSpades])
    self.hands['four'] = card.Hand([self.aceOfSpades, self.aceOfClubs, self.aceOfDiamonds, self.jackOfClubs, self.aceOfHearts])
    self.hands['fullHouse'] = card.Hand([self.aceOfSpades, self.aceOfClubs, self.aceOfDiamonds, self.twoOfHearts, self.twoOfClubs])
    self.hands['three'] = card.Hand([self.aceOfSpades, self.fiveOfHearts, self.aceOfDiamonds, self.twoOfHearts, self.aceOfHearts])
    self.hands['flush'] = card.Hand([self.twoOfHearts, self.threeOfHearts, self.sevenOfHearts, self.nineOfHearts, self.queenOfHearts])
    self.hands['noflush'] = card.Hand([self.jackOfClubs, self.threeOfHearts, self.sevenOfHearts, self.nineOfHearts, self.queenOfHearts])
    self.hands['twoPairs'] = card.Hand([self.twoOfHearts, self.twoOfClubs, self.sevenOfHearts, self.sevenOfClubs, self.queenOfHearts])
    self.hands['pair'] = card.Hand([self.twoOfHearts, self.twoOfClubs, self.sevenOfHearts, self.nineOfHearts, self.queenOfHearts])
    self.hands['high'] = card.Hand([self.twoOfClubs, self.kingOfDiamonds, self.fiveOfHearts, self.sevenOfHearts, self.queenOfHearts])

  def tearDown(self):
    self.hands = None

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

  def testStr(self):
    
    hand = card.Hand([card.Card(11, card.CLUBS), card.Card(10, card.CLUBS), card.Card(9, card.CLUBS), card.Card(8, card.CLUBS), card.Card(7, card.CLUBS)])
    self.assertEquals(str(hand), '7♣,8♣,9♣,10♣,J♣')

  def testCardCmp(self):

    self.assertGreater(self.aceOfSpades, self.kingOfDiamonds)
    self.assertGreater(self.kingOfDiamonds, self.queenOfHearts)
    self.assertGreater(self.queenOfHearts, self.jackOfClubs)
    self.assertGreater(self.jackOfClubs, self.twoOfHearts)
    self.assertEqual(self.aceOfSpades, self.aceOfHearts)
    self.assertEqual(self.aceOfSpades, card.ACE)

  def testHandCmp(self):

    h = self.hands

    self.assertTrue(h['straightflush'] > h['highStraight'])
    self.assertTrue(h['highStraight'] > h['lowStraight'])
    self.assertFalse(h['lowStraight'] > h['highStraight'])

    self.assertTrue(h['twoPairs'] > h['fullHouse'])
    self.assertTrue(h['twoPairs'] > h['high'])

    self.assertTrue(h['twoPairs'] > h['pair'])
    self.assertFalse(h['twoPairs'] < h['pair'])

  def testStraightFlush(self):
    self.assertEqual(self.hands['straightflush'].hasStraightFlush(), 11)
    pass

  def testFourOfAKind(self):
    self.assertEqual(self.hands['four'].hasFourOfAKind(), [card.ACE, card.JACK])
    self.assertFalse(self.hands['fullHouse'].hasFourOfAKind())

  def testThreeOfAKind(self):

    self.assertEqual(self.hands['three'].hasThreeOfAKind(), [card.ACE, 5, 2])
    self.assertFalse(self.hands['four'].hasThreeOfAKind())

  def testStraight(self):
    """
    
    """
    self.assertEqual(self.hands['highStraight'].hasStraight(), 14)
    self.assertEqual(self.hands['lowStraight'].hasStraight(), 5)

  def testFullHouse(self):

    self.assertEqual(self.hands['fullHouse'].hasFullhouse(), [14, 2])


  def testFlush(self):


    self.assertEqual(self.hands['flush'].hasFlush(), [12,9,7,3,2])
    self.assertFalse(self.hands['noflush'].hasFlush())

  def testThreeOfAKind(self):

    self.assertEqual(self.hands['three'].hasThreeOfAKind(), [card.ACE, 5, 2])
    self.assertFalse(self.hands['twoPairs'].hasThreeOfAKind())

  def testTwoPairs(self):


    self.assertEqual(self.hands['twoPairs'].hasTwoPairs(), [7, 2, card.QUEEN])

  def testPair(self):

    self.assertEqual(self.hands['pair'].hasPair(), [2, card.QUEEN, 9, 7])
    self.assertFalse(self.hands['twoPairs'].hasPair())
    self.assertFalse(self.hands['three'].hasPair())

  def testHighCard(self):

    self.assertEqual(self.hands['high'].highCard(), [card.KING, card.QUEEN, 7, 5, 2])

    

if __name__ == '__main__':
  unittest.main()