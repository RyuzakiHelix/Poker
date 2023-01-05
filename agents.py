from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from player import Player
import asyncio


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


class TestAgent(Agent):
    class MyBehav(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour . . .")
            self.counter = 0

        async def run(self):
            print("Counter: {}".format(self.counter))
            self.counter += 1
            await asyncio.sleep(1)

    async def setup(self):
        print("Agent starting . . .")
        b = self.MyBehav()
        self.add_behaviour(b)
