from card import Card


def main():
    class StandardDeck(list):
        def __init__(self):
            super().__init__()
            suits = list(range(4))
            values = list(range(13))
            [[self.append(Card(i, j)) for j in suits] for i in values]

    deck = StandardDeck()
    for card in deck:
        print(card)


if __name__ == "__main__":
    main()
