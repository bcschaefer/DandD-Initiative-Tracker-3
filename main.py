#track initiative
#track hp
#track buffs & debuffs & conditions
from InitiativeTracker import Tracker
import os

PlayerInitiative = {}
MonsterInitiative = {}
crXP = {1/8:25, 1/4:50, 1/2:100, 1:200, 2:450, 3:700, 4:1100, 5:1800, 6:2300, 7:2900, 8:3900, 9:5000, 10:5900, 11:7200, 12:8400, 13:10000, 14:11500, 15:13000, 16:15000, 17:18000, 18:20000, 19:25000, 20:25000, 21:33000, 22:41000, 23:50000, 24:62000, 25:75000, 26:90000, 27:105000, 28:120000, 29:135000, 30:155000} #dictionary of monster xp
CR = 4

#converts file of players' information into list
def readPlayerFile(file):
  f = open(file, "r")
  next(f)
  for line in f:
    name, initiative, hp, maxhp = line.split(",")
    PlayerInitiative[str(name)] = [int(initiative),int(hp), int(maxhp), []]

#converts file of monsters' information into list
def readMonsterFile(file):
  f = open(file, "r")
  next(f)
  for line in f:
    name, initiative, hp, maxhp, cr = line.split(",")
    MonsterInitiative[str(name)] = [int(initiative),int(hp), int(maxhp), [], int(cr)]
    
#player stats
PlayerCheck = input("Use pregenerated characters (y/n)? ")
if PlayerCheck[0].lower() == 'n':
  playerNum = int(input("How many players do you want to add? "))
  os.system('clear')
  for i in range(playerNum): 
    Player = input(f"Enter the name of Player {i+1}: ")
    Initiative=int(input(f"Enter {Player}'s Initiative: "))
    currentHP = int(input(f"Enter {Player}'s Current HP: "))
    maxHP = int(input(f"Enter {Player}'s Max HP: "))
    Conditions = []
    PlayerInitiative[Player]=[Initiative, currentHP, maxHP, Conditions]
    os.system('clear')
if PlayerCheck[0].lower()== 'y': #option to import file
  while True:
    try:
      file = input("Enter file: ")
      readPlayerFile(file)
      break
    except:
      input("Invalid File Name")


#monster stats
MonstersCheck = input("Use pregenerated monsters (y/n)? ")
if MonstersCheck[0].lower() == 'n':
  MonsterNum = int(input("How many monsters do you want to add? "))
  os.system('clear')
  for i in range(MonsterNum): 
    Monster = input(f"Enter the name of Monster {i+1}: ")
    Initiative=int(input(f"Enter {Monster}'s Initiative: "))
    currentHP = int(input(f"Enter {Monster}'s HP: "))
    maxHP = int(input(f"Enter {Monster}'s HP: "))
    Conditions = []
    CR = int(input(f"Enter the CR of {Monster}: ")) #Almost redundant-- only identifies monster in combined initiative
    MonsterInitiative[Monster]=[Initiative,currentHP,maxHP,Conditions,CR]
    os.system('clear')
if MonstersCheck[0].lower() == 'y':
  while True: #option to import file
    try:
      file = input("Enter file: ")
      readMonsterFile(file)
      break
    except:
      input("Invalid File Name")
  


Encounter = Tracker(PlayerInitiative, MonsterInitiative)

for monster in MonsterInitiative.keys():
  if '/' in str(MonsterInitiative[monster][CR]):
    crList = MonsterInitiative[monster][CR].split('/')
    newCR = int(crList[0])/int(crList[1])
    MonsterInitiative[monster][CR] = newCR
    
totalXP = 0
for index, creature in enumerate(MonsterInitiative.keys()):
  totalXP+=crXP[MonsterInitiative[creature][CR]]

Tracker.order_initiative(Encounter)
Tracker.rotate_initiative(Encounter)
os.system('clear')
print('Encounter Over--All Monsters are dead')
print(f"Total XP: {totalXP}")
print(f"Individual XP: {int(totalXP/len(PlayerInitiative.keys()))}")