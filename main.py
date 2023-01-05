from card import Card
import random
from deck import StandardDeck
from player import Player
from game import Game
from rules import find_winners, score_all
from agents import AgentPlayerOne, PrviAgent, TestAgent
import agents
import spade
import time


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

    a = AgentPlayerOne("posiljatelj@rec.foi.hr", "tajna")
    a.start()

   # deck.deal(player1)
   # print(player1.cards)
    # Player.establish_player_attributes(players)
   # for player in players:
    #    print(
    #        f"Player {player.name} has the attributes: {player.list_of_special_attributes}")

    entrysc = 100
    entrysb = 10
    entrybb = 20
    chip_entry_list = [entrysc, entrysb, entrybb]
    new_game = Game(deck, players, chip_entry_list)
    new_game.establish_player_attributes()
    new_game.deal_hole()
    # new_game.deal_flop()
    # new_game.deal_turn()
    # new_game.deal_river()
    new_game.print_round_info()
    # new_game.score_all()
    # new_game.find_winners()
    # score_all(new_game)
    # find_winners(new_game)
    # new_game.end_round()
    new_game.act_one()
    new_game.print_round_info()
    if not new_game.round_ended:
        new_game.deal_flop()
        new_game.print_round_info()
    if not new_game.round_ended:
        new_game.ask_players()
        new_game.print_round_info()
    if not new_game.round_ended:
        new_game.deal_turn()
        new_game.print_round_info()
    if not new_game.round_ended:
        new_game.ask_players()
        new_game.print_round_info()
    if not new_game.round_ended:
        new_game.deal_river()
        new_game.print_round_info()
    if not new_game.round_ended:
        new_game.ask_players()
        new_game.print_round_info()
    if not new_game.round_ended:
        # new_game.score_all()
        score_all(new_game)
        new_game.print_round_info()
    # new_game.find_winners()
    find_winners(new_game)


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
    # main()
    # a = AgentPlayerOne("test090498@01337.io", "test090498")
    # a = AgentPlayerOne("test0904@shad0w.io", "test0904")
    # a = AgentPlayerOne("test090498@jabber.hot-chilli.net", "test090498")
    # a = PrviAgent("test090498@jabber.hot-chilli.net", "test090498")
    a = TestAgent("test090498@jabber.hot-chilli.net", "test090498")
    a.start()
    # future = a.start()
    # future.result()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nZaustavljam agenta...")

    a.stop()
    spade.quit_spade()
