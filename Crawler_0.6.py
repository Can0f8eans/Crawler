''''to do:
- work on creating a save file that tracks ur stats
- make map generation'''
import random
import math
def build_map(roomTotal):
    '''This function generates the map to the number of rooms
    specified by the initial value provided. Then, using random,
    specifies if the room will have x many connections or, none at all.
    Finally it will join the rooms together at random.'''
    roomNumber = 0
    direction = ['n','s','e','w']
    origin = Room('origin',None,None,None,None)
    if type(origin.getRoomItem()) == Enemy:
        origin.setRoomItem('Empty')
    maxNum = round(math.sqrt(roomTotal))
    numDoors = random.choice(range(4)) + 1
    specifiedDoors = random.sample(direction,numDoors)
    #print(specifiedDoors)
    for door in specifiedDoors:
            stringMap(origin,door,maxNum, roomNumber)
    origin.addExit(origin)
    return origin
def stringMap(room, dir, maxNum, roomNum):
    if dir == 'n':
        curRoom = room.n = Room(f'{maxNum}, north',None,None,None,None)
        curRoom.s = room
    elif dir == 's':
        curRoom = room.s = Room(f'{maxNum}, south',None,None,None,None)
        curRoom.n = room
    elif dir == 'w':
        curRoom = room.w = Room(f'{maxNum}, west',None,None,None,None)
        curRoom.e = room
    else:
        curRoom = room.e = Room(f'{maxNum}, east',None,None,None,None)
        curRoom.w = room
    roomNum +=1
    #print(roomNum)
    curNum = maxNum - 1
    direction = ['n','s','e','w']
    opposites = {'n':'s','s':'n','e':'w','w':'e'}
    if curNum == 0:
        return 
    else:
        numDoors = random.choice(range(4)) + 1
        specifiedDoors = random.sample(direction,numDoors)
        if opposites[dir] in specifiedDoors:
            #print(opposites[dir])
            specifiedDoors.remove(opposites[dir])

        for door in specifiedDoors:
            stringMap(curRoom,door,curNum,roomNum)
def setItemType(itemTypeNum):
    if itemTypeNum == 0:
        item = Food()
    elif itemTypeNum == 1:
        item = Weapon()
    elif itemTypeNum == 2:
        item = Enemy()
    return item
class Food:
    def __init__(self):
        foodName = ["Biscuits", "Steaks", "Old Rations"]
        self._itemName = random.choice(foodName)
        if self._itemName == "Biscuits":
            self._val = 4
        elif self._itemName == "Steaks":
            self._val = 8
        else:
            self._val = 3
    def getFoodName(self):
        return self._itemName
    def getFoodVal(self):
        return self._val
class Weapon:
    def __init__(self):
        weaponName = ["Sword", "Spear", "Ax", "Knife"]
        self._weapon = random.choice(weaponName)
        if self._weapon == "Sword":
            self._damage = 2
        elif self._weapon == "Spear":
            self._damage = 3
        elif self._weapon == "Ax":
            self._damage = 4
        else:
            self._damage = 1
    def getWeaponName(self):
        return (self._weapon)
    def getWeaponDamage(self):
        return(self._damage)
class Enemy:
    def __init__(self):
        enemyName = ["Slime", "Spider", "Bat", "Skeleton"]
        self._enemy = random.choice(enemyName)
        self._asleep = random.choice([True,False])
        self._dead = False
        self._evaded = False 
        if self._enemy == "Slime":
            self._damage = 1
            self._health = 2
        elif self._enemy == "Spider":
            self._damage = 2
            self._health = 3
        elif self._enemy == "Bat":
            self._damage = 3
            self._health = 4
        else:
            skeletonWeapon = Weapon()
            self._damage = skeletonWeapon.getWeaponDamage()
            self._health = 5
    def hasBeenEvaded(self,status):
        self._evaded = status
    def getEvadeStatus(self):
        return self._evaded
    def attack(self, playerHealth):
        roll = range(20)
        roll = random.choice(roll)
        if roll > 10:
            playerHealth = playerHealth - self._damage
            print(f"The {self._enemy} hits, dealing {self._damage} damage!")
            return playerHealth
        else:
            print(f"The {self._enemy} missed!")
            return playerHealth
    def getEnemyName(self):
        return self._enemy
    def getEnemyHealth(self):
        return self._health
    def setEnemyHealth(self, newHealth):
        self._health = newHealth
    def isAsleep(self):
        return self._asleep
    def awake(self):
        self._asleep = False
    def isDead(self):
        return self._dead 
    def died(self):
        self._dead = True
