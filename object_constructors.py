import random
from random import random, choice
import time

def gen_food(x,z):

	food = choice(['bread','apple'])
	generatorString = '<DrawItem x="{0}" z="{1}" y="{2}" type="{3}"/>'.format(x, z, 4, food)

	return generatorString

def gen_lots_of_food():

	generatorString = ''

	for x in range(-49,49,1):
		for z in range(-49,49,1):
			if random() > 0.8:
				print(time.sleep(0.00001))
				generatorString += gen_food(x,z)
				print(time.sleep(0.00001))

	return generatorString

"""
MOCHT JE HET LEUK VINDEN KAN JE BOMEN PLAATSEN
MISSCHIEN EEN IDEE VOOR EXPLORATION = BOOM GEVONDEN
"""

def draw_cuboid(x1, x2, z1, z2, y1, y2 ,t ):
	return '<DrawCuboid x1="{x1}" x2="{x2}" z1="{z1}" z2="{z2}" y1="{y1}" y2="{y2}" type="{t}"/>'.format(
	  x1= x1,
	  x2= x2,
	  z1= z1,
	  z2= z2,
	  y1= y1,
	  y2= y2,
	  t=t)

def gen_tree(x,z):

	tree_length = random.randint(3,14)
		
	start = float(random.randint(1,3))
	tree_foliage_start = int( round( (start / (start+1)) * float(tree_length) ) )
	leaves = random.choice(['leaves','leaves2'])
	log = random.choice(['log','log2'])

	#Make top foliage
	generatorString = '<DrawBlock x="{0}" z="{1}" y="{2}" type="{3}"/>'.format(x, z, tree_length+6, leaves)
	generatorString += draw_cuboid(x-1,x+2,z-1,z+1,tree_length+5,tree_length+5,leaves)
	
	foliage_around_trunk = tree_length - tree_foliage_start + 1
	for i in range(foliage_around_trunk):
		#max reach
		s = 1 #Can change this to create wider foliage.
		generatorString += draw_cuboid(x-s-i,x+s+i,z-s-i,z+s+i,tree_length-i+4,tree_length-i+4,leaves)

	#I'm putting this here because I think later entries override earlier ones, and I want a stem instead of foliage.
	generatorString += draw_cuboid(x,x,z,z,4,tree_length+4,log)
	return generatorString