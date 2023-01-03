from card import Card
import random


class StandardDeck(list):
    def __init__(self):
        super().__init__()
        suits = list(range(4))
        values = list(range(13))
        [[self.append(Card(i, j)) for j in suits] for i in values]

    def shuffle(self):
        random.shuffle(self)
        print("\n\n--deck shuffled--")

    def deal(self, times=1):
        for i in range(times):
            # location.cards.append(self.pop(0))
            print(self.pop(0))
