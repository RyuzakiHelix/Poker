from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, FSMBehaviour, State
from player import Player
from game import Game
import asyncio
import spade


class DealerAgent(Agent):
    def __init__(self, *xmpp, player, newgame):
        super().__init__(*xmpp)
        self.player = Player()
        self.player = player
        # self.game = Game()
        self.game = newgame
        self.possible_responses = []
        self.counter = 1

    class MyBehav(FSMBehaviour):
        async def on_start(self):
            print("Game starting . . .")
            self.agent.game.deal_hole()
            self.agent.game.print_round_info()
            self.agent.player.stake_gap = self.agent.game.highest_stake - self.agent.player.stake
            self.agent.possible_responses.clear()
            if self.agent.player.stake_gap > 0:
                self.agent.possible_responses.append("fold")
                if self.agent.player.stake_gap == self.agent.player.chips:
                    self.agent.possible_responses.append("all_in_exact")
                if self.agent.player.stake_gap > self.agent.player.chips:
                    self.agent.possible_responses.append("all_in_partial")
                if self.agent.player.stake_gap < self.agent.player.chips:
                    self.agent.possible_responses.append("call_exact")
                    self.agent.possible_responses.append("call_and_raise")
                    self.agent.possible_responses.append("call_and_all_in")
            if self.agent.player.stake_gap == 0:
                self.agent.possible_responses.append("check")
                self.agent.possible_responses.append("raise")
                self.agent.possible_responses.append("fold")
                self.agent.possible_responses.append("all_in")

            self.counter = 1

    class State1(State):
        async def run(self):
            print(self.agent.possible_responses)
            print("Round: {}".format(self.agent.counter))
            # self.agent.game.act_one()
            self.agent.counter += 1
            # This is weird, it works but vsc doesnt register it as right
            # print(self.agent.dealer.name)
            # print(self.agent.game.first_actor.name)
            msg = spade.message.Message(
                to="test0904@jabber.hot-chilli.net",
                body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            if (msgD.body == "call_exact"):
                print("We are here he sent the corrent response")
                # self.agent.game.act_one()
                self.agent.game.ask_player_agent(msgD.body, "first actor")
                self.agent.game.print_round_info()

            self.agent.game.ask_player_agent("call_exact", "dealer")
            self.agent.game.print_round_info()

            msg = spade.message.Message(
                to="test0409@jabber.hot-chilli.net",
                body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body, "small blind")
            self.agent.game.print_round_info()

            msg = spade.message.Message(
                to="test040998@jabber.hot-chilli.net",
                body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body, "big blind")
            self.agent.game.print_round_info()

            # time to move to state2

            await asyncio.sleep(1)

    async def setup(self):
        print(
            f"I am your dealer: {self.player.name} and i have so many chips: {self.player.chips}")
        b = self.MyBehav()
        b.add_state(name="State1", state=self.State1(), initial=True)
        self.add_behaviour(b)


class PlayerAgent(Agent):
    def __init__(self, *xmpp, player, newgame):
        super().__init__(*xmpp)
        self.player = Player()
        self.player = player
        # self.game = Game()
        self.game = newgame
        self.possible_responses = []
        # self.possible_responses = ["check", "raise", "fold", "all_in", "call_exact"]

    class MyBehav(FSMBehaviour):
        async def on_start(self):
            print("Player Agent starting . . .")
            self.agent.player.stake_gap = self.agent.game.highest_stake - self.agent.player.stake
            self.agent.possible_responses.clear()
            if self.agent.player.stake_gap > 0:
                self.agent.possible_responses.append("fold")
                if self.agent.player.stake_gap == self.agent.player.chips:
                    self.agent.possible_responses.append("all_in_exact")
                if self.agent.player.stake_gap > self.agent.player.chips:
                    self.agent.possible_responses.append("all_in_partial")
                if self.agent.player.stake_gap < self.agent.player.chips:
                    self.agent.possible_responses.append("call_exact")
                    self.agent.possible_responses.append("call_and_raise")
                    self.agent.possible_responses.append("call_and_all_in")
            if self.agent.player.stake_gap == 0:
                self.agent.possible_responses.append("check")
                self.agent.possible_responses.append("raise")
                self.agent.possible_responses.append("fold")
                self.agent.possible_responses.append("all_in")

    class State1(State):
        async def run(self):
            print("In state")

            print(self.agent.possible_responses)
            if ("check" in self.agent.possible_responses):
                response = "check"
            elif ("call_exact" in self.agent.possible_responses):
                response = "call_exact"
            elif ("fold" in self.agent.possible_responses):
                response = "fold"
            elif ("raise" in self.agent.possible_responses):
                response = "raise"
            elif ("all_in" in self.agent.possible_responses):
                response = "all_in"
            elif ("call_and_raise" in self.agent.possible_responses):
                response = "call_and_raise"
            elif ("call_and_all_in" in self.agent.possible_responses):
                response = "call_and_all_in"
            elif ("all_in_partial" in self.agent.possible_responses):
                response = "all_in_partial"
            elif ("all_in_exact" in self.agent.possible_responses):
                response = "all_in_exact"

            msgD = await self.receive(timeout=20)
            if msgD:
                print(f"{msgD.sender} Dealer is asking you: {msgD.body}")
                msg = spade.message.Message(
                    to=str(msgD.sender),
                    body=response)
                await self.send(msg)
            await asyncio.sleep(1)

    async def setup(self):
        print(
            f"It is my call: {self.player.name} and i have so many chips: {self.player.chips}")
        b = self.MyBehav()
        b.add_state(name="State1", state=self.State1(), initial=True)
        self.add_behaviour(b)
