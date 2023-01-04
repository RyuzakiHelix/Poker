import itertools
from collections import Counter
# Evalute the value of the players hand
# Have to fix this logic


def hand_scorer(game, player):
    seven_cards = player.cards + game.cards
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


def score_all(game):
    for player in game.list_of_players_not_out:
        hand_scorer(game, player)
        print(f"Player {player.name} has a score of: {player.score}")


def find_winners(game):
    if game.fold_out:
        for player in list(set(game.winners)):
            player.chips += int((game.pot / len(list(set(game.winners)))))
            print(
                f"{player.name} wins {int((game.pot / len(list(set(game.winners)))))} chips!")
    else:
        list_of_stakes = []
        for player in game.list_of_players_not_out:
            list_of_stakes.append(player.stake)
        list_of_stakes = list(set(list_of_stakes))
        list_of_stakes = sorted(list_of_stakes)
        for stake in list_of_stakes:
            print(stake)
        for player in game.list_of_players_not_out:
            print(player.name)
            print(player.stake)
        # print(game.list_of_players_not_out)
        list_of_players_at_stake = []
        list_of_list_of_players_at_stake = []
        for i in range(len(list_of_stakes)):
            for player in game.list_of_players_not_out:
                if player.stake >= list_of_stakes[i]:
                    list_of_players_at_stake.append(player)
            list_of_list_of_players_at_stake.append(
                list(set(list_of_players_at_stake)))
            list_of_players_at_stake.clear()
        # print(list_of_list_of_players_at_stake)
        list_of_pot_seeds = []
        for i in list_of_stakes:
            list_of_pot_seeds.append(i)
        list_of_pot_seeds.reverse()
        for i in range(len(list_of_pot_seeds)):
            try:
                list_of_pot_seeds[i] -= list_of_pot_seeds[i + 1]
            except IndexError:
                pass
        list_of_pot_seeds.reverse()
        list_of_pots = []
        for i in range(len(list_of_pot_seeds)):
            print(len(list_of_list_of_players_at_stake[i]))
        for i in range(len(list_of_pot_seeds)):
            list_of_pots.append(
                list_of_pot_seeds[i] * len(list_of_list_of_players_at_stake[i]))
        for i in range(len(list_of_pots)):
            winners = []
            game.list_of_scores_eligible.clear()
            for player in list_of_list_of_players_at_stake[i]:
                if player.fold:
                    pass
                else:
                    game.list_of_scores_eligible.append(player.score)
            max_score = max(game.list_of_scores_eligible)
            for player in list_of_list_of_players_at_stake[i]:
                if player.fold:
                    pass
                else:
                    if player.score == max_score:
                        player.win = True
                        winners.append(player)
            prize = int(list_of_pots[i] / len(winners))
            for player in winners:
                print(f"{player.name} wins {prize} chips!")
                player.chips += prize
                game.pot -= prize
        for player in game.list_of_players_not_out:
            if player.win:
                print({player.name})
            elif player.fold:
                print("\n" + player.name + ": " +
                      str(player.cards) + "\n\t" + "[FOLDED]")
            else:
                print({player.name})
            print(f"\tScoreCode: {player.score}")
            print(f"Pot: {game.pot}")
        [print(player.name, player.chips)
         for player in game.list_of_players_not_out]


"""
def score_interpreter(player):
    list_of_hand_types = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush",
                          "Full House",
                          "Four of a Kind", "Straight Flush", "Royal Flush"]
    list_of_values_to_interpret = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
                                   "Jack",
                                   "Queen",
                                   "King", "Ace"]
    hand_type = list_of_hand_types[player.score[0]]
    mod1 = list_of_values_to_interpret[player.score[1]]
    mod2 = list_of_values_to_interpret[player.score[2]]
    mod3 = list_of_values_to_interpret[player.score[3]]
    if player.score[0] == 0:
        return hand_type + ": " + mod3
    if player.score[0] == 1:
        return hand_type + ": " + mod1 + "s"
    if player.score[0] == 2:
        return hand_type + ": " + mod1 + "s" + " and " + mod2 + "s"
    if player.score[0] == 3:
        return hand_type + ": " + mod1 + "s"
    if player.score[0] == 4:
        return hand_type + ": " + mod1 + " High"
    if player.score[0] == 5:
        return hand_type + ": " + mod1 + " High"
    if player.score[0] == 6:
        return hand_type + ": " + mod1 + "s" + " and " + mod2 + "s"
    if player.score[0] == 7:
        return hand_type + ": " + mod1 + "s"
    if player.score[0] == 8:
        return hand_type + ": " + mod1 + " High"
    if player.score[0] == 9:
        return hand_type
"""
