from card import Card
import random
from deck import StandardDeck
from player import Player
from game import Game
from rules import find_winners, score_all
from agents import PlayerAgent, DealerAgent
from agents import *
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

    new_game.round_ended = True
    new_game.end_round()


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

    deck = StandardDeck()
    deck.shuffle()
    print(deck)
    print(len(deck))
    player1 = Player("Ivan")
    player2 = Player("Marko")
    player3 = Player("Luka")
    player4 = Player("Matej")
    player5 = Player("Ivana")
    players = [player1, player2, player3, player4]
    entrysc = 100
    entrysb = 10
    entrybb = 20
    chip_entry_list = [entrysc, entrysb, entrybb]
    new_game = Game(deck, players, chip_entry_list)
    new_game.establish_player_attributes()
    new_game.print_round_info()
    new_game.act_one()
    xmpp = ["test090498@jabber.hot-chilli.net", "test090498"]
    xmpp1 = ["test0904@jabber.hot-chilli.net", "test0904"]
    xmpp2 = ["test0409@jabber.hot-chilli.net", "test0409"]
    xmpp3 = ["test040998@jabber.hot-chilli.net", "test040998"]
    # a = TestAgent("test090498@jabber.hot-chilli.net", "test090498", player=player1)
    agent1 = PlayerAgent(xmpp1[0], xmpp1[1],
                         player=new_game.first_actor, newgame=new_game)
    future1 = agent1.start()
    future1.wait()
    agent2 = PlayerAgent(xmpp2[0], xmpp2[1],
                         player=new_game.small_blind, newgame=new_game)
    future2 = agent2.start()
    future2.wait()
    agent3 = PlayerAgent(xmpp3[0], xmpp3[1],
                         player=new_game.big_blind, newgame=new_game)
    future3 = agent3.start()
    future3.wait()
    dealer = DealerAgent(
        xmpp[0], xmpp[1], player=new_game.dealer, newgame=new_game)
    dealer.start()

    # future = a.start()
    # future.result()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping agent...")

    dealer.stop()
    agent1.stop()
    agent2.stop()
    agent3.stop()
    spade.quit_spade()
