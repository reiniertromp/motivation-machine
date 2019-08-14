from __future__ import print_function
from builtins import range
import MalmoPython
import os
import sys
import time
import json
from xml_settings import *
#import agent
import threading

# optional imports
from model.needs import needs, consumptions
from model.agent import Need, Modulator, Consumption
from random import randint, random
import math

from widgets import Settings
from helper_widgets import Diagram

from model import api
from model.needs import needs, consumptions
from model.modulators import modulators, aggregates
from model.emotions import emotions
from simulation import Simulation

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# Create default Malmo objects:
class Adam:

    def __init__(self):
        self.moving = False
        self.resting = False
        self.mission_started = False
        self.data = []
        self.time_step = 0
        self.inner_Adam = Simulation()
        self.agent_host = MalmoPython.AgentHost()
        self.reset = api.reset()
        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:',e)
            print(self.agent_host.getUsage())
            exit(1)
        if self.agent_host.receivedArgument("help"):
            print(self.agent_host.getUsage())
            exit(0)
        
        #Build a mission and give it the configuration of the world. Note that we can change that later with Python (not XML) code.
        self.my_mission = MalmoPython.MissionSpec(missionXML, True)
        self.my_mission_record = MalmoPython.MissionRecordSpec()

        #We may also store previous observations within Malmo, but let MicroPsi take care of remembering what they were.
        self.agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
        self.my_mission.forceWorldReset()

    def start_mission(self):    
        max_retries = 3
        for retry in range(max_retries):
            try:
                self.agent_host.startMission(self.my_mission, self.my_mission_record)
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:",e)
                    exit(1)
                else:
                    time.sleep(1)

    def loop_until_mission_starts(self):
        print("Waiting for the mission to start ",)
        self.world_state = self.agent_host.getWorldState()
        while not self.world_state.has_mission_begun:
            sys.stdout.write(".")
            time.sleep(0.1)
            self.world_state = self.agent_host.getWorldState()
            for error in self.world_state.errors:
                print("Error:",error.text)
        print()
        print("Mission running ",)

    def get_world_state(self):
        #Helper function to ensure we get the world state.
        world_state = agent_host.peekWorldState()
        while world_state.is_mission_running and all (e.text=='{}' for e in world_state.observations):
            world_state = agent_host.peekWorldState()
        return world_state


    def get_observations(self):
        world_state = self.get_world_state()
        if not all(e.text=='{}' for e in world_state.observations):
            obs = json.loads( world_state.observations[-1].text )
        else:
            raise Exception('\nSomehow did not get observations, despite waiting for them.\n')
        return obs

    def get_rest_values(self, data):
        """returns a list of values of the rest need  """
        rest_values = [step["needs"]["rest"]["value"] for step in data]
        return rest_values[-1]

    def appelboer(self):
        if not self.mission_started:            
            self.start_mission()
            self.loop_until_mission_starts()
            self.mission_started = True
        
        #Check whether the mission is actually running. (When MicroPsi thinks it is.)
        else:           
            world_state = self.agent_host.peekWorldState()
            if not world_state.is_mission_running:
                raise Exception('\nMission no longer running!\n')


        if self.time_step == 10:
            self.agent_host.sendCommand('move 1')
            self.moving=True

        print(api.get_needs_and_consumptions())

       # optional for consumption triggers
       # print(api.get_needs())
        #
        # if self.moving:  # agent_host.sendCommand("move 1"):     # IF ADAM MOVES TRIGGER SPRINT CONSUMPTION
        #
        #     consumptions["sprint"].trigger()
        #     consumptions.update()
        # elif not self.moving:  # agent_host.sendCommand("move 0"):  # IF HE STANDS STILL, TRIGGER RECOVER CONSUMPTION
        #     consumptions["recover"].trigger()
        #
        # self.data = self.inner_Adam.log
        # rest_values = self.get_rest_values(self.data)
        # print(rest_values)

        print('\nTime step {0} finished, mission still running.\n'.format(str(self.time_step)))
        self.time_step += 1

    def start_simulation(self):
        self.my_mission.forceWorldReset()
        print("Start nu de main loop.")
        while self.inner_Adam.step():
            self.appelboer()
        print("\nAfgelopen.\n")

if __name__ == "__main__":
    reinier = Adam()
    reinier.start_simulation()



