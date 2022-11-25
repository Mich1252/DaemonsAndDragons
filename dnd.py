#Author: Andrew Cohn
#DESC: DND Dm Console. Allows the DM to add players and enemies, and to keep track of their health, as well as various other attributes.
from random import randint as rand
import re
import json
def main():   
    #Giant dictonary containing all the commands. Used to print help menu, and to check in if the user input is valid.
    global commands 
    commands = {
    'add':"Adds players or enemies to the game!\n   Parameters-\n    p or e, for player or enemy\n   number of players to add",
    'remove':'Removes players or enemies from the game!\n   Parameters-\n    p or e, for player or enemy\n   names of players/enemies to remove',
    'status':"Gathers the current hp of a player or enemy\n     Parameters-\n    p or e, for player or enemy\n    name of player or enemy",
    'attack':"Deals damage. \n    Parameters-\n    target, which can be a player or enemy, and should be a string\n    victim,which can be a player or enemy, and should be a string",
    'help':"Reads this list\n    Parameters-\n    None",
    'exit':"Saves and exits!\n  Parameters-\n    filename to save to (has to end in .json)",
    'save':"Saves and exits!\n  Parameters-\n    filename to save to (has to end in .json)",
    'list': "Lists all the players and enemies in the game\n    Parameters-\n    None",
    'load': "Loads the data from another .json. Currently broken. Loading only works when the program is first run for now. TODO.\n    Parameters-\n    filename to load from",
    'rollinit':"Rolls initiative for all players and enemies.\n    Parameters-\n    None",
    'printinit':"Prints the initiative order.\n    Parameters-\n    None",
    }
    
    usrInput = ['']
    #These globals are used to store the players and enemies, as dictionaries with nested dictionaries.
    global players
    players = {}
    global enemies
    enemies = {}   
    #Decides to load data from a file or continue with a new game.
    decision = ''
    while decision.lower() not in ['y','n']:
        decision = input("Would you like to load a previous game? (y/n)\n")
    if decision.lower() == 'y':
        file = ""
        while file[-5:] != '.json':
            file = input("Enter the filename to load from (must end in .json):\n")
        players, enemies = load(players,enemies,file)
        requestInput()
    else:
        requestInput() 
    #Send the input to a function which decides which other function to pipe it to
    controlFlow(usrInput,players,enemies)
