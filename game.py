from deck import StandardDeck
from player import Player
import itertools
from collections import Counter


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

# Evalute the value of the players hand
    def hand_scorer(self, player):
        seven_cards = player.cards + self.cards
        all_hand_combos = list(itertools.combinations(seven_cards, 5))
        list_of_all_score_possibilities = []
        for i in all_hand_combos:
            suit_list = []
            value_list = []
            for j in i:
                suit_list.append(j.suit)
                value_list.append(j.value)
            initial_value_check = list(reversed(sorted(value_list)))
            score1 = 0
            score2 = 0
            score3 = 0
            score4 = initial_value_check.pop(0)
            score5 = initial_value_check.pop(0)
            score6 = initial_value_check.pop(0)
            score7 = initial_value_check.pop(0)
            score8 = initial_value_check.pop(0)
            list_of_pair_values = []
            other_cards_not_special = []
            pair_present = False
            pair_value = int
            value_counter = dict(Counter(value_list))
            for value_name, count in value_counter.items():
                if count == 2:
                    pair_present = True
                    pair_value = value_name
                    list_of_pair_values.append(value_name)
            if pair_present:
                for value in value_list:
                    if value not in list_of_pair_values:
                        other_cards_not_special.append(value)
                other_cards_not_special = list(
                    reversed(sorted(other_cards_not_special)))
                if len(set(list_of_pair_values)) == 1:
                    score1 = 1
                    score2 = max(list_of_pair_values)
                    try:
                        score3 = other_cards_not_special.pop(0)
                        score4 = other_cards_not_special.pop(0)
                        score5 = other_cards_not_special.pop(0)
                        score6 = other_cards_not_special.pop(0)
                        score7 = other_cards_not_special.pop(0)
                        score8 = other_cards_not_special.pop(0)
                    except IndexError:
                        pass
                if len(set(list_of_pair_values)) == 2:
                    list_of_pair_values = list(
                        reversed(sorted(list_of_pair_values)))
                    score1 = 2
                    score2 = list_of_pair_values.pop(0)
                    score3 = list_of_pair_values.pop(0)
                    try:
                        score4 = other_cards_not_special.pop(0)
                        score5 = other_cards_not_special.pop(0)
                        score6 = other_cards_not_special.pop(0)
                        score7 = other_cards_not_special.pop(0)
                        score8 = other_cards_not_special.pop(0)
                    except IndexError:
                        pass
            three_of_a_kind_value = int
            other_cards_not_special = []
            three_of_a_kind_present = False
            for value_name, count in value_counter.items():
                if count == 3:
                    three_of_a_kind_present = True
                    three_of_a_kind_value = value_name
            if three_of_a_kind_present:
                for value in value_list:
                    if value != three_of_a_kind_value:
                        other_cards_not_special.append(value)
                other_cards_not_special = list(
                    reversed(sorted(other_cards_not_special)))
                score1 = 3
                score2 = three_of_a_kind_value
                try:
                    score3 = other_cards_not_special.pop(0)
                    score4 = other_cards_not_special.pop(0)
                    score5 = other_cards_not_special.pop(0)
                    score6 = other_cards_not_special.pop(0)
                    score7 = other_cards_not_special.pop(0)
                    score8 = other_cards_not_special.pop(0)
                except IndexError:
                    pass
            if sorted(value_list) == list(range(min(value_list), max(value_list) + 1)):
                score1 = 4
                score2 = max(value_list)
            if sorted(value_list) == [0, 1, 2, 3, 12]:
                score1 = 4
                score2 = 3
            if len(set(suit_list)) == 1:
                score1 = 5
                score2 = max(value_list)
            if three_of_a_kind_present and pair_present:
                score1 = 6
                score2 = three_of_a_kind_value
                score3 = pair_value
            four_of_a_kind_value = int
            other_card_value = int
            four_of_a_kind = False
            for value_name, count in value_counter.items():
                if count == 4:
                    four_of_a_kind_value = value_name
                    four_of_a_kind: True
            for value in value_list:
                if value != four_of_a_kind_value:
                    other_card_value = value
            if four_of_a_kind:
                score1 = 7
                score2 = four_of_a_kind_value
                score3 = other_card_value
            if sorted(value_list) == [0, 1, 2, 3, 12] and len(set(suit_list)) == 1:
                score1 = 8
                score2 = 3
            if sorted(value_list) == list(range(min(value_list), max(value_list) + 1)) and len(set(suit_list)) == 1:
                score1 = 8
                score2 = max(value_list)
                if max(value_list) == 12:
                    score1 = 9
            list_of_all_score_possibilities.append(
                [score1, score2, score3, score4, score5, score6, score7, score8])
        best_score = max(list_of_all_score_possibilities)
        player.score = best_score
