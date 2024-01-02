import os

def dispindex(value): #needed a parameter
  return value+1


INITIATIVE = 0
CURRENTHP = 1
MAXHP = 2
CONDITIONS = 3
CR = 4

class Tracker(object):
  def __init__(self, p={}, m={}): #p={Player:[Initiative,Current HP,Conditions,Max HP]} m={Monster:[Initiative,HP,Conditions, CR, Max HP]}
    self.players = p
    self.monsters = m
  def order_initiative(self): #ordered dictionary of all creatures in battle
    global initiativeOrder
    initiativeOrder = self.players.copy()
    initiativeOrder.update(self.monsters) #combine player and monster dictionaries

    initiativeOrder = dict(sorted(initiativeOrder.items(), key= lambda item: item[1][0], reverse=True)) #sort dictionary by initiative
    return initiativeOrder

  def select_target(self): #pick target for next action
    for index, creature in enumerate(initiativeOrder.keys()):
      print(f"{dispindex(index)}. {creature} -- {initiativeOrder[creature][CURRENTHP]} HP", end="")# 1. Player 1 -- 50 HP
      if initiativeOrder[creature][CONDITIONS]:
        print(f" -- Conditions: {initiativeOrder[creature][CONDITIONS]}")
      else:
        print("")

    while True:
      target = input("Select your target: ")
      try: #allows user to enter integer
        list(initiativeOrder.keys())[int(target)-1]
        return int(target)
        break
      except:
        try:
          initiativeOrder[target]
          return target
          break
        except:
          input("Please enter a valid target")
    
  def aoe_target(self):
    aoeList = [] 
    for index, creature in enumerate(initiativeOrder.keys()):
      print(f"{index+1}. {creature} -- {initiativeOrder[creature][CURRENTHP]} HP", end="") # 1. Player 1 -- 50 HP
      if initiativeOrder[creature][CONDITIONS]:
        print(f" -- Conditions: {initiativeOrder[creature][CONDITIONS]}")
      else:
        print("")      
    while True:
      aoeTarget = input("Enter the name of your targets one at a time. Press Enter when done: ")
      if aoeTarget != '':
        try: #Lets user enter integer as well as name -- not implimented
         aoeList.append(list(initiativeOrder.keys())[int(aoeTarget)-1])
        except:
          try:
            initiativeOrder[aoeTarget]
            aoeList.append(aoeTarget)
          except:
            input("Please enter a valid target")
      else:
        break
    return aoeList

 #attack target
  def attack(self):
    target = self.select_target()
    damage = int(input("Enter total damage: "))
    try: #lets user use int instead of name
      target = list(initiativeOrder.keys())[target-1]
    except:
      pass
    initiativeOrder[target][CURRENTHP] -= damage
    if initiativeOrder[target][CURRENTHP]<= 0: #removes monster if monster dies
      initiativeOrder.pop(target) #removes from order
      try:
        self.monsters.pop(target) #removes from monster list
      except:
        pass

  def aoe_attack(self):
    aoeList=self.aoe_target()
    for target in aoeList: #loops through aoe list
      initiativeOrder[target][CURRENTHP]-=int(input(f"Enter the damage for {target}: "))
      if initiativeOrder[target][CURRENTHP]<= 0: #removes monster if monster dies
        initiativeOrder.pop(target)
        try:
          self.monsters.pop(target)
        except: 
          pass

  #heal target
  def heal(self):
    target = self.select_target()
    health = int(input("Enter the total health: "))
    try: #lets user use int instead of name
      target = list(initiativeOrder.keys())[target-1]
    except:
      pass
    initiativeOrder[target][CURRENTHP]+= health
    if initiativeOrder[target][CURRENTHP] > initiativeOrder[target][MAXHP]:
      if input("Set hp above max? y/n: ")[0].lower() == 'y':
        pass
      else:
        initiativeOrder[target][CURRENTHP] = initiativeOrder[target][MAXHP]

  def aoe_heal(self):
    aoeList=self.aoe_target()
    health=int(input("Enter total health: ")) #heals all players by amount
    for target in aoeList:
      initiativeOrder[target][CURRENTHP]+=health
      if initiativeOrder[target][CURRENTHP] > initiativeOrder[target][MAXHP]:
        if input("Set hp above max? y/n: ")[0].lower() == 'y':
          pass
        else:
          initiativeOrder[target][CURRENTHP] = initiativeOrder[target][MAXHP]

  #buff/debuff
  def add_condition(self):
    target = self.select_target() 
    try: #lets user use int instead of name
      target = list(initiativeOrder.keys())[target-1]
    except:
      pass
    condition = input("Enter condition: ")
    initiativeOrder[target][CONDITIONS].append(condition) #adds input to condition key
  def aoe_condition(self): 
    aoeList=self.aoe_target()
    condition=input("Enter condition: ")
    for target in aoeList: #loops through aoe targets
      initiativeOrder[target][CONDITIONS].append(condition)

  #remove buff/debuff
  def remove_condition(self): 
    conditionCount = 0
    conditionList = []
    for index, character in enumerate(initiativeOrder.keys()):
      if initiativeOrder[character][CONDITIONS]:
        conditionCount+=1
        conditionList.append(character)
        print(f"{conditionCount}. {character} -- {initiativeOrder[character][CONDITIONS]}") # 1. Player 3 -- Poisoned
    if conditionCount>0: #only display condition if creature has condition
      target = input("Who's condition you would like to remove: ")
      try: #lets user use int instead of name
        target = conditionList[int(target)-1]
      except:
        pass
      if len(initiativeOrder[target][CONDITIONS]) == 1:
        initiativeOrder[target][CONDITIONS]=[]
      else:
        condition = input("Select a condition to remove: ")
        initiativeOrder[target][CONDITIONS].remove(condition)

  def display_initiative(self, t):
    for index, character in enumerate(initiativeOrder.keys()):
      range = len(list(initiativeOrder.keys()))
      charConditions = None
      if list(initiativeOrder.values())[(index+t)%(range)][CONDITIONS]:
          charConditions = list(initiativeOrder.values())[(index+t)%(range)][CONDITIONS]

      if ((index+t)%(range)) == t-1:
        pass
        
      else:
        print(f"""\33[90m
  {list(initiativeOrder.keys())[(index+t)%(range)]}
      HP: {list(initiativeOrder.values())[(index+t)%(range)][CURRENTHP]}
      Conditions: {charConditions}\033[0m""")



  def rotate_initiative(self):
    roundCount = 0
    while True:
      turn = 0
      for index, character in enumerate(initiativeOrder.keys()): #cycles through characters
        if index == 0: roundCount+=1
        turn +=1
        charConditions = None
        while True: #turn lasts until player hits continue
          
          if list(initiativeOrder.values())[index][CONDITIONS]:
            charConditions = list(initiativeOrder.values())[index][CONDITIONS]
            
          os.system('clear')
          print(f"Round {roundCount}\n")
          print(f"{character}'s Turn:") #Player 1
          print(f"HP: {list(initiativeOrder.values())[index][CURRENTHP]}") #HP: XX
          print(f"Conditions: {charConditions}") #Conditions: None
          self.display_initiative(turn)
          while True:
            try:
              action = int(input(f"""
1. Attack
2. Heal
3. Add Buff/Debuff
4. Remove Buff/Debuff                          
5. Continue
"""))
              break
            except:
              input("Please enter a valid integer")
                
          os.system('clear')
          if action != 4 and action != 5: #asks for attack area if not remove buff/debuff
            aoe_check = int(input(
"""1. Single Target
2. AOE
"""))
          os.system('clear')
          #executes function depending on ansers above
          if action == 1 and aoe_check == 1:
            self.attack()
          elif action == 1 and aoe_check == 2:
            self.aoe_attack()
          elif action == 2 and aoe_check == 1:
            self.heal()
          elif action ==2 and aoe_check ==2:
            self.aoe_heal()
          elif action == 3 and aoe_check == 1:
            self.add_condition()
          elif action == 3 and aoe_check == 2:
            self.aoe_condition()
          elif action == 4:
            self.remove_condition()
          elif action == 5:
            break
          else:
            os.system('clear')
            input("Select select a valid number")   
          if not self.monsters: #ends code when monsters die
            break
        if not self.monsters: #ends code when monsters die
          break
      if not self.monsters: #ends code when monsters die
        break