def controlFlow(usrInput,players,enemies):
    """
    This function is responsible for handling the control flow- essentially, it reads the input,
    parses the command from the input, calls the appopriate function, then asks for more input.
        Parameters- 
            usrInput: a list containing the user input, split by spaces.
            players: a dictionary containing the players in the game.
            enemies: a dictionary containing the enemies in the game.
    """
    
    #Help Command!
    if usrInput[0] == 'help':
        help()
        requestInput()
    
    #Add Command!
    if usrInput[0] == 'add' and len(usrInput) == 3:
        if str(usrInput[1])[0].lower() == 'p':
            addPlayer(players,int(usrInput[2]))
        elif str(usrInput[1])[0].lower() == 'e':
            addEnemy(enemies,int(usrInput[2]))
    elif usrInput[0] == 'add' and  not len(usrInput) == 3:
        print("Missing parameter(s) team and player count.")
        requestInput()
    #Status Command!
    if usrInput[0] == 'status':
        if str(usrInput[1])[0].lower() == 'p':
            if usrInput[2] in players:
                status(players,usrInput[1],usrInput[2])
                requestInput()
            else:
                print("Player not found.")
                requestInput()
        elif str(usrInput[1])[0].lower() == 'e':
            if usrInput[2] in enemies:
                status(enemies,usrInput[1],usrInput[2])
                requestInput()
            else:
                print("Enemy not found.")
                requestInput()
        else:
            print("Invalid input for team")
            requestInput()
    else:
        pass
    #Load! Currently broken. Only works when main is first run. TODO.
    if usrInput[0] == 'load':
        file = usrInput[1]
        players, enemies = load(players,enemies,file)
        requestInput()
    else:
        pass

    #Save and exit! They both call the same function.
    if (str(usrInput[0]).lower() == 'save' or str(usrInput[0]).lower() == 'exit') and len(usrInput) == 2:
        file = usrInput[1]
        if file[-5:] == '.json':
            save(players,enemies,file)
        else:
            print("Invalid file type. (Must be .json")
        if usrInput[0] == 'save':
            requestInput()
        else:
            print("Goodbye!")
            exit()
    elif (usrInput[0] == 'save' or usrInput[0] == 'exit') and (not len(usrInput) == 2):
        print("missing parameter: filename")
        requestInput()
    #List command!
    if usrInput[0] == 'list':
        listNames(players,enemies)
        requestInput()

    #Remove command!
    if usrInput[0] == 'remove':
        #If the user wants to remove a player
        if str(usrInput[1])[0].lower() == 'p':
            #Remove all the players in the list
            for i in range(len(usrInput)-2):
                if usrInput[i+2] in players:
                    del players[usrInput[i+2]]
                else:
                    print("Player "+str(usrInput[i+2])+" not found.")
        #If the user wants to remove an enemy
        elif str(usrInput[1])[0].lower() == 'e':
            #Remove all the enemies in the list
            for i in range(len(usrInput)-2):
                if usrInput[i+2] in enemies:
                    del enemies[usrInput[i+2]]
                else:
                    print("Enemy "+str(usrInput[i+2])+" not found.")
        else:
            print("Invalid input for team")
        requestInput()
    #attack command!
    if usrInput[0] == 'attack':
        attack(usrInput[1],usrInput[2])
        requestInput()
    #Roll init!
    if usrInput[0] == 'rollinit':
        initDict = {}
        for name in players.keys():
            initDict[name] = rand(1,20)+int(players[name]['dexterity'])
        for name in enemies.keys():
            initDict[name] = rand(1,20)+int(enemies[name]['dexterity'])
        global turnOrder 
        turnOrder = sorted(initDict.items(), key=lambda x: x[1], reverse=True)
        print("Turn order:")
        for i in turnOrder:
            print(str(i[0])+": "+str(i[1]))
        requestInput()
    if usrInput[0] == 'printinit':
        print("Turn order:")
        for i in turnOrder:
            print(str(i[0])+": "+str(i[1]))
        requestInput()

        
def attack(attacker,victim):
    """
    This function deals damage to players and enemies.
    It also processes the damage string to determine if the damage should be rolled or not.
    Parameters-
        attacker: the name of the attacker
        victim: the name of the victim
    """
    
    #If the player is hitting an enemy, ask for damage, and subtract from enemy HP.
    if attacker in players:
        damage = int(input("Enter the int damage to deal to the enemy:\n"))
        enemies[victim]['curHp'] -= damage
    #If the enemy is attacking:
    elif attacker in enemies:    
        #Does the enemy use ranged or melee? Ask the user.    
            attack = ""
            while attack not in {'r','m'}:
                attack = input("ranged or melee? (r/m)\n")
            
            #If the player hits with a ranged move:
            if attack == 'r' and (rand(1,20)+enemies[attacker]['rAttackBonus']) >= int(players[victim]['ac']):
                #parse the damage string to determine what to roll
                damageInt = 0
                damageList = re.split("d|\+",enemies[attacker]['mAttack'])
                numDice = int(damageList[0])
                diceType = int(damageList[1])
                modifier = int(damageList[2])
                #Casino!
                for i in range(numDice):
                    damageInt += rand(1,diceType)
                players[victim]['curHp'] -= damageInt+modifier
                print("Hit for "+str(damageInt+modifier)+"!")
                print(victim+" has "+str(players[victim]['curHp'])+" HP left.")
            #If ranged attack misses:
            elif attack == 'r' and (rand(1,20)+int(enemies[attacker]['rAttackBonus'])) <= int(players[victim]['ac']):
                print("Ranged attack missed!")
            
            #If the player hits with a melee move:
            elif attack == 'm' and (rand(1,20)+int(enemies[attacker]['mAttackBonus'])) >= int(players[victim]['ac']):
                #Parse the dice string to determine what to roll
                damageInt = 0
                damageList = re.split("d|\+",enemies[attacker]['mAttack'])
                numDice = int(damageList[0])
                diceType = int(damageList[1])
                modifier = int(damageList[2])
                #Cha-Ching!
                for i in range(numDice):
                    damageInt += rand(1,diceType)
                players[victim]['curHp'] -= damageInt+modifier
                print("Hit for "+str(damageInt+modifier)+"!")
                print(victim+" has "+str(players[victim]['curHp'])+" HP left.")
            #If melee attack misses:
            elif attack == 'm' and (rand(1,20)+int(enemies[attacker]['mAttackBonus'])) <= int(players[victim]['ac']):
                print("Melee attack missed!")
            #If God has left this accursed realm:
            else:
                print("This is a failsafe and should literally never execute.")




