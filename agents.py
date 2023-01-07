from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, FSMBehaviour, State
from player import Player
from game import Game
from rules import find_winners, score_all
import asyncio
import spade
import time

class DealerAgent(Agent):
    def __init__(self, *xmpp, player, newgame):
        super().__init__(*xmpp)
        self.player = Player()
        self.player = player
        #self.game = Game()
        self.game = newgame
        self.possible_responses = []
        self.counter = 1
        self.next_round = False


    class MyBehav(FSMBehaviour):
        async def on_start(self):
            print("Game starting . . .")   
            self.counter = 1

    class State1(State):
        async def run(self):
            """
            if self.agent.next_round:
                print("I am here")
                self.agent.game.establish_player_attributes()
                self.agent.game.print_round_info()
                self.agent.game.act_one()
                self.next_round = False
                print(self.agent.next_round)
                time.sleep(3)
            """

            self.agent.game.deal_hole()
            self.agent.game.print_round_info()
            time.sleep(3)  
            self.agent.create_possible_responses()
            print(self.agent.possible_responses)
            print("Round: {}".format(self.agent.counter))
            #self.agent.game.act_one()
            self.agent.counter += 1
            msg = spade.message.Message(
                        to="test0904@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            if (msgD.body=="call_exact"):
                print("We are here he sent the corrent response")
                #self.agent.game.act_one()
                self.agent.game.ask_player_agent(msgD.body,"first actor")
                self.agent.game.print_round_info()
           
            response=self.agent.make_decision()
            self.agent.game.ask_player_agent(response,"dealer")
            self.agent.game.print_round_info()

            msg = spade.message.Message(
                        to="test0409@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"small blind")
            self.agent.game.print_round_info()

            msg = spade.message.Message(
                        to="test040998@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"big blind")
            self.agent.game.print_round_info()

            #time to move to state2
            self.set_next_state("State2")

            await asyncio.sleep(1)

    class State2(State):
        async def run(self):
            print(self.agent.possible_responses)
            print("Round: {}".format(self.agent.counter))
            self.agent.game.deal_flop()
            self.agent.game.print_round_info()
            self.agent.create_possible_responses()
            
            print(self.agent.possible_responses)
            print("Round: {}".format(self.agent.counter))


            msg = spade.message.Message(
                        to="test0904@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"first actor")
            self.agent.game.print_round_info()
            print("Round: {}".format(self.agent.counter))

            response=self.agent.make_decision()
            self.agent.game.ask_player_agent(response,"dealer")
            self.agent.game.print_round_info()

            print("Round: {}".format(self.agent.counter))

            msg = spade.message.Message(
                        to="test0409@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"small blind")
            self.agent.game.print_round_info()
            print("Round: {}".format(self.agent.counter))

            msg = spade.message.Message(
                        to="test040998@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"big blind")
            self.agent.game.print_round_info()

            self.agent.counter += 1

            #time to move to state2
            self.set_next_state("State3")

            await asyncio.sleep(1)

    class State3(State):
        async def run(self):
            print(self.agent.possible_responses)
            print("Round: {}".format(self.agent.counter))
            self.agent.game.deal_turn()
            self.agent.game.print_round_info()
            self.agent.create_possible_responses()
            
            print(self.agent.possible_responses)
            print("Round: {}".format(self.agent.counter))


            msg = spade.message.Message(
                        to="test0904@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"first actor")
            self.agent.game.print_round_info()
            print("Round: {}".format(self.agent.counter))

            response=self.agent.make_decision()
            self.agent.game.ask_player_agent(response,"dealer")
            self.agent.game.print_round_info()

            print("Round: {}".format(self.agent.counter))

            msg = spade.message.Message(
                        to="test0409@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"small blind")
            self.agent.game.print_round_info()
            print("Round: {}".format(self.agent.counter))

            msg = spade.message.Message(
                        to="test040998@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"big blind")
            self.agent.game.print_round_info()

            self.agent.counter += 1

            #time to move to state2
            self.set_next_state("State4")

            await asyncio.sleep(1)

    class State4(State):
        async def run(self):
            print(self.agent.possible_responses)
            print("Round: {}".format(self.agent.counter))
            self.agent.game.deal_river()
            self.agent.game.print_round_info()
            self.agent.create_possible_responses()
            
            print(self.agent.possible_responses)
            print("Round: {}".format(self.agent.counter))


            msg = spade.message.Message(
                        to="test0904@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"first actor")
            self.agent.game.print_round_info()
            print("Round: {}".format(self.agent.counter))

            response=self.agent.make_decision()
            self.agent.game.ask_player_agent(response,"dealer")
            self.agent.game.print_round_info()

            print("Round: {}".format(self.agent.counter))

            msg = spade.message.Message(
                        to="test0409@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"small blind")
            self.agent.game.print_round_info()
            print("Round: {}".format(self.agent.counter))

            msg = spade.message.Message(
                        to="test040998@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"big blind")
            self.agent.game.print_round_info()

            self.agent.counter += 1

            #time to move to state2
            self.set_next_state("State5")

            await asyncio.sleep(1)

    class State5(State):
        async def run(self):
            print(self.agent.possible_responses)
            print("Round: {}".format(self.agent.counter))
            self.agent.game.print_round_info()
            self.agent.create_possible_responses()
            
            print(self.agent.possible_responses)
            print("Round: {}".format(self.agent.counter))


            msg = spade.message.Message(
                        to="test0904@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"first actor")
            self.agent.game.print_round_info()
            print("Round: {}".format(self.agent.counter))

            response=self.agent.make_decision()
            self.agent.game.ask_player_agent(response,"dealer")
            self.agent.game.print_round_info()

            print("Round: {}".format(self.agent.counter))

            msg = spade.message.Message(
                        to="test0409@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"small blind")
            self.agent.game.print_round_info()
            print("Round: {}".format(self.agent.counter))

            msg = spade.message.Message(
                        to="test040998@jabber.hot-chilli.net",
                        body="What do you want to do?")
            await self.send(msg)
            msgD = await self.receive(timeout=20)
            print(f"{msgD.sender} Player is answering you: {msgD.body}")
            self.agent.game.ask_player_agent(msgD.body,"big blind")
            self.agent.game.print_round_info()

            self.agent.counter += 1

            #time to move to state2
            score_all(self.agent.game)
            self.agent.game.print_round_info()
            find_winners(self.agent.game)

            time.sleep(2)
            self.agent.game.round_ended = True
            self.agent.game.end_round()
            self.agent.next_round = True
            self.set_next_state("State1")


            await asyncio.sleep(1)


    async def setup(self):
        print(f"I am your dealer: {self.player.name} and i have so many chips: {self.player.chips}")
        b = self.MyBehav()
        b.add_state(name="State1", state=self.State1(), initial=True)
        b.add_state(name="State2", state=self.State2())
        b.add_state(name="State3", state=self.State3())
        b.add_state(name="State4", state=self.State4())
        b.add_state(name="State5", state=self.State5())
        b.add_transition(source="State1", dest="State2")
        b.add_transition(source="State2", dest="State3")
        b.add_transition(source="State3", dest="State4")
        b.add_transition(source="State4", dest="State5")
        b.add_transition(source="State5", dest="State1")
        self.add_behaviour(b)

    def create_possible_responses(self):
        self.player.stake_gap = self.game.highest_stake - self.player.stake
        self.possible_responses.clear()
        if self.player.stake_gap > 0:
            self.possible_responses.append("fold")
            if self.player.stake_gap == self.player.chips:
                self.possible_responses.append("all_in_exact")
            if self.player.stake_gap > self.player.chips:
                self.possible_responses.append("all_in_partial")
            if self.player.stake_gap < self.player.chips:
                self.possible_responses.append("call_exact")
                self.possible_responses.append("call_and_raise")
                self.possible_responses.append("call_and_all_in")
        if self.player.stake_gap == 0:
            self.possible_responses.append("check")
            self.possible_responses.append("raise")
            self.possible_responses.append("fold")
            self.possible_responses.append("all_in")

    def make_decision(self):
        if("check" in self.possible_responses):
                response="check"
        elif ("call_exact" in self.possible_responses):
                response = "call_exact"
        elif ("fold" in self.possible_responses):
                response = "fold"
        elif ("raise" in self.possible_responses):
                response = "raise"
        elif ("all_in" in self.possible_responses):
                response = "all_in"
        elif ("call_and_raise" in self.possible_responses):
                response = "call_and_raise"
        elif ("call_and_all_in" in self.possible_responses):
                response = "call_and_all_in"
        elif ("all_in_partial" in self.possible_responses):
                response = "all_in_partial"
        elif ("all_in_exact" in self.possible_responses):
                response = "all_in_exact"
        return response

class PlayerAgent(Agent):
    def __init__(self, *xmpp, player, newgame):
        super().__init__(*xmpp)
        self.player = Player()
        self.player = player
        #self.game = Game()
        self.game = newgame
        self.possible_responses = []
        self.next_round = False
        #self.possible_responses = ["check", "raise", "fold", "all_in", "call_exact"]


    class MyBehav(FSMBehaviour):
        async def on_start(self):
            print("Player Agent starting . . .")
            
            
            
    class State1(State):
        async def run(self):
            print(self.agent.next_round)
            #This cant work, have to find a different method maybe send the message to dealer and he waits to collect all 4
            if self.agent.next_round:
                print("I am here in agent")
                self.agent.game.establish_player_attributes()
                self.agent.game.print_round_info()
                self.agent.game.act_one()
                self.agent.next_round = False
                print(self.agent.next_round)
                time.sleep(3)
            print("In state")
            self.agent.create_possible_responses()
            print(self.agent.possible_responses)
            #time.sleep(4)
            response=self.agent.make_decision()
            print("this is my response:",response)

            time.sleep(2)

            msgD = await self.receive(timeout=20)
            if msgD:
                print(f"{msgD.sender} Dealer is asking you: {msgD.body}")
                msg = spade.message.Message(
                        to=str(msgD.sender),
                        body=response)
                await self.send(msg)

            self.set_next_state("State2")
            await asyncio.sleep(1)

    class State2(State):
        async def run(self):
            print("In state")
            self.agent.create_possible_responses()
            print(self.agent.possible_responses)
            #time.sleep(4)

            response=self.agent.make_decision()

            msgD = await self.receive(timeout=20)
            if msgD:
                print(f"{msgD.sender} Dealer is asking you: {msgD.body}")
                msg = spade.message.Message(
                        to=str(msgD.sender),
                        body=response)
                await self.send(msg)

            self.set_next_state("State3")
            await asyncio.sleep(1)

    class State3(State):
        async def run(self):
            print("In state")
            self.agent.create_possible_responses()
            print(self.agent.possible_responses)
            #time.sleep(4)

            response=self.agent.make_decision()

            msgD = await self.receive(timeout=20)
            if msgD:
                print(f"{msgD.sender} Dealer is asking you: {msgD.body}")
                msg = spade.message.Message(
                        to=str(msgD.sender),
                        body=response)
                await self.send(msg)
            
            self.set_next_state("State4")
            await asyncio.sleep(1)

    class State4(State):
        async def run(self):
            print("In state")
            self.agent.create_possible_responses()
            print(self.agent.possible_responses)
            #time.sleep(4)

            response=self.agent.make_decision()

            msgD = await self.receive(timeout=20)
            if msgD:
                print(f"{msgD.sender} Dealer is asking you: {msgD.body}")
                msg = spade.message.Message(
                        to=str(msgD.sender),
                        body=response)
                await self.send(msg)
            
            self.set_next_state("State5")
            await asyncio.sleep(1)

    class State5(State):
        async def run(self):
            print("In state")
            self.agent.create_possible_responses()
            print(self.agent.possible_responses)
            #time.sleep(4)

            response=self.agent.make_decision()

            msgD = await self.receive(timeout=20)
            if msgD:
                print(f"{msgD.sender} Dealer is asking you: {msgD.body}")
                msg = spade.message.Message(
                        to=str(msgD.sender),
                        body=response)
                await self.send(msg)

            self.agent.next_round = True
            print(self.agent.next_round)
            self.set_next_state("State1")
            await asyncio.sleep(1)

    async def setup(self):
        print(f"I am: {self.player.name} and i have so many chips: {self.player.chips}")
        b = self.MyBehav()
        b.add_state(name="State1", state=self.State1(), initial=True)
        b.add_state(name="State2", state=self.State2())
        b.add_state(name="State3", state=self.State3())
        b.add_state(name="State4", state=self.State4())
        b.add_state(name="State5", state=self.State5())
        b.add_transition(source="State1", dest="State2")
        b.add_transition(source="State2", dest="State3")
        b.add_transition(source="State3", dest="State4")
        b.add_transition(source="State4", dest="State5")
        b.add_transition(source="State5", dest="State1")
        self.add_behaviour(b)
    
    def create_possible_responses(self):
        self.player.stake_gap = self.game.highest_stake - self.player.stake
        self.possible_responses.clear()
        if self.player.stake_gap > 0:
            self.possible_responses.append("fold")
            if self.player.stake_gap == self.player.chips:
                self.possible_responses.append("all_in_exact")
            if self.player.stake_gap > self.player.chips:
                self.possible_responses.append("all_in_partial")
            if self.player.stake_gap < self.player.chips:
                self.possible_responses.append("call_exact")
                self.possible_responses.append("call_and_raise")
                self.possible_responses.append("call_and_all_in")
        if self.player.stake_gap == 0:
            self.possible_responses.append("check")
            self.possible_responses.append("raise")
            self.possible_responses.append("fold")
            self.possible_responses.append("all_in")
    
    def make_decision(self):
        if("call_exact" in self.possible_responses):
                response="call_exact"
        elif ("check" in self.possible_responses):
                response = "check"
        elif ("fold" in self.possible_responses):
                response = "fold"
        elif ("raise" in self.possible_responses):
                response = "raise"
        elif ("all_in" in self.possible_responses):
                response = "all_in"
        elif ("call_and_raise" in self.possible_responses):
                response = "call_and_raise"
        elif ("call_and_all_in" in self.possible_responses):
                response = "call_and_all_in"
        elif ("all_in_partial" in self.possible_responses):
                response = "all_in_partial"
        elif ("all_in_exact" in self.possible_responses):
                response = "all_in_exact"
        return response
