class Player(object):
    def __init__(self, name=None):
        self.name = name
        self.chips = 0
        self.stake = 0
        self.stake_gap = 0
        self.cards = []
        self.score = []
        self.fold = False
        self.ready = False
        self.all_in = False
        self.list_of_special_attributes = []
        self.win = False

    def __repr__(self):
        name = self.name
        return name

    def establish_player_attributes(list_of_players_not_out):
        address_assignment = 0
        dealer = list_of_players_not_out[address_assignment]
        dealer.list_of_special_attributes.append("dealer")
        address_assignment += 1
        address_assignment %= len(list_of_players_not_out)
        small_blind = list_of_players_not_out[address_assignment]
        small_blind.list_of_special_attributes.append("small blind")
        address_assignment += 1
        address_assignment %= len(list_of_players_not_out)
        big_blind = list_of_players_not_out[address_assignment]
        big_blind.list_of_special_attributes.append("big blind")
        address_assignment += 1
        address_assignment %= len(list_of_players_not_out)
        first_actor = list_of_players_not_out[address_assignment]
        first_actor.list_of_special_attributes.append("first actor")
        list_of_players_not_out.append(
            list_of_players_not_out.pop(0))
