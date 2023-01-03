from card import Card
import random
from deck import StandardDeck


def main():

    deck = StandardDeck()
    deck.shuffle()
    # for card in deck:
    # print(card)
    print(len(deck))
    deck.deal()


if __name__ == "__main__":
    main()
