from deck import StandardDeck
from player import Player
import itertools
from collections import Counter
import time


class Game(object):
    def __init__(self, starting_deck, players, starting_chips):
        self.need_raise_info = False
        self.game_over = False
        self.acting_player = Player()
        self.possible_responses = []
        self.round_counter = 0
        self.cards = []
        self.pot = 0
        self.pot_dict = {}
        self.pot_in_play = 0
        self.list_of_player_names = []
        self.dealer = Player()
        self.small_blind = Player()
        self.big_blind = Player()
        self.first_actor = Player()
        self.winners = []
        self.deck = starting_deck
        self.list_of_scores_from_eligible_winners = []
        # self.setup = ask_app("Start?")
        while True:
            try:
                self.number_of_players = len(players)
                break
            except ValueError:
                print("Invalid response")
        if 1 < self.number_of_players < 11:
            pass
        else:
            print("Invalid number of players")
            # main()
        self.list_of_players = [
            Player(name) for name in players if name != ""]
        while True:
            try:
                self.starting_chips = int(starting_chips[0])
                if self.starting_chips > 0:
                    break
                print("Invalid number, try greater than 0")
            except ValueError:
                print("Invalid response")
                continue
        for player in self.list_of_players:
            player.chips = self.starting_chips
        self.ready_list = []
        while True:
            try:
                self.small_blind_amount = int(starting_chips[1])
                if self.starting_chips > self.small_blind_amount > 0:
                    break
                print(
                    "Invalid number: try bigger than zero, smaller than starting chips")
            except ValueError:
                print("Invalid response")
                continue
        while True:
            try:
                self.big_blind_amount = int(starting_chips[2])
                if self.starting_chips > self.big_blind_amount > self.small_blind_amount:
                    break
                print(
                    "Invalid number: try bigger than small blind, smaller than starting chips")
            except ValueError:
                print("Invalid response")
                continue
        self.winner = None
        self.action_counter = 0
        self.attribute_list = ["d", "sb", "bb", "fa"]
        self.highest_stake = 0
        self.fold_list = []
        self.not_fold_list = []
        self.round_ended = False
        self.fold_out = False
        self.list_of_scores_eligible = []
        self.list_of_players_not_out = list(set(self.list_of_players))
        self.number_of_player_not_out = int(
            len(list(set(self.list_of_players))))

    def print_round_info(self):
        print("\n")
        for player in self.list_of_players:
            print("\n")
            print(f"Name: {player.name}")
            print(f"Cards: {player.cards}")
            print(f"Player score: {player.score}")
            print(f"Chips: {player.chips}")
            print(f"Special Attributes: {player.list_of_special_attributes}")
            if player.fold:
                print(f"Folded")
            if player.all_in:
                print(f"All-in")
            print(f"Stake: {player.stake}")
            print(f"Stake-gap: {player.stake_gap}")
            print("\n")
        print(f"Pot: {self.pot}")
        print(f"Community cards: {self.cards}")
        print("\n")

# It has to be here bcs i could not manage to link players atributes yet, self has to be bcs of subscription to object
    def establish_player_attributes(self):
        address_assignment = 0
        self.dealer = self.list_of_players_not_out[address_assignment]
        self.dealer.list_of_special_attributes.append("dealer")
        address_assignment += 1
        address_assignment %= len(self.list_of_players_not_out)
        self.small_blind = self.list_of_players_not_out[address_assignment]
        self.small_blind.list_of_special_attributes.append("small blind")
        address_assignment += 1
        address_assignment %= len(self.list_of_players_not_out)
        self.big_blind = self.list_of_players_not_out[address_assignment]
        self.big_blind.list_of_special_attributes.append("big blind")
        address_assignment += 1
        address_assignment %= len(self.list_of_players_not_out)
        self.first_actor = self.list_of_players_not_out[address_assignment]
        self.first_actor.list_of_special_attributes.append("first actor")
        self.list_of_players_not_out.append(
            self.list_of_players_not_out.pop(0))

# Deal players their cards
    def deal_hole(self):
        for player in self.list_of_players_not_out:
            self.deck.deal(player, 2)

# Deal on the table 3 cards
    def deal_flop(self):
        self.deck.burn()
        self.deck.deal(self, 3)

# After the flop betting round is closed, the dealer burns another card, then puts the next card face up, directly to the right of the flop
    def deal_turn(self):
        self.deck.burn()
        print("\n--card burned--")
        self.deck.deal(self, 1)
        print(f"\nCommunity Cards: {self.cards}")