class Room:
    """This class holds all information about the room, whether it's
    empty, has any loot, has any monsters, or has an exit."""
    def __init__(self, name, n, s, w, e):
        self._name = name
        self.n = n
        self.s = s
        self.w = w
        self.e = e
        roomItem = random.choice([0,1,2,3])
        if roomItem == 3:
            self._roomItem = "Empty"
        else:
            self._roomItem = setItemType(roomItem)
        self._visited = False
    def get_name(self):
        '''Just a function for debugging purposes. Returns the name of
        the current room'''
        return self._name
    def set_name(self,new_name):
        '''Again, this is for debugging, this renames the room,
        possibly to indicate if the room has
        been visited or not.'''
        assert type(new_name) == str
        self._name = new_name
    def collapse_room(self):
        '''sets the exits to the room to None to indicate that the
        room has collapsed and cannot be entered. Still a WIP. '''
        self.n = None
        self.s = None
        self.w = None
        self.e = None
    def getRoomItem(self):
        '''This helper function will return a pointer to the rooms item'''
        return self._roomItem
    def takeItem(self):
        '''This will set the room's item to nothing, for example if you 
        eat food and take the food in the room.'''
        self._roomItem = 'Empty'
    def setRoomItem(self, newItem):
        '''This is utilized by the swap function to put in the other item'''
        self._roomItem = newItem
    def setVisited(self, player):
        '''This is for the purpose of tracking player statistics.'''
        if self._visited is not True:
            self._visited = True
            player.addRoom()
    def getVisited(self):
        '''This function helps other functions understand if 
        you've been in that room before.'''
        return self._visited
    def delveDeeper(self,curRoom,player):
        '''Ah yes, the star of the show here! This is the 
        function that calls the move function and generates
        a new floor for the player, as well as tracks his 
        stats. Will return an 'error' if the player tries
        to go to the next floor from a room where there is no exit.'''
        if self._roomItem == "Exit":
            chance = random.choice(range(100))
            if chance == 0:
                print("Screams echo silently around you as you delve"
                " deeper into the Dungeon...\n")
            else:
                print("You delve deeper into the Dungeon...\n")
            room = build_map(random.randint(5,10))
            player.addFloor()
            return room
        else:
            print("There is no exit here!\n")
            return curRoom
    def addExit(self,room):
        '''After a floor has been generated, this function
        will go through and add an exit. There is a chance that there
        isn't an exit to put an untimely end to a player's run.'''
        if random.choice(range(3)) == 0:
            if room._name != 'origin':
                room._roomItem = 'Exit'
            #print("There is now an exit")
            return
        else:
            availableDir = []
            if room.n != None:
                availableDir.append('n')
            elif room.s != None:
                availableDir.append('s')
            elif room.w != None:
                availableDir.append('w')
            elif room.e != None:
                availableDir.append('e')
            for item in availableDir:
                if item == 'n':
                    room.addExit(room.n)
                elif item == 's':
                    room.addExit(room.s)
                elif item == 'w':
                    room.addExit(room.w)
                elif item == 'e':
                    room.addExit(room.e)
    def getAvailRooms(self):
        '''this is a helper function that helps the 
        info function understand what doors are available to
        traverse.'''
        avaialbleDoors = []
        if self.n != None:
            avaialbleDoors.append('n')
        if self.s != None:
            avaialbleDoors.append('s')
        if self.w != None:
            avaialbleDoors.append('w')
        if self.e != None:
            avaialbleDoors.append('e')
        return avaialbleDoors
