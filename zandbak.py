from random import randint, random
from model import api
import simulation
from simulation import Simulation
from model.common import decay
from widgets import GuiApp
from model.needs import consumptions

#GET THE NEEDS FROM THE API
default_needs = api.get_needs()

# DE STEP OP 0 ZETEN ZODAT JE DE STARTWAARDEN KRIJGT EN DAN RESETTEN EN UPDATEN.
# aLS HIJ EENMAAL SIMULEERT KRIJG JE HEM NIET MEER OP DE STARTWAARDEN LIJKT HET...

# step = 0
# api.reset()
# api.update()
#
# print(needs)
# for k, v in needs.items():
#     print(k,v)
#
# print(needs['food'])

# EEN EIGEN SIMULATIETJE

#
# l_needs = list(needs.values())
# print(needs)

# step = 0
# api.reset()


inner_Adam = Simulation()
# inner_adam.current_simstep = 0
# printcounter = 0

#
# while inner_adam.step("eat") is True:
#     inner_adam.step("eat")
#  #   if printcounter == 1000:
#     print(inner_adam.log)
#  #       printcounter = 0
#  #   printcounter += 1



cons = (api.get_consumptions())
con_list = list(consumptions().values())
# Als de agent een appel eet dan wordt de eat consumption getriggerd


# als de food.value te laag wordt, moet de agent gaan lopen. Waarschijnljk door een goal te zetten: appel zoeken
# vraag is hoe je die goal beschrijft: de event wordt dan een goal.


data = []
moving = True
while inner_Adam.step() is True:
    if moving is True:                              #agent_host.sendCommand("move 1"):
        consumptions["sprint"].trigger()
    elif moving is False:                           #agent_host.sendCommand("move 0"):
        consumptions["recover"].trigger()
    inner_Adam.step()
    data = inner_Adam.log
    print(inner_Adam.log)

#MAKE A DICT FROM THE FIRST STEP
step1 = data[0]
step2 = data[1]
# GET THE REST NEED
need_rest1 = step1['needs']['rest']
need_rest2 = step2['needs']['rest']

#GET THEM FOR ALL STEPS
rest_dict = {}

def get_need_rest():
    rest_dict = {}
    for step in range(len(data)):
        rest_dict = data[step]['needs']['rest']
    return rest_dict

def get_rest_values():
    rest_values = [step["needs"]["rest"]["value"] for step in data]
    return rest_values


#step1_needs = step1['needs']


dict = {}
for k, v in step1_needs.items():
    dict = (k,v)




print(step1[0])
for i in step1:
    print(i)














