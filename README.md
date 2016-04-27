🃏 poker
=====

One approach to determining relative ranking of poker hands

```
git clone https://github.com/davidfmiller/poker.git
cd poker
python test.py
```

You can create your own hands like so:

```
import card

straightFlush = card.Hand([card.Card(11, card.CLUBS), card.Card(9, card.CLUBS), card.Card(10, card.CLUBS), card.Card(8, card.CLUBS), card.Card(7, card.CLUBS)])
twoPairs = card.Hand([self.twoOfHearts, self.twoOfClubs, self.sevenOfHearts, self.sevenOfClubs, self.queenOfHearts])

if straightFlush > twoPairs:
  print str(straightFlush) + ' > ' + str(twoPairs)
```

The above code will print the following:

```
7♣,8♣,9♣,10♣,J♣ > 2♣,2♥,7♣,7♥,Q♥
```

The command `python card.py ` will produce a single, randomly-selected card, ex: `10♥` or `Q♦`