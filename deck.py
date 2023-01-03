from card import Card
import random


class StandardDeck(list):
    def __init__(self):
        super().__init__()
        suits = list(range(4))
        values = list(range(13))
       # [[self.append(Card(value, suit)) for suit in suits] for value in values]
        for value in values:
            for suit in suits:
                self.append(Card(value, suit))

    def shuffle(self):
        random.shuffle(self)
        print("\n\n--deck shuffled--")

    def deal(self, player, times=1):
        for i in range(times):
            player.cards.append(self.pop(0))
           # print(self.pop(0))

    def burn(self):
        self.pop(0)