def help():
    """
    Prints the help menu.
    """
    for command,desc in commands.items():
        print(command+":\n")
        print(desc+"\n")


def listNames(players,enemies):
    """
    Prints the names of all the players and enemies in the game.
        Parameters- Players, the same dict as before
                    Enemies, the same dict as before
    """
    print("Players:")
    counter = 1
    for name in players.keys():
        print('Player '+str(counter)+": "+name)
    print("Enemies:")
    for name in enemies:
        print(name)

def requestInput():
    """
    Requests input from the user and returns it. If the first word of the input is not a valid command, it asks for input again. Sends that to the control flow function.
    """
    usrInput = [' ']
    while usrInput[0].lower() not in commands:
        console = input("Enter a command: ").lower()
        usrInput = console.split()
    controlFlow(console.split(' '),players,enemies)

def addPlayer(players,pCount):
    """
    This function adds players and their states to the players dict. The players dict is a dictionary with nested dictionaries. The nested dictionaries contain the player's name as a key,and stat attributes as values.
    Parameters-
        players: the players dict
        pCount: the number of players to add
    """
   
    casters = {'bard','cleric','druid','paliden','sorcerer','wizard','artificer','warlock'}
    for i in range(pCount):
        attributes = {}
        name = input("What is the name of player " + str(i+1) + "?\n").lower()
        attributes["class"] = input("What is the class of player " + str(i+1) + "?\n")
        attributes["level"] = int(input("What is the level of player " + str(i+1) + "?\n"))
        attributes["charisma"] = int(input("What is the charisma of player " + str(i+1) + "?\n"))
        attributes["strength"] = int(input("What is the strength bonus of player " + str(i+1) + "?\n"))
        attributes["dexterity"] = int(input("What is the dexterity bonus of player " + str(i+1) + "?\n"))
        attributes["constitution"] = int(input("What is the constitution bonus of player " + str(i+1) + "?\n"))
        attributes["intelligence"] = int(input("What is the intelligence bonus of player " + str(i+1) + "?\n"))
        attributes["wisdom"] = int(input("What is the wisdom of player " + str(i+1) + "?\n"))
        attributes['hp'] = int(input('What is the max HP of player ' + str(i+1) + '?\n'))
        attributes['ac'] = int(input('What is the AC of player ' + str(i+1) + '?\n'))
        attributes['curHp'] = int(input('What is the current HP of player ' + str(i+1) + '?\n'))
        attributes['proficency'] = int(input('What is the proficency bonus of player ' + str(i+1) + '?\n'))
        if attributes['class'] in casters:
            for i in range(1,int(input("How many spells would you like to add?\n"))):
                spells = set()
                spells.add(input("Enter the name of the the spell.\n"))
            attributes['spellSlots'] = input('How many total spell slots for player ' + str(i+1) + '?\n')
            attributes['spells'] = spells
        players[name] = attributes
    requestInput()
    

def status(players,team,name):
    """
    Prints the status of a player or enemy.
    Will tell if an enemy is bloodied.
        Parameters:
            players: the players dict
            team: the team of the player or enemy
            name: the name of the player or enemy
    """
    #Is player?
    if str(team)[0].lower() == 'p':
        if name in players:
            print(name+" has " + str(players[name]['curHp']) +' hit points remaining.')
        else:
            print("That player does not exist.")
    #Is enemy?
    elif str(team)[0].lower() == 'e':
        if name in enemies:
            hp_percent = int(enemies[name]['curHp'])/int(enemies[name]['hp'])
            isBloodied = False
            print(name+" has " + str(players[name]['ac']) +' armour class.')
            print(name+" has " + str(players[name]['curHp']) +' hit points remaining.')
            if hp_percent <= .5:
                isBloodied = True
            if isBloodied:
                print(name + " is bloodied.")
            else:
                print(name + " is not bloodied.")
            console = ''
        else:
            print("That enemy does not exist.")
            console = ''