class Player:
    '''This is the player class that contains
    all valueable information and functions
    that make the game happen.'''
    def __init__(self, name):
        '''The init function, pretty self explanatory. By calling the constructor, 
        a player is given a weapon and food, and the game begins to track 
        his statistics. '''
        self._name = str(name)
        weapon = Weapon()
        startingFood = Food()
        self._health = 15
        self._inventory = [weapon, startingFood]
        self._roomTraversed = 1
        self._floorTraversed = 0
        self._dead = False
        self._monstersKilled = 0
    def attack(self, enemyHealth):
        '''The attack function uses a d20 to determine whether or
        not the player lands a blow.'''
        roll = range(20)
        roll = random.choice(roll)
        if roll > 10:
            print(f"You hit, dealing {self._inventory[0].getWeaponDamage()} damage!")
            enemyHealth = enemyHealth - self._inventory[0].getWeaponDamage()
            return enemyHealth
        else:
            print("You missed!")
            return enemyHealth
    def get_inventory(self):
        '''Returns the inventory of the player'''
        if len(self._inventory) == 1:
            print(f"You have a {self._inventory[0].getWeaponName()} and no food!")
        else: 
            print(f"You have a {self._inventory[0].getWeaponName()}, and some {self._inventory[1].getFoodName()}")
    def set_item(self, room):
        '''This is the swap function.'''
        item = room.getRoomItem()
        if type(item) == Food:
            if len(self._inventory) == 1:
                print(f"Added {item.getFoodName()} to your inventory")
                self._inventory.append(item)
                room.takeItem()
            else:
                print (f"Would you like to swap your {self._inventory[1].getFoodName()} with {item.getFoodName()}?")
                print("You can only have one item of food on you at a time!"
                " So choose wisely!")
                temp = input("(Y/N?) ")
                if temp.upper() == "Y" or temp.upper() == "YES":
                    tempRoomItem = self._inventory[1]
                    self._inventory[1] = item
                    room.setRoomItem(tempRoomItem)
                    print(f"You take the {self._inventory[1].getFoodName()} into your inventory.")
                else:
                    print("You do nothing.")
        elif type(item) == Weapon:
            print (f"Would you like to swap your {self._inventory[0].getWeaponName()} with "
            f"{item.getWeaponName()}?")
            print("You can only have one weapon on you at a time!"
            " So choose wisely!")
            temp = input("(Y/N?) ")
            if temp.upper() == 'Y' or temp.upper() == 'YES':
                tempRoomItem = self._inventory[0]
                self._inventory[0] = item
                room.setRoomItem(tempRoomItem)
                print(f"You take the {self._inventory[0].getWeaponName()} and drop your {tempRoomItem.getWeaponName()}")
            else:
                print("You do nothing")
    def eat(self):
        '''This function is how the player eats and regains
        health.'''
        if len(self._inventory) == 1:
            print("You cannot eat as you do not have any food!")
        else:
            if self._health == 15:
                print ("You cannot eat as your health is full")
            else:
                newHealth = self._health + self._inventory[1].getFoodVal()
                if newHealth > 15:
                    diff = newHealth - 15
                    self._health = 15
                    print(f"You gained {diff}hp.")
                    self._inventory.pop()
                elif newHealth == 15 or newHealth < 15:
                    self._health = newHealth
                    print(f"You gained {self._inventory[1].getFoodVal()}hp.")
                    self._inventory.pop()
    def getPlayerHealth(self):
        '''returns the player health to determine
        whether or not the player has died'''
        return self._health
    def setPlayerHealth(self, newHealth):
        '''This function is how the game tracks damage
        sustained through combat.'''
        self._health = newHealth
    def getStats(self):
        '''This is the stat function'''
        print(f"Player Name:        {self._name}")
        print(f"Health:             {self._health}")
        print(f"Rooms Traversed:    {self._roomTraversed}")
        print(f"Floors Traversed:   {self._floorTraversed}")
        print(f"Monsters Killed:    {self._monstersKilled}")
    '''The following functions are for the sake
    of tracking player statistics.'''
    def addRoom(self):
        self._roomTraversed +=1
    def addFloor(self):
        self._floorTraversed +=1
    def isDead(self):
        return self._dead
    def died(self):
        self._dead = True
    def addMonster(self):
        self._monstersKilled +=1
