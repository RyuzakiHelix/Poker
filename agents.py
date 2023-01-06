from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from player import Player
from game import Game
import asyncio
import spade


class AgentPlayerOne(Agent):

    class PlayBehavior1(PeriodicBehaviour):
        async def run(self):
            print("ovdje sam Periodic")

    class PlayBehavior2(CyclicBehaviour):
        async def run(self):
            print("ovdje sam Cyclic")

    async def setup(self):
        b1 = self.PlayBehavior1()
        b2 = self.PlayBehavior2()
        self.add_behaviour(b2)


class PrviAgent(Agent):
    async def setup(self):
        print("PrviAgent: Pokrecem se!")


class DealerAgent(Agent):
    def __init__(self, *xmpp, player, newgame):
        super().__init__(*xmpp)
        self.dealer = Player()
        self.dealer = player
        # self.game = Game()
        self.game = newgame

    class MyBehav(CyclicBehaviour):
        async def on_start(self):
            print("Game starting . . .")
            self.agent.game.deal_hole()
            self.agent.game.print_round_info()

            self.counter = 1

        async def run(self):
            print("Round: {}".format(self.counter))
            # self.agent.game.act_one()
            self.agent.game.print_round_info()
            self.counter += 1
            # This is weird, it works but vsc doesnt register it as right
            # print(self.agent.dealer.name)
            msg = spade.message.Message(
                to="test0904@jabber.hot-chilli.net",
                body="Želiš li igrati?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} šalje poruku: {msgD.body}")
            if (msgD.body == "Da želim igrati!"):
                print("We are here he sent the corrent response")

            await asyncio.sleep(1)

    async def setup(self):
        print(
            f"I am your dealer: {self.dealer.name} and i have so many chips: {self.dealer.chips}")
        b = self.MyBehav()
        self.add_behaviour(b)


class PlayerAgent(Agent):
    def __init__(self, *xmpp, player, newgame):
        super().__init__(*xmpp)
        self.player = Player()
        self.player = player
        # self.game = Game()
        self.game = newgame

    class MyBehav(CyclicBehaviour):
        async def on_start(self):
            print("Game starting . . .")

        async def run(self):
            print("I am running")
            msgD = await self.receive(timeout=20)
            if msgD:
                print(f"{msgD.sender} šalje poruku: {msgD.body}")
                msg = spade.message.Message(
                    to=str(msgD.sender),
                    body="Da želim igrati!")
                await self.send(msg)
            await asyncio.sleep(1)

    async def setup(self):
        print(
            f"It is my call: {self.player.name} and i have so many chips: {self.player.chips}")
        b = self.MyBehav()
        self.add_behaviour(b)