def load(players,enemies,file):
    """
    This code fucking blows. I want to be able to call load at any time, but it only works when the program is first run. I don't know why. I'm going to have to look into it.
    """
    fileObject = open(file,'r').readlines()
    players = json.loads(fileObject[0])
    enemies = json.loads(fileObject[1])
    print("Loading successful!")
    return players,enemies
def save(players,enemies,file):
    """
    This is the code that saves the game. It saves the players and enemies dicts to a file.
        Parameters:
            file: the file to save to (string)
            players: the players dict
            enemies: the enemies dict
    """
    fileObject = open(file,'w')
    fileObject.write(json.dumps(players)+"\n")
    fileObject.write(json.dumps(enemies))
    fileObject.close()
    print('Saved!')

    

def addEnemy(enemies,eCount):
    """
    Adds an enemy to the enemies dictionary. The enemies dictionary is a dictionary with nested dictionaries. The nested dictionaries contain the enemy's name as a key,and stat attributes as values.
    The enemy is added to the dictionary with the name as the key and the attributes as the value.
        Parameters:
            enemies: the enemies dict
            eCount: The number of enemies to add
    """
    """
    This block of code stores a few premade enemies in a dictionary. That way I can spam add Kobolds or Goblins or whatever.
    """
    ###PREMADE ENEMIES BEGIN###
    premades ={
        'goblin':{
            'hp':7,
            'ac':15,
            'curHp':7,
            'strength':-1,
            'dexterity':2,
            'constitution':0,
            'intelligence':0,
            'wisdom':-1,
            'charisma':-1,
            'mAttack':'1d6+2',
            'mAttackBonus':4,
            'rAttack':'1d6+2',
            'rAttackBonus':4
        },
        'kobold':{
            'hp':5,
            'ac':12,
            'curHp':5,
            'strength':-1,
            'dexterity':2,
            'constitution':-1,
            'intelligence':-1,
            'wisdom':-1,
            'charisma':-1,
            'mAttack':'1d4+2',
            'mAttackBonus':4,
            'rAttack':'1d4+2',
            'rAttackBonus':4
        },
    
    ###PREMADE ENEMIES END###
    }

   

    if input("Would you like to add a premade enemy(s)? (y/n)\n").lower() == 'y':
        premade = input("Which premade enemy would you like to add?\n")
        if premade.lower() in premades:
            for counter in range(1,eCount+1):
                enemies[premade+str(counter)] = premades[premade]
        else:
            print("That enemy does not exist.")
    else:
        for i in range(eCount):
            attributes = {}
            name = input("What is the name of enemy " + str(i+1) + "?\n")
            attributes["hp"] = int(input("What is the HP of enemy " + str(i+1) + "?\n"))
            attributes["curHp"] = int(input("What is the current HP of enemy " + str(i+1) + "?\n"))
            attributes["ac"] = int(input("What is the AC of enemy " + str(i+1) + "?\n"))
            attributes["strength"] = int(input("What is the strength bonus of enemy " + str(i+1) + "?\n"))
            attributes["dexterity"] = int(input("What is the dexterity bonus of enemy " + str(i+1) + "?\n"))
            attributes["constitution"] = int(input("What is the constitution bonus of enemy " + str(i+1) + "?\n"))
            attributes["intelligence"] = int(input("What is the intelligence bonus of enemy " + str(i+1) + "?\n"))
            attributes["wisdom"] = int(input("What is the wisdom bonus of enemy " + str(i+1) + "?\n"))
            attributes["charisma"] = int(input("What is the charisma bonus of enemy " + str(i+1) + "?\n"))
            attributes["mAttack"] = input("What is the melee attack of enemy " + str(i+1) + "?\n(Must be in the form adb+c, where a is the number of dice, b is the dice, and c is the modifier\n")
            attributes["mAttackBonus"] = int(input("What is the melee attack bonus of enemy " + str(i+1) + "?\n"))
            attributes["rAttack"] = input("What is the ranged attack of enemy " + str(i+1) + "?\nMust be in the form adb+c, where a is the number of dice, b is the dice, and c is the modifier\n")
            attributes["rAttackBonus"] = int(input("What is the ranged attack bonus of enemy " + str(i+1) + "?\n"))
            enemies[name] = attributes
    requestInput()
main()