def fight(player,enemy):

    if enemy.isAsleep()==True:
        ans = input(f'A {enemy.getEnemyName()} is in the room, but asleep. Will you fight it?\n')
        if 'N' in ans.upper():
            print('you choose not to fight, you must leave quickly before it wakes.')
            enemy.hasBeenEvaded(True)
        else:
            print(f"You attack the {enemy.getEnemyName()}")
            enemyHealth = enemy.getEnemyHealth()
            playerHealth = player.getPlayerHealth() 
            while enemyHealth> 0 and playerHealth > 0:
                coin = random.choice(range(2))
                if coin == 0:
                    print(f"The {enemy.getEnemyName()} Attacks!")
                    player.setPlayerHealth(enemy.attack(player.getPlayerHealth()))
                else:
                    print(f"You attack the {enemy.getEnemyName()}!")
                    enemy.setEnemyHealth(player.attack(enemy.getEnemyHealth()))
                enemyHealth = enemy.getEnemyHealth()
                playerHealth = player.getPlayerHealth()  
            if enemyHealth <= 0:
                print(f"You killed the {enemy.getEnemyName()}!")
                player.addMonster()
                enemy.died()
            elif playerHealth <= 0:
                print("You died!")
                print("Game Over!")
                player.died()
    else:
        print(f"A {enemy.getEnemyName()} attacks!\nWill you run or fight?")
        temp = input("Run or fight? (R/F)\n")
        d10 = random.choice(range(10))
        if 'R' in temp.upper() and d10 > 4:
            enemy.hasBeenEvaded(True)
            print("You successfully run from the fight! You must leave quickly before it strikes again!")
        elif d10 <= 4 or 'F' in temp.upper():
            if 'R' in temp.upper():
                print(f"You tried running but the {enemy.getEnemyName()} won't let you escape")
            enemyHealth = enemy.getEnemyHealth()
            playerHealth = player.getPlayerHealth() 
            while enemyHealth> 0 and playerHealth > 0:
                coin = random.choice(range(2))
                if coin == 0:
                    print(f"The {enemy.getEnemyName()} Attacks!")
                    player.setPlayerHealth(enemy.attack(player.getPlayerHealth()))
                else:
                    print(f"You attack the {enemy.getEnemyName()}!")
                    enemy.setEnemyHealth(player.attack(enemy.getEnemyHealth()))
                enemyHealth = enemy.getEnemyHealth()
                playerHealth = player.getPlayerHealth()  
            if enemyHealth <= 0:
                print(f"You killed the {enemy.getEnemyName()}!")
                player.addMonster()
                enemy.died()
            elif playerHealth <= 0:
                print("You died!")
                print("Game Over!")
                player.died()
def info(room):
    direction = {'n':'north','s':'south','w':'west','e':'east'}
    numDoors = room.getAvailRooms()
    item = room.getRoomItem()
    itemType = type(item)
    if itemType == Food:
        print(f"There are some {item.getFoodName()} on the floor.")
    elif item == 'Exit' and itemType == str:
        print("You feel a cold breeze rush from under your feet.") 
        print("There is an entrance to the floor below...")
    elif item == 'Empty' and itemType == str:
        print('The room is empty...')
    elif itemType == Weapon:
        print(f"There is a {item.getWeaponName()} on the floor.")
    elif itemType == Enemy:
        if item.isAsleep():
            print(f"There is a sleeping {item.getEnemyName()}.")
        if item.isAsleep() is False and item.getEvadeStatus():
            print(f"The {item.getEnemyName()} is looking for you. Go quickly!")
        if item.isDead():
            print(f"There is a dead {item.getEnemyName()} on the floor.")
    if len(numDoors) == 1:
        print (f'There is a door to the {direction[numDoors[0]]}')
    else:
        string = 'There are doors to'
        for i in range(len(numDoors)):
            if i + 1 == len(numDoors): 
                string = string + f" and the {direction[numDoors[i]]}."
            else:
                string = string + f" the {direction[numDoors[i]]},"
        print(string)