# The river is the last of the community cards dealt in a game, both in poker tournaments and cash games
    def deal_river(self):
        self.deck.burn()
        print("\n--card burned--")
        self.deck.deal(self, 1)
        print(f"\n\nCommunity Cards: {self.cards}")

    def clear_board(self):
        self.possible_responses.clear()
        self.cards.clear()
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.pot = 0
        self.pot_dict.clear()
        self.winners.clear()
        self.list_of_scores_from_eligible_winners.clear()
        self.action_counter = 0
        self.highest_stake = 0
        self.fold_list.clear()
        self.not_fold_list.clear()
        self.fold_out = False
        self.list_of_scores_eligible.clear()
        self.round_ended = False
        for player in self.list_of_players:
            player.score.clear()
            player.cards.clear()
            player.stake = 0
            player.stake_gap = 0
            player.ready = False
            player.all_in = False
            player.fold = False
            player.list_of_special_attributes.clear()
            player.win = False

    def end_round(self):
        self.list_of_players_not_out = list(set(self.list_of_players_not_out))
        for player in self.list_of_players_not_out:
            if player.chips <= 0:
                self.list_of_players_not_out.remove(player)
                print(f"{player.name} is out of the game!")
        self.number_of_player_not_out = len(set(self.list_of_players_not_out))
        if self.number_of_player_not_out == 1:
            self.game_over = True
            self.winner = self.list_of_players_not_out[0]
            print(
                f"Game is over: {self.winner} wins with {self.winner.chips}!")
            quit()
        new_round = str(input("Start a new round? (yes/no)"))
        if new_round == "yes":
            print("\n\n\t\t\t\t--ROUND OVER--")
            print("\n\n\t\t\t--STARTING NEW ROUND--\n")
            self.round_counter += 1
            pass
        else:
            quit()
        time.sleep(0.3)
        self.clear_board()

    def answer(self, player):
        player.stake_gap = self.highest_stake - player.stake
        if player.all_in or player.fold or self.fold_out:
            return True
        if player.chips <= 0:
            print(f"{player.name} is all in!")
            player.all_in = True
        print(f"Highest stake: {self.highest_stake}")
        print(
            f"Put in at least {player.stake_gap} to stay in.\nDon't Have that much? You'll have to go all-in!")
        print(f"Chips available: {player.chips}")
        self.possible_responses.clear()
        if player.stake_gap > 0:
            self.possible_responses.append("fold")
            if player.stake_gap == player.chips:
                self.possible_responses.append("all_in_exact")
            if player.stake_gap > player.chips:
                self.possible_responses.append("all_in_partial")
            if player.stake_gap < player.chips:
                self.possible_responses.append("call_exact")
                self.possible_responses.append("call_and_raise")
                self.possible_responses.append("call_and_all_in")
        if player.stake_gap == 0:
            self.possible_responses.append("check")
            self.possible_responses.append("raise")
            self.possible_responses.append("fold")
            self.possible_responses.append("all_in")
        while True:
            print(self.possible_responses)
            # response = str(ask_app(f"{player.name}'s action\n->", self))
            response = str(input(f"{player.name}'s action\n->"))
            # Get agent response here!!!!!!!!!!
            if response not in self.possible_responses:
                print("Invalid response")
                continue
            if response == "all_in_partial":
                player.stake += player.chips
                self.pot += player.chips
                player.stake_gap -= player.chips
                player.chips = 0
                print(f"{player.name} is all-in!")
                player.all_in = True
                return True
            if response == "all_in_exact":
                print(f"{player.name} is all-in!")
                player.all_in = True
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips = 0
                player.stake_gap = 0
                return True
            if response == "fold":
                player.fold = True
                self.fold_list.append(player)
                if len(self.fold_list) == (len(self.list_of_players_not_out) - 1):
                    for player in self.list_of_players_not_out:
                        if player not in self.fold_list:
                            self.fold_out = True
                            print(f"{player} wins!")
                            self.winners.append(player)
                            for player in self.winners:
                                player.win = True
                            self.round_ended = True
                return True
            if response == "call_exact":
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                return True
            if response == "check":
                player.stake_gap = 0
                return True
            if response == "raise":
                self.need_raise_info = True
                while True:
                    bet = int(
                        input(f"How much would {player.name} like to raise? ({player.chips} available)\n->",
                              self))
                    if bet > player.chips or bet <= 0:
                        print("Invalid response")
                        continue
                    if bet == player.chips:
                        print(f"{player.name} is all-in!")
                        player.all_in = True
                    self.need_raise_info = False
                    player.stake += bet
                    self.pot += bet
                    player.chips -= bet
                    self.highest_stake = player.stake
                    self.ready_list.clear()
                    player.stake_gap = 0
                    return True
            if response == "call_and_raise":
                self.need_raise_info = True
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                while True:
                    try:
                        bet = int(
                            input(f"How much would {player.name} like to raise? ({player.chips} available)\n->",
                                  self))
                    except ValueError:
                        continue
                    if bet > player.chips or bet <= 0:
                        print("Invalid response")
                        continue
                    if bet == player.chips:
                        print(f"{player.name} is all-in!")
                        player.all_in = True
                    self.need_raise_info = False
                    player.stake += bet
                    self.pot += bet
                    player.chips -= bet
                    self.highest_stake = player.stake
                    self.ready_list.clear()
                    return True
            if response == "call_and_all_in":
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                player.stake += player.chips
                self.pot += player.chips
                player.stake_gap -= player.chips
                player.chips = 0
                print(f"{player.name} is all-in!")
                player.all_in = True
                self.highest_stake = player.stake
                self.ready_list.clear()
                return True
            if response == "all_in":
                player.stake_gap = 0
                player.stake += player.chips
                self.pot += player.chips
                player.chips = 0
                print(f"{player.name} is all-in!")
                player.all_in = True
                self.highest_stake = player.stake
                self.ready_list.clear()
                return True
            print("Invalid Response")

    def ask_players(self):
        self.ready_list.clear()
        for player in self.list_of_players_not_out:
            print(player.name, player.list_of_special_attributes)
        starting_index = self.list_of_players_not_out.index(self.first_actor)
        for player in self.list_of_players_not_out:
            player.ready = False
        while True:
            self.acting_player = self.list_of_players_not_out[starting_index]
            player_ready = self.answer(
                self.list_of_players_not_out[starting_index])
            starting_index += 1
            starting_index %= len(self.list_of_players_not_out)
            if player_ready:
                self.ready_list.append("gogo")
            if len(self.ready_list) == len(self.list_of_players_not_out):
                break

    def act_one(self):
        if self.small_blind_amount > self.small_blind.chips:
            self.small_blind.stake += self.small_blind.chips
            self.highest_stake = self.small_blind.chips
            self.pot += self.small_blind.chips
            self.small_blind.chips = 0
            print(f"{self.small_blind.name} is all-in!")
            self.small_blind.all_in = True
        else:
            self.small_blind.chips -= self.small_blind_amount
            self.small_blind.stake += self.small_blind_amount
            self.highest_stake = self.small_blind_amount
            self.pot += self.small_blind_amount
        if self.big_blind_amount > self.big_blind.chips:
            self.big_blind.stake += self.big_blind.chips
            self.highest_stake = self.big_blind.chips
            self.pot += self.big_blind.chips
            self.big_blind.chips = 0
            print(f"{self.big_blind.name} is all-in!")
            self.big_blind.all_in = True
        else:
            self.big_blind.chips -= self.big_blind_amount
            self.big_blind.stake += self.big_blind_amount
            self.highest_stake = self.big_blind_amount
            self.pot += self.big_blind_amount
        # self.ask_players()

    def answer_agent(self, player, response, raise_value):
        print(response)
        print(raise_value)
        time.sleep(3)
        player.stake_gap = self.highest_stake - player.stake
        if player.all_in or player.fold or self.fold_out:
            return True
        if player.chips <= 0:
            print(f"{player.name} is all in!")
            player.all_in = True
        print(f"Highest stake: {self.highest_stake}")
        print(
            f"Put in at least {player.stake_gap} to stay in.\nDon't Have that much? You'll have to go all-in!")
        print(f"Chips available: {player.chips}")
        self.possible_responses.clear()
        if player.stake_gap > 0:
            self.possible_responses.append("fold")
            if player.stake_gap == player.chips:
                self.possible_responses.append("all_in_exact")
            if player.stake_gap > player.chips:
                self.possible_responses.append("all_in_partial")
            if player.stake_gap < player.chips:
                self.possible_responses.append("call_exact")
                self.possible_responses.append("call_and_raise")
                self.possible_responses.append("call_and_all_in")
        if player.stake_gap == 0:
            self.possible_responses.append("check")
            self.possible_responses.append("raise")
            self.possible_responses.append("fold")
            self.possible_responses.append("all_in")
        while True:
            if response not in self.possible_responses:
                print(response)
                print("Invalid response")
                time.sleep(2)
                continue
            if response == "all_in_partial":
                player.stake += player.chips
                self.pot += player.chips
                player.stake_gap -= player.chips
                player.chips = 0
                print(f"{player.name} is all-in!")
                player.all_in = True
                return True
            if response == "all_in_exact":
                print(f"{player.name} is all-in!")
                player.all_in = True
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips = 0
                player.stake_gap = 0
                return True
            if response == "fold":
                player.fold = True
                self.fold_list.append(player)
                if len(self.fold_list) == (len(self.list_of_players_not_out) - 1):
                    for player in self.list_of_players_not_out:
                        if player not in self.fold_list:
                            self.fold_out = True
                            print(f"{player} wins!")
                            self.winners.append(player)
                            for player in self.winners:
                                player.win = True
                            self.round_ended = True
                return True
            if response == "call_exact":
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                return True
            if response == "check":
                player.stake_gap = 0
                return True
            if response == "raise":
                self.need_raise_info = True
                while True:

                    bet = int(raise_value)
                    if bet > player.chips or bet <= 0:
                        print("Invalid response")
                        continue
                    if bet == player.chips:
                        print(f"{player.name} is all-in!")
                        player.all_in = True
                    self.need_raise_info = False
                    player.stake += bet
                    self.pot += bet
                    player.chips -= bet
                    self.highest_stake = player.stake
                    self.ready_list.clear()
                    player.stake_gap = 0
                    return True
            if response == "call_and_raise":
                self.need_raise_info = True
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                while True:
                    try:
                        print("raised by ", raise_value)
                        bet = int(raise_value)
                    except ValueError:
                        continue
                    if bet > player.chips or bet <= 0:
                        print("Invalid response")
                        continue
                    if bet == player.chips:
                        print(f"{player.name} is all-in!")
                        player.all_in = True
                    self.need_raise_info = False
                    player.stake += bet
                    self.pot += bet
                    player.chips -= bet
                    self.highest_stake = player.stake
                    self.ready_list.clear()
                    return True
            if response == "call_and_all_in":
                player.stake += player.stake_gap
                self.pot += player.stake_gap
                player.chips -= player.stake_gap
                player.stake_gap = 0
                player.stake += player.chips
                self.pot += player.chips
                player.stake_gap -= player.chips
                player.chips = 0
                print(f"{player.name} is all-in!")
                player.all_in = True
                self.highest_stake = player.stake
                self.ready_list.clear()
                return True
            if response == "all_in":
                player.stake_gap = 0
                player.stake += player.chips
                self.pot += player.chips
                player.chips = 0
                print(f"{player.name} is all-in!")
                player.all_in = True
                self.highest_stake = player.stake
                self.ready_list.clear()
                return True
            print("Invalid Response")

    def ask_player_agent(self, response, raise_value, wanted_player):

        for player in self.list_of_players_not_out:
            if (wanted_player in player.list_of_special_attributes):
                # print(player.name)
                index = self.list_of_players_not_out.index(player)
        self.answer_agent(
            self.list_of_players_not_out[index], response, raise_value)

    def act_one_agent(self, response):
        if self.small_blind_amount > self.small_blind.chips:
            self.small_blind.stake += self.small_blind.chips
            self.highest_stake = self.small_blind.chips
            self.pot += self.small_blind.chips
            self.small_blind.chips = 0
            print(f"{self.small_blind.name} is all-in!")
            self.small_blind.all_in = True
        else:
            self.small_blind.chips -= self.small_blind_amount
            self.small_blind.stake += self.small_blind_amount
            self.highest_stake = self.small_blind_amount
            self.pot += self.small_blind_amount
        if self.big_blind_amount > self.big_blind.chips:
            self.big_blind.stake += self.big_blind.chips
            self.highest_stake = self.big_blind.chips
            self.pot += self.big_blind.chips
            self.big_blind.chips = 0
            print(f"{self.big_blind.name} is all-in!")
            self.big_blind.all_in = True
        else:
            self.big_blind.chips -= self.big_blind_amount
            self.big_blind.stake += self.big_blind_amount
            self.highest_stake = self.big_blind_amount
            self.pot += self.big_blind_amount
        self.ask_player_agent(response)
