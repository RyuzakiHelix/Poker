from card import Card
import random
from deck import StandardDeck
from player import Player
from game import Game


def main():

    deck = StandardDeck()
    deck.shuffle()
    print(deck)
    # for card in deck:
    # print(card)
    print(len(deck))
    player1 = Player("Ivan")
    player2 = Player("Marko")
    player3 = Player("Luka")
    player4 = Player("Matej")
    player5 = Player("Ivana")
    players = [player1, player2, player3, player4]

   # deck.deal(player1)
   # print(player1.cards)
    Player.establish_player_attributes(players)
    for player in players:
        print(
            f"Player {player.name} has the attributes: {player.list_of_special_attributes}")

    entrysc = 100
    entrysb = 10
    entrybb = 20
    chip_entry_list = [entrysc, entrysb, entrybb]
    new_game = Game(deck, players, chip_entry_list)
    new_game.deal_hole()
    new_game.deal_flop()
    new_game.deal_turn()
    new_game.deal_river()
    new_game.print_round_info()
    new_game.score_all()


"""
    for player in players:
        player.list_of_special_attributes.clear()
    players = [player1, player2, player3]
    Player.establish_player_attributes(players)
    for player in players:
        print(
            f"Player {player.name} has the attributes: {player.list_of_special_attributes}")
"""

if __name__ == "__main__":
    main()