def map():
    print('You look at your map...')
def move(room, direction, Player):
    enemy = None
    if type(room.getRoomItem()) == Enemy:
        enemy = room.getRoomItem()
        if enemy.isAsleep():
            enemy.awake()
        enemy.hasBeenEvaded(False)
    if "N" in direction.upper():
        if room.n is not None:
            room.setVisited(Player)
            room = room.n
            print("You go north...")
            return room 
        else:
            print("You cannot move in that direction!\n")
            return room
    elif "SO" in direction.upper():
        if room.s is not None:
            room.setVisited(Player)
            room = room.s
            print("You go south...")
            return room
        else:
            print("You cannot move in that direction!\n")
            return room
    elif "W" in direction.upper():
        if room.w is not None: 
            room.setVisited(Player)
            room = room.w
            print("You go west...")
            return room
        else:
            print("You cannot move in that direction!\n")
            return room
    elif "EA" in direction.upper():
        if room.e is not None:
            room.setVisited(Player)
            room = room.e
            print("You go east...")
            return room
        else:
            print("You cannot move in that direction!\n")
            return room
def title():
    print('        dP""b8  88""Yb     db    Yb        dP  88      888888  88""Yb ')
    print('       dP   `"  88__dP    dPYb    Yb  db  dP   88      88__    88__dP ')
    print('       Yb       88"Yb    dP__Yb    YbdPYbdP    88  .o  88""    88"Yb  ')
    print('        YboodP  88  Yb  dP""""Yb    YP  YP     88ood8  888888  88  Yb ')
def game_begin():
    isValid = True
    curRoom  = build_map(random.randint(5,10))
    print("What shall you call yourself, adventurer?")
    name = input()
    playerChar = Player(name)
    while isValid:
        if curRoom != None:
            item = curRoom.getRoomItem()
        if type(item) == Enemy and (item.isDead() is False) and item.getEvadeStatus() is False:
                fight(playerChar, item)
                if playerChar.isDead() == True:
                    print()
                    playerChar.getStats()
                    isValid = False
                    break
        else:
            command = input(f"What is your command, {name}?\n")
            if "N" in command[0].upper() or "SO" in command[0:2].upper() or "W" in command[0].upper() or "EA" in command[0:2].upper():

                curRoom = move(curRoom, command.strip(), playerChar)
                if curRoom != None:
                    if curRoom.getVisited():
                        print("You have been here before...")
            elif "INF" in command.upper():
                info(curRoom)
            elif "ST" in command.upper():
                playerChar.getStats()
            elif "INV" in command.upper():
                playerChar.get_inventory()
            elif "EAT" in command.upper():
                playerChar.eat()
            elif "SW" in command.upper():
                playerChar.set_item(curRoom)
            elif "H" in command.upper():
                print("Available commands: N, S, W, E, Info, Stat, Inventory, Eat, Delve Deeper, Exit, and Help")
                input()
            elif "DE" in command.upper():
                curRoom = curRoom.delveDeeper(curRoom, playerChar)
            elif "EX" in command.upper():
                break
            else:
                print("Invalid command")
def menu():
    while True:
        print()
        print("Welcome to...")
        print()
        title()
        print('\n')
        print ("\t\t\t      Delve Deeper...")
        print ("\t\t\t       About Crawler")
        print ("\t\t\t           Exit")
        print ("\n")
        command = input("What say ye? ")
        command = command.strip()
        print()
        if 'EX' in command.upper():
            exit()
        elif "AB" in command.upper():
            print("Creator:         Ernie Smith IV - Beans") 
            print("Creation Date:   10/07/2020")
            print("Latest update: 0.6 - 11/15/2022")
            print("Crawler is a randomly generated dungeon crawler. "
            "Everything is randomly generated, the loot, "
            "the floor size, everything.")
            print("This was just a pet project of mine, just to see if "
            "I could do it!")
            input("[Exit]")
        elif "DE" in command.upper():
            print("You enter the dungeon...")
            game_begin()
menu()
