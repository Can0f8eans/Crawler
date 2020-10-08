import random
def join_room_w2e(roomList):
    '''A helper function that joins the generated rooms, linking
    them together to enable traversing the rooms.'''
    for i in range(len(roomList)):
        if i + 1 > len(roomList)-1:
            roomList[i].e = None
        else:
            roomList[i].e = roomList[i+1]
            roomList[i+1].w = roomList[i]
    return roomList
def join_room_n2s(roomList):
    '''Similar in principle to join_room_w2e, this helper 
    function joins the rooms vertically.'''
    for i in (range(len(roomList))):
        for j in reversed(range(len(roomList[i]))):
            if i + 1 > len(roomList)-1:
                roomList[i][j].n = None
            else:
                roomList[i][j].n = roomList[i+1][j]
                roomList[i+1][j].s = roomList[i][j]
        tempList = roomList[i]
    return roomList
def build_grid(width, height):
    '''This function generates a python list which contains all of the 
    rooms. Then using this list, it links together the rooms and 
    returns the origin, aka first or starting room.'''
    roomList = []
    for i in range(height):
        tempList = []
        for j in range(width):
            tempRoom = Room(f"{i},{j}",None,None,None,None)
            tempList.append(tempRoom)
            if j ==0 and i == 0:
                origin = tempRoom
        tempList = join_room_w2e(tempList)
        roomList.append(tempList)
    roomList = join_room_n2s(roomList)
    return origin
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
        self._dead = False
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
            self._roomItem = "Exit"
        else:
            self._roomItem = setItemType(roomItem)
        self._visited = False
    def get_name(self):
        '''Just a function for debugging purposes. Returns the name of
        the current room'''
        return self._name
    def set_name(self,new_name):
        '''Renames the room, possibly to indicate if the room has
        been visited or not.'''
        assert type(new_name) == str
        self._name = new_name
    def collapse_room(self):
        '''sets the exits to the room to None to indicate that the
        room has collapsed and cannot be entered. '''
        self.n = None
        self.s = None
        self.w = None
        self.e = None
    def getRoomItem(self):
        return self._roomItem
    def takeItem(self):
        self._roomItem = None
    def setRoomItem(self, newItem):
        self._roomItem = newItem
    def setVisited(self, player):
        if self._visited is not True:
            self._visited = True
            player.addRoom()
    def delveDeeper(self,curRoom,player):
        if self._roomItem == "Exit":
            chance = random.choice(range(100))
            if chance == 0:
                print("Screams echo silently around you as you delve"
                " deeper into the Dungeon...")
            else:
                print("You delve deeper into the Dungeon...")
            room = build_grid(random.randint(5,10),random.randint(5,10))
            player.addFloor()
            return room
        else:
            print("There is no exit here!")
            return curRoom
class Player:
    def __init__(self, name):
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
        if len(self._inventory) == 1:
            print(f"You have a {self._inventory[0].getWeaponName()} and no food")
        else: 
            print(f"You have a {self._inventory[0].getWeaponName()}, and some {self._inventory[1].getFoodName()}")
    def set_item(self, room):
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
        return self._health
    def setPlayerHealth(self, newHealth):
        self._health = newHealth
    def getStats(self):
        print(f"Player Name:        {self._name}")
        print(f"Health:             {self._health}")
        print(f"Rooms Traversed:    {self._roomTraversed}")
        print(f"Floors Traversed:   {self._floorTraversed}")
        print(f"Monsters Killed:    {self._monstersKilled}")
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
    print(f"A {enemy.getEnemyName()} attacks! You must fight!")
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
    item = room.getRoomItem()
    itemType = type(item)
    if itemType == Food:
        print(f"There are some {item.getFoodName()} on the floor.")
    elif itemType == str:
        print("You feel a cold breeze rush from under your feet. There is an entrance to the "
        "floor below...")
    elif itemType == Weapon:
        print(f"There is a {item.getWeaponName()} on the floor")
    elif itemType == Enemy:
        print(f"There is a dead {item.getEnemyName()} on the floor")
    elif item is None:
        print("There is nothing in the room.")
def move(room, direction, Player):
    if "NORTH" in direction.upper():
        if room.n is not None:
            room = room.n
            room.setVisited(Player)
            print("You go north...")
            return room 
        else:
            print("You cannot move in that direction!")
            return room
    elif "SOUTH" in direction.upper():
        if room.s is not None:
            room = room.s
            room.setVisited(Player)
            print("You go south...")
            return room
        else:
            print("You cannot move in that direction!")
            return room
    elif "WEST" in direction.upper():
        if room.w is not None: 
            room = room.w
            room.setVisited(Player)
            print("You go west...")
            return room
        else:
            print("You cannot move in that direction!")
            return room
    elif "EAST" in direction.upper():
        if room.e is not None:
            room = room.e
            room.setVisited(Player)
            print("You go east... ")
            return room
        else:
            print("You cannot move in that direction!")
            return room
def title():
    print('        dP""b8 88""Yb    db    Yb        dP 88     888888 88""Yb ')
    print('       dP   `" 88__dP   dPYb    Yb  db  dP  88     88__   88__dP ')
    print('       Yb      88"Yb   dP__Yb    YbdPYbdP   88  .o 88""   88"Yb  ')
    print('        YboodP 88  Yb dP""""Yb    YP  YP    88ood8 888888 88  Yb ')
def game_begin():
    isValid = True
    curRoom  = build_grid(random.randint(5,10), random.randint(5,10))
    print("What shall you call yourself, adventurer? ")
    name = input()
    playerChar = Player(name)
    while isValid:
        item = curRoom.getRoomItem()
        if type(item) == Enemy and (item.isDead() is False):
            fight(playerChar, item)
            if playerChar.isDead() == True:
                print()
                playerChar.getStats()
                isValid = False
                break
        else:
            command = input(f"What is your command, {name}?\n")
            if "NORTH" in command.upper() or "SOUTH" in command.upper() or "WEST" in command.upper() or "EAST" in command.upper():
                curRoom = move(curRoom, command.strip(), playerChar)
            elif "INFO" in command.upper():
                info(curRoom)
            elif "STAT" in command.upper():
                playerChar.getStats()
            elif "INVENTORY" in command.upper():
                playerChar.get_inventory()
            elif "EAT" in command.upper():
                playerChar.eat()
            elif "SWAP" in command.upper():
                playerChar.set_item(curRoom)
            elif "HELP" in command.upper():
                print("Available commands: N, S, W, E, Info, Stat, Inventory, Eat, Delve Deeper, and Help")
            elif "DELVE" in command.upper():
                curRoom = curRoom.delveDeeper(curRoom, playerChar)
            elif "EXIT" in command.upper():
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
        command = input("What sayest thou? ")
        command = command.strip()
        print()
        if command.upper() == "EXIT":
            exit()
        elif "ABOUT" in command.upper():
            print("Creator:         Ernie Smith IV - Beans") 
            print("Creation Date:   10/07/2020")
            print("Crawler is a randomly generated dungeon crawler. "
            "Everything is randomly generated, the loot, "
            "the floor size, everything.")
            print("This was just a pet project of mine, just to see if "
            "I could do it!")
        elif "DELVE" in command.upper():
            game_begin()
menu()