import random

def direction_checker(currentX, currentY,targetX,targetY):
    if(targetX == currentX):
        if currentY<targetY:
            return "south"
        else:
            return "north"
    elif currentY == targetY:
        if currentX<targetX:
            return "east"
        else:
            return "west"
    else:
        if currentX>targetX:
            if currentY>targetY:
                return "northwest"
            else:
                return "southwest"
        else:
            if currentY>targetY:
                return "northeast"
            else:
                return "southeast"



#version = int(input("Which version would you like to play? 1 or 2? "))
version = 2

if version == 2:
    # Number key:
    # Type 1 is dragon
    # Type 2 is orc
    # Type 3 is rabbit
    # Type 5 is unicorn
    # Type 11 is mountain
    # Type 12 is lake

    # Placement of treasure
    fieldSize=40
    targetX = random.randint(-fieldSize//2,fieldSize//2)
    targetY = random.randint(-fieldSize//2,fieldSize//2)

    # Placement of terrain features
    lakeX = (-1)**(random.randint(1,2))*(random.randint(3,8))
    lakeY = (-1)**(random.randint(1,2))*(random.randint(3,8))

    mountainX = targetX
    mountainY= targetY
    while(abs(mountainX-targetX)<=3 and abs(mountainY-targetY)<=3) or (abs(mountainX-lakeX)<=2 and abs(mountainY-lakeY)<=2):
        mountainX = (-1)**(random.randint(1,2))*(random.randint(10,20))
        mountainY = (-1)**(random.randint(1,2))*(random.randint(10,20))

    # Placement of enemies
    dragonX = 0
    dragonY = 0
    while(abs(dragonX)<=3 and abs(dragonY)<=3) or (abs(dragonX-lakeX)<=2 and abs(dragonY-lakeY)<=2):
        dragonX = 0
        dragonY = 0
        dragonX = targetX + (-1)**(random.randint(1,2))*(random.randint(3,6))
        dragonY = targetY + (-1)**(random.randint(1,2))*(random.randint(3,6))


    orc1X = (-1)**(random.randint(1,2))*(random.randint(2,15))
    orc1Y = (-1)**(random.randint(1,2))*(random.randint(2,15))

    orc2X = (-1)**(random.randint(1,2))*(random.randint(2,15))
    orc2Y = (-1)**(random.randint(1,2))*(random.randint(2,15))

    orc3X = (-1)**(random.randint(1,2))*(random.randint(2,15))
    orc3Y = (-1)**(random.randint(1,2))*(random.randint(2,15))

    orc4X = (-1)**(random.randint(1,2))*(random.randint(2,15))
    orc4Y = (-1)**(random.randint(1,2))*(random.randint(2,15))

    orc5X = (-1)**(random.randint(1,2))*(random.randint(2,15))
    orc5Y = (-1)**(random.randint(1,2))*(random.randint(2,15))

    # slightly more helpful NPCs
    unicornX = (-1)**(random.randint(1,2))*(random.randint(10,15))
    unicornY = (-1)**(random.randint(1,2))*(random.randint(10,15))


    guessX = 0
    guessY = 0
    displayX = 0
    displayY = 0
    stepNumber = 0
    longitude = "W"
    latitude = "N"

    health = 3
    weapon = False
    palantir = False
    unicornSeen = False

    finished = False

    def check_for_item(type,thingX,thingY):
        damaged = 0
        if type == 3:
            rabbitChance = random.randint(1,100)
            if rabbitChance<=25:
                THATrabbitChance = random.randint(1,100)
                if weapon == False:
                    if THATrabbitChance <10:
                        damaged = -2
                        print(" You have startled a harmless-seeming rabbit. However, this rabbit is not harmless. \n It is THAT RABBIT from THAT MOVIE. \n When it is finished with you, both your pride and your health are in the dust.")
                    else:
                        print(" You have startled a harmless-seeming rabbit. It runs off into the bushes.")
                if weapon == True:
                    if THATrabbitChance <25:
                        damaged = -2
                        print(" You have startled a harmless-seeming rabbit. However, this rabbit is not harmless. \n It is THAT RABBIT from THAT MOVIE. Swords are of no avail.\n When it is finished with you, both your pride and your health are in the dust.")
                    else:
                        print(" You have startled a harmless-seeming rabbit. It runs off into the bushes.")
        elif(abs(thingX-guessX)<=5 and abs(thingY-guessY)<=5):
            if type == 0: #TREASURE
                if thingX == guessX and thingY == guessY: #Found range
                    if palantir == False:
                        print("Somehow, without any guidance, you stumbled upon the treasure. You thus have the most important quality of an adventurer: luck.")
                    print(" Congratulations! You have found the treasure and proved yourself an adventurer! \n Just one question: what are you going to do now?")
                    print(" (If you would like to play again, type, 'python Quest_for_Ynond.py')\n")
                    finished = True
                elif abs(thingX-guessX)<=1 and abs(thingY-guessY)<=1:# Sight range
                    print(" You see a heap of gold, jewels, and various other valuable items on the ground directly to your {0}. \n Your adventurer senses tell you that this is treasure. Someone really should be guarding it better.".format(direction_checker(guessX,guessY,thingX,thingY)))
            if type == 1: #DRAGON
                if abs(thingX-guessX)<=1 and abs(thingY-guessY)<=1:# Devoured Range
                    print(" You have gotten too close to a dragon. You are crunchy and taste good with ketchup. \n You have been devoured.")
                    damaged =-3
                elif abs(thingX-guessX)<=2 and abs(thingY-guessY)<=2: #Fire Range
                    print(" There is a dragon immediately to your {0}. It set your pants on fire.".format(direction_checker(guessX,guessY,thingX,thingY)))
                    if((health-1)<=0):
                        finished = True
                    damaged = -1
                elif abs(thingX-guessX)<=3 and abs(thingY-guessY)<=3: #Sight Range
                    print(" You see a dragon nearby to your {0}. Your adventurer senses tell you that treasure is likely nearby. \n Your adventurer senses also tell you to move no closer.".format(direction_checker(guessX,guessY,thingX,thingY)))
                elif abs(thingX-guessX)<=5 and abs(thingY-guessY)<=5: #Smoke sight Range
                    print(" On the horizon to your {0}, you see a column of smoke.".format(direction_checker(guessX,guessY,thingX,thingY)))
            elif type == 2: # ORC
                if thingX == guessX and thingY == guessY: #Attack range
                    if(weapon==False):
                        print(" You have gotten too close to an orc. After a brief skirmish, you acquire a few minor stab wounds. Pretty good for not having a weapon.")
                        damaged = -1
                    else:
                        print(" You have encountered an orc. After a brief skirmish, you leave him with several major stab wounds. Nice work.")
                elif abs(thingX-guessX)<=1 and abs(thingY-guessY)<=1:# Sight Range
                    if(weapon == False):
                        print(" You see an orc to your immediate {0}. As you have no weapon, you should probably leave him alone.".format(direction_checker(guessX,guessY,thingX,thingY)))
                    else:
                        print(" You see an orc to your immediate {0}. As you have a weapon, you can do whatever you want with this information.".format(direction_checker(guessX,guessY,thingX,thingY)))
            elif type == 5: # UNICORN
                if abs(thingX-guessX)<=1 and abs(thingY-guessY)<=1 and unicornSeen == True: #Healed range
                    print(" You encounter a unicorn. Though you don't have any sugar cubes, you gently hold out your hand. It approaches and bends to tap your palm with its horn.")
                    print(" You have been healed back to full health, 3/3.")
                    damaged = 3
                elif abs(thingX-guessX)<=2 and abs(thingY-guessY)<=2: #Sight range
                    print(" You see what looks like a white horse in an unfenced field to your {0}.".format(direction_checker(guessX,guessY,thingX,thingY)))
                    return(True)
            elif type == 11:
                if thingX == guessX and thingY == guessY and palantir == False: #Mountaintop
                    print(" You have reached the top of Mount Palantir. From here, you can see the whole plain of Gillikin:")
                    print(" \tTo your {0}, you see a shining lake. According to the visitor information sign, this is Lake Nimue.".format(direction_checker(guessX,guessY,lakeX,lakeY)))
                    print(" \tTo your {0}, you see a column of smoke, likely indicating the presence of a dragon.".format(direction_checker(guessX,guessY,dragonX,dragonY)))
                    print(" \tYou also spy five orcs, a unicorn, and countless rabbits wandering through the land.\n")
                    print(" After admiring the view for a while, you look down. At your feet, there is a strange forked stick.\n You pick up the stick and discover that it is not an ordinary stick, but a Wand of Dowsing. \n It tells you that the treasure is to your {0}. That's helpful. You decide to take the wand with you. \n Your chances of finding the treasure have greatly increased.".format(direction_checker(guessX,guessY,targetX,targetY)))
                    return True
                elif abs(thingX-guessX)<=1 and abs(thingY-guessY)<=1: #Healed range
                    print(" You are halfway up the mountain.")
                elif abs(thingX-guessX)<=5 and abs(thingY-guessY)<=5: #Sight range
                    print(" You are nearing the mountain.")
            elif type == 12: #LAKE
                if abs(thingX-guessX)<=1 and abs(thingY-guessY)<=1: #Swimming range
                    print(" You are now swimming in a lake. Good thing seven-league boots are waterproof.")
                elif abs(thingX-guessX)<=2 and abs(thingY-guessY)<=2: #Edge range
                    print(' You stop by the edge of a lake.')
                    if weapon == False:
                        print(' Out in the water, you see an arm holding a sword. As you watch, the sword rises out of the water,\n  revealing that it is held by a lady in a sopping white gown. The lady comes to the edge of the water and says to you,\n "Fair adventurer, take this gift as a token of your adventuring prowess."')
                        print("\n You now possess a sword. You will probably have better luck fighting orcs now.")
                        return True
                elif abs(thingX-guessX)<=5 and abs(thingY-guessY)<=5:# Sight range
                    print(" There is a shining lake to your {0}".format(direction_checker(guessX,guessY,thingX,thingY)))
        #update and compile damage
        if damaged < 0:
            if (health+damaged)>0:
                print(" Your health is now at {0}/3".format(health+damaged))
            else:
                print(" Unfortunately, your adventuring is now at an end.")
        return(damaged)

    def check_path(type,thingX,thingY):
        # N/S movement
        damaged = 0
        if (direction == 1 and guessY<thingY and (guessY+stepNumber)>thingY) or (direction == 3 and guessY>thingY and (guessY+stepNumber)<thingY):
            if abs(thingX-guessX)<=3:
                if abs(thingX-guessX)<=1:
                    if(type==1):
                        print(" During your journey, you got too close to a dragon. \n You have been devoured.")
                        damaged =-3
                    if(type==2):
                        if thingX == guessX:
                            print(" During your journey, you got too close to an orc. You were traveling too fast to defend yourself. \n He gifted you a stab wound as a souvenir of your visit.")
                            damaged =-1
                        else:
                            print(" During your journey, you passed very close to an orc, but luckily not within sword range.")
                    if(type==11):
                        if thingX == guessX:
                            print(" During your journey, you passed straight over the top of a mountain, but you were moving too fast to get a good view.")
                    if(type==12):
                        print(" During your journey, you passed straight through a lake. You are now sopping wet.")
                elif abs(thingX-guessX)<=2: #Fire Range
                    if(type==1):
                        print(" During your journey, you got too close to a dragon. It set your pants on fire.")
                        if((health-1)<=0):
                            finished = True
                            damaged = -1
                elif abs(thingX-guessX)<=3: #Sight Range
                    if(type==1):
                        print(" During your journey, you passed very close to a dragon, but managed to pass by unscathed. You are very lucky.")
        # E/W movement
        if (direction == 4 and guessX<thingX and (guessX+stepNumber)>thingX) or (direction == 2 and guessX>thingX and (guessX+stepNumber)<thingX):
            if abs(thingY-guessY)<=3:
                if abs(thingY-guessY)<=1:
                    if(type==1):
                        print(" During your journey, you got too close to a dragon. \n You have been devoured.")
                        damaged =-3
                    if(type==2):
                        if thingX == guessX:
                            print(" During your journey, you got too close to an orc. You were traveling too fast to defend yourself. \n He gifted you a stab wound as a souvenir of your visit.")
                            damaged =-1
                        else:
                            print(" During your journey, you passed very close to an orc, but luckily not within sword range.")
                    if thingY == guessY:
                        print(" During your journey, you passed straight over the top of a mountain, but you were moving too fast to get a good view.")
                    if(type==12):
                        print(" During your journey, you passed straight through a lake. You are now sopping wet.")
                elif abs(thingY-guessY)<=2: #Fire Range
                    if(type==1):
                        print(" During your journey, you got too close to a dragon. It set your pants on fire.")
                        if((health-1)<=0):
                            finished = True
                            damaged = -1
                elif abs(thingY-guessY)<=3: #Sight Range
                    if(type==1):
                        print(" During your journey, you passed very close to a dragon, but managed to pass by unscathed. You are very lucky.")
        if damaged < 0:
            if (health+damaged)>0:
                print(" Your health is now at {0}/3".format(health+damaged))
            else:
                print(" Unfortunately, your adventuring is now at an end.")
        return(damaged)

    #Opening message
    print("\n Welcome, adventurer! You stand in the very center of the plain of Gillikin, a land of dragons, orcs, and bunny rabbits.")
    print(" You seek to prove your adventuring prowess by discovering the fabled Treasure of Ynond. Luckily, you came prepared.")
    print(" You are wearing a pair of seven-league boots that enable you to travel up to seven leagues at a time. ")
    print(" However, you forgot to bring a sword. Adventure wisely.\n Good luck, adventurer!")

    while finished == False:
        while guessX!=targetX or guessY!=targetY:

            #check for enemies
            health += (check_for_item(1,dragonX,dragonY))
            health += (check_for_item(2,orc1X,orc1Y))
            health += (check_for_item(2,orc2X,orc2Y))
            health += (check_for_item(2,orc3X,orc3Y))
            health += (check_for_item(2,orc4X,orc4Y))
            health += (check_for_item(2,orc5X,orc5Y))
            health += (check_for_item(3,0,0))
            #check for unicorns
            if (unicornSeen == False):
                unicornSeen = check_for_item(5,unicornX,unicornY)
            else:
                health += (check_for_item(5,unicornX,unicornY))
                if health>3:
                    health =3

            #check for mysterious women lying in ponds
            if(weapon == False):
                weapon = (check_for_item(12,lakeX,lakeY))
            else:
                check_for_item(12,lakeX,lakeY)

            #check for clairvoyant mountaintops
            if(palantir == False):
                palantir = (check_for_item(11,mountainX,mountainY))
            else:
                check_for_item(11,mountainX,mountainY)

            #update position of moveable NPCs
            orc1X+= random.randint(-1,1)
            orc1Y+= random.randint(-1,1)
            orc2X+= random.randint(-1,1)
            orc2Y+= random.randint(-1,1)
            orc3X+= random.randint(-1,1)
            orc3Y+= random.randint(-1,1)
            orc4X+= random.randint(-1,1)
            orc4Y+= random.randint(-1,1)
            orc5X+= random.randint(-1,1)
            orc5Y+= random.randint(-1,1)

            if unicornSeen == False:
                unicornX+= random.randint(-2,2)
                unicornY+= random.randint(-2,2)
            if abs(unicornX)>20 or abs(unicornY)>20:
                unicornX = 0
                unicornY = 0

            if health>0:
                # check where you are with respect to the target
                if palantir == True:
                    print("\n The treasure is to your", direction_checker(guessX,guessY,targetX,targetY))
                else:
                    print("\n Mount Palantir is to your", direction_checker(guessX,guessY,mountainX,mountainY))

                # input desired direction and distance
                direction = input("\n Which direction would you like to go? (N,E,S,W) ")
                if direction == "none":
                    finished = True
                    break
                stepNumber = -1
                while stepNumber<0 or stepNumber>7 or stepNumber%1!=0:
                    stepNumber = input(" How many leagues would you like to travel? ")
                    if stepNumber.isdigit() == False:
                        print(stepNumber + " is not a number! Try again! ")
                        stepNumber = -1
                    else:
                        stepNumber = float(stepNumber)
                    if stepNumber <0 or stepNumber>7:
                        if stepNumber>7:
                            print(" Guess how many leagues seven-league boots can travel? Surprise, not {0}!".format(stepNumber))
                        print(" You seem to have difficulty with the concept of counting. Please try again.")
                    if stepNumber%1 != 0:
                        print(" You can only travel a fraction of a league if you can take a fraction of a step. Can you do that? I didn't think so.")
                        print(" You seem to have difficulty with the concept of counting. Please try again.")
                if direction == "N" or direction == "n":
                    direction = 1
                    guessY-=stepNumber
                elif direction == "E" or direction == "e":
                    direction = 2
                    guessX+=stepNumber
                elif direction == "S" or direction == "s":
                    direction = 3
                    guessY+=stepNumber
                elif direction == "W" or direction == "w":
                    direction = 4
                    guessX-=stepNumber
                else:
                    print("As you did not pick a valid direction, you have forfeited the chance to move. Please review third-grade geography and try again.")
                if guessX<=0:
                    longitude = "W"
                else:
                    longitude = "E"
                if guessY<=0:
                    latitude = "N"
                else:
                    latitude = "S"

                print("")

                health += check_path(1,dragonX,dragonY)
                health += check_path(2,orc1X,orc1Y)
                health += check_path(2,orc2X,orc2Y)
                health += check_path(2,orc3X,orc3Y)
                health += check_path(2,orc4X,orc4Y)
                health += check_path(2,orc5X,orc5Y)

                displayX = abs(guessX)
                displayY = abs(guessY)
                #print(" You have reached {0}{2}, {1}{3}.".format(displayX,displayY,longitude,latitude))

                check_for_item(0,targetX,targetY)
                if(finished==True):
                    break

            else:
                finished = True
                break
        break
