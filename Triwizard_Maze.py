# Time taken: 1718 + 60
# Compass directions: 1-N, 2-E, 3-S, 4-W
import random

compassKey = {'north': 1, "east": 2, "south": 3, "west": 4}

local_objects = ['hedge']
spell_choices = ["lumos", "point me", "red sparks", "expelliarmus", "stupefy", "impedimenta", "reducto",
                 "expecto patronum", "riddikulus"]

rescuer = 0
Encounter = False
encounter_name = "None"

Krum_status = "active"
Cedric_status = "friendly"

CS_counter = 0
CK_counter = -2  # -2 = first overheard. -1 = continuous overheard. 0 = arrived. 1 = first seen. 2 = continuous seen
CK_ignored_counter = 0
Skrewt_counter = 0
First_Skrewt = True
Sph_counter = 0  # 0 = first seen. 1 = first spoken to. 2 = riddle heard
Mist_counter = 0
Spider_counter = 0  # 1 = cedric seen. 2 = spider seen 3 = spider attacks 4 = spider carries 5 = under spider
Boggle_counter = 0
Peeves_counter = 0
Fleur_attacked = False
Flobberworms_dead = False
finished = False

# stuff: 0,0 = cup. 1,-10 = sphinx.  2, -12 = skrewt.  2,-4 = post-skrewt Cedric.  3,-5 = Boggart.  4,-3 = skrewt.
# 4,-8 = flobberworms.  5, -12 = torch.  7,-5 = egg.  7,-9 = trigger C&K encounter.  9,-1 = skrewt. 10,-6 = mist. 12,
# -12 = Peeves

N_paths = [
    [True, True, False, False, False, False, False, False, False, False, False, False, False],
    [True, True, True, True, True, True, True, True, False, False, False, False, False],
    [True, False, True, True, True, False, False, True, False, False, True, False, True],
    [True, True, False, True, False, True, False, True, False, False, True, False, True],
    [True, True, True, True, False, True, True, False, True, False, True, True, True],
    [True, True, True, False, False, True, True, True, True, True, True, True, True],
    [True, True, True, True, True, True, False, True, False, False, True, True, True],
    [True, True, False, False, True, True, False, False, False, True, True, True, True],
    [True, True, False, False, False, True, False, False, True, True, True, False, False],
    [True, True, True, False, False, True, False, False, False, False, False, False, False],
    [True, False, False, False, False, False, False, False, False, True, False, True, True],
    [True, False, False, False, False, False, True, False, False, False, True, True, True],
    [False, True, False, True, False, True, True, True, False, False, False, True, True],
    [False, False, False, False, False, False, False, False, False, False, False, False, False]
]

W_paths = [
    [False, True, False, False, False, False, False, False, True, True, True, True, True, True],
    [False, True, False, False, False, False, True, False, False, True, True, False, True, False],
    [False, False, True, False, True, True, True, True, True, True, True, True, True, False],
    [False, False, False, False, True, False, False, False, False, False, True, False, False, False],
    [False, False, False, True, True, True, False, False, False, True, False, False, False, False],
    [False, False, False, False, True, False, False, True, True, False, True, True, False, False],
    [False, True, False, True, False, True, True, False, True, True, False, False, False, False],
    [False, False, False, True, True, False, False, True, True, False, False, False, True, False],
    [False, False, False, True, True, True, True, True, True, True, True, True, True, False],
    [False, False, False, True, True, False, True, True, True, True, True, True, False, False],
    [False, True, True, True, True, True, True, True, True, False, False, False, False, False],
    [False, False, True, True, True, True, False, False, True, True, True, True, False, False],
    [False, True, False, True, True, False, True, True, True, False, True, True, True, False]

]


def general_path_check(positionX, positionY, direction):
    if direction == 1 or direction == 5:
        return N_paths[abs(positionY)][positionX]
    elif direction == 2:
        return W_paths[abs(positionY)][positionX + 1]
    elif direction == 3 or direction == -1:
        return N_paths[abs(positionY) + 1][positionX]
    elif direction == 4 or direction == 0:
        return W_paths[abs(positionY)][positionX]


def explain_path_check(positionX, positionY, direction_facing):
    Left = general_path_check(positionX, positionY, direction_facing - 1)
    Right = general_path_check(positionX, positionY, direction_facing + 1)
    Back = general_path_check(positionX, positionY, direction_facing - 2)
    Front = general_path_check(positionX, positionY, direction_facing)
    direction_option_list = [Front, Right, Left]
    open_path_list = []
    option_count = 0
    for i in range(3):
        if direction_option_list[i]:
            open_path_list.append(i)
            option_count += 1
    if option_count == 3:
        return "You have reached a crossroads. All paths are open."
    elif option_count == 2:
        if open_path_list[0] != 0:
            return "The way forward is blocked by a hedge. But there are paths to your right and left."
        else:
            message = "The path you are on continues forward, but there is a side path to your "
            if open_path_list[1] == 1:
                message += "right."
            else:
                message += "left."
            return message
    elif option_count == 1:
        if open_path_list[0] == 0:
            return "You are in a straight stretch of corridor."
        else:
            message = "You have reached a corner. The path continues to your "
            if open_path_list[0] == 1:
                message += "right."
            else:
                message += "left"
            return message
    else:
        return "You have reached a dead end."


def nearby_objects_check(x, y):
    if x == 1 and y == -10:
        return 'a sphinx standing in the path.'
    elif (x == 2 and y == -12) or (x == 4 and y == -3) or (x == 9 and y == -1):
        return 'a skrewt. Maybe you should avoid it.'
    elif x == 2 and y == -4 and Encounter and encounter_name == "Cedric and Skrewt":
        return 'Cedric, breathing hard.'
    elif x == 3 and y == -5:
        return 'a dementor.'
    elif x == 4 and y == -8:
        if not Flobberworms_dead:
            return 'a pile of Flobberworms.'
        else:
            return 'a crater with bits of Flobberworm scattered about.'
    elif x == 5 and y == -12:
        return 'a bobbing light in the distance.'
    elif x == 7 and y == -5:
        return "a large egg."
    elif x == 7 and y == -9 and Encounter and encounter_name == "Cedric and Krum" and CK_counter == -2:
        return 'Cedric lying on the ground, Krum standing over him.'
    elif x == 12 and y == -12:
        return "Peeves."
    else:
        return "None"


class Character:
    def __init__(self, name):
        self.name = name
        # Regular starting point: 7,-1, compass 3
        self.x = 7
        self.y = -1
        self.compass = 3
        self.Cedric_relations = 0
        self.health = 3
        self.status = "normal"

    def move(self, direction):
        # Rotate to face correct direction
        current_direction = self.compass
        if direction == "l":
            self.compass -= 1
        elif direction == "r":
            self.compass += 1
            if self.compass > 4:
                self.compass -= 4
        elif direction == "b":
            self.compass -= 2
        if self.compass < 1:
            self.compass += 4
        # check for wall in the way
        if general_path_check(self.x, self.y, self.compass):
            if self.compass == 1:
                self.y += 1
            elif self.compass == 2:
                self.x += 1
            elif self.compass == 3:
                self.y -= 1
            elif self.compass == 4:
                self.x -= 1
        else:
            newDirection = direction
            if len(direction) == 1:
                newDirection = "that direction"
            print(
                "You attempt to go " + direction + ", but there is a hedge in the way. Pay better attention to your "
                                                   "surroundings!")
            self.compass = current_direction

    def activate_Encounter(self):
        if self.x == 1 and self.y == -10:
            if encounter_name != "Sphinx":
                return "Sphinx"
            else:
                return "None"
        elif (self.x == 0 and self.y == -12) or (self.x == 4 and self.y == -3) or (self.x == 9 and self.y == -1) or (
                self.x == 7 and self.y == -4):
            return "Skrewt"
        elif self.x == 2 and self.y == -4 and CS_counter < 1:
            return "Cedric and Skrewt"
        elif self.x == 3 and self.y == -5:
            return "Dementor"
        elif self.x == 5 and self.y == -11 and self.compass == 1:
            return "Hinkypunk"
        # elif self.x == 7 and self.y == -5:
        #     return "Dragon Egg"
        elif self.x == 7 and self.y == -9 and CK_counter == -2:
            return "Cedric and Krum"
        elif self.x == 10 and -8 < self.y < -4:
            return "Mist"
        elif self.x == 12 and self.y == -12:
            return "Peeves"
        elif self.x == 0 and self.y == -7:
            return "Spider"
        else:
            return "None"

    def cast_PointMe(self):
        if self.compass == 4:
            true_north = "to your right."
        elif self.compass == 3:
            true_north = "directly behind you."
        elif self.compass == 2:
            true_north = "to your left."
        else:
            true_north = "directly in front of you."
        return "Your wand spins in your hand to point " + true_north + " North is that way."

    def cast_Lumos(self):
        print(' You whisper "Lumos!" and raise your wand to look about.')
        northward = nearby_objects_check(self.x, self.y + 1)
        eastward = nearby_objects_check(self.x + 1, self.y)
        southward = nearby_objects_check(self.x, self.y - 1)
        westward = nearby_objects_check(self.x - 1, self.y)
        cardinalDirections = [northward, eastward, southward, westward]

        front = cardinalDirections[(self.compass - 1) % 4]
        right = cardinalDirections[self.compass % 4]
        back = cardinalDirections[(self.compass + 1) % 4]
        left = cardinalDirections[(self.compass + 2) % 4]

        if front != "None":
            print(' In front of you, you see ' + front)
        if right != "None":
            print(' To your right, you see ' + right)
        if left != "None":
            print(' To your left, you see ' + left)
        if back != "None":
            print(' Behind you, you see ' + back)
        print(" There is nothing else of interest nearby. You extinguish your wandlight.")

    def attacking_Cedric(self, spell):
        if spell == 4:
            self.Cedric_relations -= 1
            print('\tYou hit him with the Disarming Charm and his wand flies out of his hand. You catch it.\n')
            newAction = 0
            while newAction == 0:
                newAction = input('\tHe stares at you. “I’d like my wand back, please.” \n 1. Yes\n 2. No.\n')
                if newAction == 1 or newAction == "Yes" or newAction == "yes":
                    print('\t“Sorry, Cedric. Here you go.”\n You return his wand.')
                elif newAction == 2 or newAction == "No" or newAction == "no":
                    newAction = 2
                    print('\t"No," you say. "I won its allegiance. Your wand is mine now."')
                else:
                    newAction = 0
            if newAction == 2:
                self.Cedric_relations -= 1
                newAction = 0
                while newAction == 0:
                    newAction = input(
                        '\tCedric stares at you in disbelief. “Seriously, Harry? I need that wand to finish the '
                        'tournament.”\n 1. Yes\n 2. No\n')
                    if newAction == 1 or newAction == "Yes" or newAction == "yes":
                        print('\t"You\'re right. I\'m sorry."\n You return his wand.')
                    elif newAction == 2 or newAction == "No" or newAction == "no":
                        self.Cedric_relations -= 1
                        print(
                            '\t"I\’ll send up red sparks for you if you want." \n\tHe stares at you in disgust. "You '
                            'foul little – ! So that’s how we stand. I see."')
                        print(
                            '\tHe suddenly lunges at you, knocking both wands out of your hand. In the ensuing '
                            'struggle, his superior\n height and weight give him the advantage, so that he ends up '
                            'with both wands. He traps you in a full\n Body-Bind, then drops your wand on your chest. '
                            '\n\t“We Hufflepuffs are forgiving. So I’ll give you a second chance. This will wear off '
                            'in a few minutes.\n But cross me again and I won’t be so nice.”\n\tHe departs.')
                    else:
                        newAction = 0
        if 4 < spell < 10:
            print('Your spell whizzes past his ear. He turns and stares at you in disbelief. ', end='')
            if spell == 8:
                print('"I\'m not a Dementor!', end=" ")
            elif spell == 9:
                print('"I\'m not a Boggart!', end=' ')
            elif self.Cedric_relations > -3:
                print('"', end='')

            if self.Cedric_relations > -1:
                print('You git! Why are you attacking me?"')
            elif self.Cedric_relations > -3:
                print('My dad was right. There’s something wrong with you."')
                if self.Cedric_relations == -2:
                    print(
                        'He traps you in a full Body-Bind. “We Hufflepuffs are forgiving. So I’ll give you a second '
                        'chance. This\n will wear off in a few minutes. But cross me again and I won’t be so nice.”')
            else:
                print("He whips out his own wand and knocks you cold. You come to with McGonagall standing above you.")
                Endings("Rescued by Professor McGonagall")
            self.Cedric_relations -= 1

    def Bagman(self):
        print(
            "Teleportation Wizard activated. (Is this cheating? Shh! Don't tell the goblins!)\n Which method of "
            "travel would you like? \n 1. Coordinates\n 2. Event")
        teleportChoice = input(" ")
        teleportChoice = teleportChoice.lower()
        if teleportChoice == '1' or teleportChoice == "coordinates":
            self.x = int(input(" X coordinate? "))
            self.y = int(input(" Y coordinate? "))
            direction = input(" Which direction would you like to face? ")
            self.compass = compassKey[direction]
        else:
            events = ['Post-skrewt Cedric', 'Dementor', 'Golden Mist', 'Cedric and Krum', 'Hinkypunk', 'Sphinx',
                      'Spider', 'Peeves']
            print(" Which event would you like to visit?")
            for i in range(len(events)):
                print(str(i + 1) + " " + events[i])
            eventChoice = input(" ")
            if eventChoice.isdigit():
                number = int(eventChoice)
                eventChoice = events[number - 1]
            eventChoice = eventChoice.lower()
            if eventChoice == 'post-skrewt cedric':
                self.x = 3
                self.y = -4
                self.compass = 4
            elif eventChoice == 'dementor':
                self.x = 3
                self.y = -6
                self.compass = 1
            elif eventChoice == "golden mist":
                self.x = 10
                self.y = -7
                self.compass = 1
            elif eventChoice == "cedric and krum":
                self.x = 7
                self.y = -9
                self.compass = 2
            elif eventChoice == 'hinkypunk':
                self.x = 6
                self.y = -12
                self.compass = 4
            elif eventChoice == 'sphinx':
                self.x = 2
                self.y = -10
                self.compass = 4
            elif eventChoice == 'spider':
                self.x = 0
                self.y = -8
                self.compass = 1
            elif eventChoice == 'peeves':
                self.x = 11
                self.y = -12
                self.compass = 2


Harry = Character("Harry")


def Endings(title):
    Epilogue = "Nope"
    if title.startswith("Rescued"):
        if title != "Rescued by Professor Moody":
            if title == "Rescued by Hagrid":
                print(
                    '\tWhen Hagrid comes around the corner and sees you, his face falls. “Oh, Harry, I was hoping it '
                    'wouldn’\n be you. But at leas’ you’re all right. Did you see the Skrewts? Aren’t they '
                    'magnificent?”\n\tYou hastily nod agreement, then follow Hagrid out of the maze.')
            elif title == "Rescued by Professor McGonagall":
                print(
                    '\tMcGonagall comes to retrieve you, looking disappointed. “Potter, I expected better of you. '
                    'But,” she\n sighs, “at least you survived the tournament. That’s better than most years.”\n\tYou '
                    'follow her out of the maze to safety.')
            elif title == 'Rescued by Professor Flitwick':
                print(
                    '\tFlitwick comes to retrieve you. “This is a quite difficult challenge,” he squeaks. “But at '
                    'least you\n were wise enough to know your limits. And Cedric’s still out there, so we may yet '
                    'have a Hogwarts champion!”\n\tYou follow him out of the maze to safety.')
            print(
                '\tYou wait out the rest of the task under Dumbledore’s watchful eye. But the outcome of the '
                'Triwizard\n Tournament is uncertain, as Cedric and the Cup both mysteriously disappeared.')
            if Harry.Cedric_relations >= 0:
                print(
                    '\tSeveral days later, his body and the Cup are discovered in a graveyard in Little Hangleton. He '
                    'is\n posthumously declared the Triwizard Champion.')
            print(
                '\tThrough the summer, your scar begins to hurt and you can’t shake the feeling that Voldemort is '
                'after\n you. One night, while you and your cousin Dudley are walking home, you are confronted by a '
                'hooded figure.\n It stretches forth its hand. You nearly cast a Patronus charm, but then it flips '
                'back its hood and reveals\n the face of Professor Moody. “Come, Harry. There’s no time to lose!” he '
                'growls. You take his hand, then\n suddenly everything goes black; you are being pressed very hard '
                'from all directions; you can’t breathe,\n there are iron bands tightening around your chest; your '
                'eyeballs are being forced back into your head; your\n eardrums are being pushed into your skull -- '
                '\n\tYou are standing in a dark and overgrown graveyard. You can see the black outlines of a small '
                'church\n and a fine old house. You can also see a cloaked figure holding a bundle. Your scar '
                'explodes with pain and\n you fall to the ground. Above you, you hear a high cold voice say, '
                '“Harry Potter. I have waited far too long\n for this.”')
            print(
                '\tTHE END\n\tYou couldn’t finish the maze, but at least you were rescued by a friendly face. Well, '
                'for a little while.',
                end="")
            if Harry.Cedric_relations < 0:
                print('And Cedric lived! But, is that really a good thing … ?')
        else:
            print(
                '\tMoody limps around the corner. “Oh, Potter,” he growls. “I expected better of you. But at least '
                'you\n survived. That’s more than some have done.” While he’s talking, he takes you by the arm and '
                'continues\n guiding you through the maze.\n\t“Professor, are you sure this is the fastest way '
                'out?”\n\t“I’m taking a shortcut.”\n\tAfter rounding one last corner, you come upon a clearing, '
                'in the center of which is the Triwizard Cup.\n\t“Professor, I think you’ve gone the wrong way. '
                'You’re supposed to take me out of the maze, aren’t you?”\n\tBut he is gazing at the cup and scarcely '
                'seems to hear you. “Just look at it, Harry. It’s what all of\n you are striving for. None of the '
                'others deserve it, Harry. Krum is a Dark wizard. Fleur is a flutterhead.\n Cedric is, well, '
                'not quite bright. You’ve conquered more in fourteen years than they’ve even seen. Take the cup.”')
            choice = input(' 1. Take the cup.\n 2. Refuse')
            choice = choice.lower()
            if choice == '1' or choice == 'take the cup':
                print(
                    '\tThough this isn’t at all in the spirit of the contest, the whole tournament’s been rigged '
                    'anyway. Why\n not get the glory? You step forward, grinning, and grasp both handles at once. '
                    'Instantly, you feel a jerk\n behind your navel. Your feet leave the ground. You cannot release '
                    'your prize as the Cup pulls you onward\n in a howl of wind and swirling color, leading you to '
                    'Voldemort.')
                print(
                    '\tTHE END.\n\tIn the words of the Sorting Hat, you would have done well in Slytherin, '
                    'you cheater. But at least Cedric lived.')
            else:
                print(
                    '\t“What? Professor, of course not!”\n\tHe stares at you, then a grin creases his face. “Won’t '
                    'take the easy glory, eh? Just like your parents.\n Well, then, just come closer and look at it, '
                    'while you have the chance.”\n\tHe walks closer to the plinth and you follow. You gaze at the '
                    'gleaming golden cup together. Professor\n Moody seems mesmerized by its shining surface. After a '
                    'few moments, you ask, “Er, Professor, the other\n competitors might be arriving soon. Should we '
                    'go now?”\n\t“Yes, of course.” He snatches at your wrist with one claw and and shoots out his '
                    'other hand to grab the\n Cup. Instantly, you feel a jerk behind your navel. Your feet leave the '
                    'ground. Moody’s hand around your\n wrist drags you onward in a howl of wind and swirling color. '
                    'Maybe it’s the confusion of Portkey travel,\n but it seems as though his face melts in the '
                    'swirl, morphing into one you have only seen in a memory.\n Barty Crouch Jr.')
                print(
                    '\tTHE END\n\tYou may not have been able to solve the maze, but at least you’re not a cheater. '
                    'And, Cedric lived!')

    elif title.startswith("Killed"):
        if title == "Killed by Spider":
            print(
                "\tOn top of your previous injuries, this is too much to bear. Your consciousness slowly fades away "
                "as\n you see Cedric running for the cup. \n He never returns.",
                end='')
            if Harry.Cedric_relations >= 0:
                print(
                    'Several days later, his body is found in a graveyard in Little Hangleton, with a gash in the '
                    'crook of his elbow.')
                Epilogue = "The Chosen One"
            else:
                print(" Rumor has it he joined Voldemort.")
                Epilogue = "The Noseless One"
        else:
            if title == "Killed by Dementor":
                print(
                    '\tYou hear your mother screaming in the distance as the Dementor bends towards you. Cold '
                    'hopelessness\n floods you. You cannot fight back. You cannot think. You cannot ... Your '
                    'consciousness fades away as your\n soul is parted from your body. \n\t Eventually, Cedric comes '
                    'upon your soulless body and casts red sparks.')
            else:
                if title == "Killed by Sphinx":
                    print(
                        "\tYou are quickly torn to shreds by her fierce claws. Sphinxes have little tolerance for "
                        "stupidity.")
                print(" Overcome by your wounds, you die. Cedric comes upon your body and casts red sparks.")

            if Harry.Cedric_relations > 0:
                Epilogue = "The Chosen One"
                print(
                    "He remains at your side until McGonagall comes. At the death of a student, the tournament is "
                    "immediately called off.")
                if Fleur_attacked == True:
                    print(
                        "Because Fleur was already rescued and Krum was disqualified by using Dark Magic, Cedric wins "
                        "by default.")
                else:
                    print(
                        "Because Cedric was in the lead before this final task, he is declared the winner of the "
                        "Triwizard Tournament.")
            else:
                print(" He then continues deeper into the maze. He never returns.", end="")
                if Harry.Cedric_relations < 0:
                    print(" Rumor has it has joined Voldemort’s followers.")
                    Epilogue = "The Noseless One"
                else:
                    Epilogue = "The Chosen One"
                    print(
                        "Several days later, his body is found in a graveyard in Little Hangleton, with a gash in the "
                        "crook of his elbow.")

    elif title.startswith("Take the Cup"):
        if title.startswith("Take the Cup Alone"):
            if title == "Take the Cup Alone, at Cedric's Prompting":
                print(
                    "\tYou look from Cedric to the cup. For one shining moment, you see yourself emerging from the "
                    "maze,\n holding it. You see yourself holding the Triwizard Cup aloft, hear the roar of the "
                    "crowd, see Cho's face\n shining with admiration.\n\t With difficulty, you limp to the cup, "
                    "not wanting to accept any more of Cedric’s help than necessary.\n Reaching the cup, "
                    "you grasp both handles at once. Instantly, you feel a jerk behind your navel. Your feet\n leave "
                    "the ground. You cannot release your prize as the Cup pulls you onward in a howl of wind and "
                    "swirling\n color, leading you to Voldemort.")
                print("\tTHE END")
                print("\tYou're selfish, but you saved Cedric's life.")
            if title == "Take the Cup Alone, you Jerk":
                print(
                    "\tThe spider seizes Cedric and carries him off. With the path now clear, you run towards the "
                    "cup.\n Reaching it, you you grasp both handles at once. Instantly, you feel a jerk behind your "
                    "navel. Your feet\n leave the ground. You cannot release your prize as the Cup pulls you onward "
                    "in a howl of wind and swirling\n color, leading you to Voldemort.")
                print("\tTHE END")
                print("\tYou\'re selfish, and you didn\'t even save Cedric, you jerk.")

        if title.startswith("Take the Cup, Cedric"):
            if title == "Take the Cup, Cedric, Please":
                print(
                    '\t"Cedric, I\'m sick of the limelight,” you say. “I don’t deserve to be here, didn’t want to be '
                    'here,\n and definitely don’t need my face plastered all over the Daily Prophet again. Hufflepuff '
                    'House hasn’t had\n this kind of glory in centuries. Go ahead. Take the cup. You deserve '
                    'it.”\n\tAfter wrestling with himself,\n Cedric reluctantly nods. “If you’re certain." \n “I’m '
                    'certain, Cedric. Go ahead.”\nHe walks up to the cup, stretches out his hands, then seizes the '
                    'cup by both handles. Immediately, he\n and the cup disappear. Something is definitely very wrong '
                    'with this tournament. \n\tAs you stand there, wondering, someone comes up behind you. It is '
                    'Professor Moody. “What happened?” he\n asks gruffly.\n\t“Cedric took the cup. But then he '
                    'disappeared.” \n\t“I knew there was something fishy about this whole mess,” he growls. “Here, '
                    'Potter. Lean on me. I’ll get you out of here.”\nAs you lean on him to get the weight off your '
                    'damaged leg, he grips you firmly and suddenly\n everything goes black; you are being pressed '
                    'very hard from all directions; you can’t breathe, there are\n iron bands tightening around your '
                    'chest; your eyeballs are being forced back into your head; your eardrums\n are being pushed into '
                    'your skull --\n\tYou arrive. Gulping great lungfuls of cold night air, you open your streaming '
                    'eyes to see Cedric, dead on the ground. You are in a graveyard')
                print("\tTHE END")
                print("\tHufflepuff got its glory at last, shortly before its champion was killed. At least you tried.")
            if title == "Take the Cup, Cedric, You jerk":
                print(
                    '\tYou can hear Cedric running for the Cup as the spider carries you away and begins to swaddle '
                    'you in\n sticky strands. It injects you with a paralyzer and you lose consciousness. \n\tYou '
                    'wake up hazily when someone brushes the web away from your face. It is Professor Moody. As you '
                    'try to\n tell him what happened, he shushes you and says, “Don’t worry about that now. I’ll get '
                    'you out of here\n first.” You suddenly feel as though you are being forced through a very tight '
                    'rubber tube, and you lose\n consciousness again.')
                print(
                    '\tYou wake to find yourself still bound. But when you look down, you are no longer bound by '
                    'webs, but\n ropes. There is a fresh cut in the crook of your elbow. As you blink blearily, '
                    'you realize that you are in\n a graveyard. As you look more closely, you realize that Voldemort '
                    'himself is standing in front of you, with\n a semicircle of Death Eaters behind him. Cedric '
                    'stands among them. \n\t“Now untie him, Wormtail, and give him back his wand.” \n\tWormtail '
                    'approaches you, raises a silver hand, and slashes through your ropes. Still groggy from the '
                    'poison, you\n crumple in a heap at the base of the tombstone. Someone places a wand in your '
                    'hand, but your nerveless fingers\n cannot hold it.\n\tVoldemort laughs, high and cold. “See how '
                    'spineless he really is. Avada Kedavra!”\n\tYou wake up in a strange misty emptiness that reminds '
                    'you vaguely of King’s Cross Station. There is\n a small, ugly, naked, wounded creature nearby. '
                    'Your father comes to you and asks whether you would like\n to go on or return to the world for a '
                    'second chance.')
                action = input("1. Go on\n2. Return to life")
                if action == "1" or action == "go on" or action == "Go on":
                    print(
                        '\tYou choose to continue on, not to return to your life of pain. Not even J.K. Rowling knows '
                        'what you find there.')
                else:
                    print(
                        '\tYou awaken on the ground and play dead. It seems that Voldemort, too, was briefly '
                        'unconscious. Now he\n asks coldly. “Is the boy dead?” No one responds, so he orders, '
                        '“You there. Examine him. Tell me whether he\n is dead." There is a bang and a gasp of '
                        'pain.\n\tLong blond hair drifts over your face. Your heart thumps traitorously, and you know '
                        'your inspector feels\n it. Lucius Malfoy leaps back and yells, “He’s alive!”\n\tYou struggle '
                        'to rise to your feet and defend yourself, but are still too weak. Overwhelmed by the Death\n '
                        'Eaters, you die ignominiously. This time you do not return.')
                Epilogue = "The Noseless One"
        elif title == "Take the Cup Together":
            print(
                '"Both of us," you say.\n\t"What?" Cedric asks.\n\t"We\'ll take it at the same time. It\'s still a '
                'Hogwarts victory. We\'ll tie for it."\n\tCedric stares at you. "You - you sure?"\n\t"Yeah,'
                '" you say. "Yeah . . . we\'ve helped each other out, haven\'t we? We both got here. Let\'s just\n '
                'take it together."\n\tCedric grins. "You\'re on. Come here."\n\tHe grabs your arm and helps you limp '
                'toward the plinth where the cup stands. You both hold a hand out over one of the cup\'s gleaming '
                'handles.\n\t"On three, right? One - two - three -" You both grasp a handle.\n\tInstantly, '
                'you feel a jerk somewhere behind your navel. Your feet leave the ground. You can’t unclench the\n '
                'hand holding the Triwizard Cup; it pulls you onward in a howl of wind and swirling color, '
                'Cedric at your side.')
            print("\tTHE END")
            print(
                "Nice job staying accurate to the story. Cedric’s going to die, but at least you know it all turns "
                "out right in the end.")
    if Epilogue != "Nope":
        if Epilogue == "The Chosen One":
            print("""Two years later, Dumbledore dies of a mysterious curse that withered his hand. Then, in a stunning coup, the Dark Lord takes over the Ministry and reveals himself returned to full power. Ron and Hermione drop out of school and go underground together. Rumor has it they are on Dumbledore’s last mission, searching for a way to kill Voldemort. The Order of the Phoenix frantically tries to reconstitute itself. However, without warning of Voldemort’s return and without Dumbledore’s leadership, half the members are killed before they establish a safe house. Voldemort is unstoppable … until he tries to recruit Neville Longbottom, leader of a student resistance group, the Defense Alliance.
	Voldemort first encounters Neville in the Room of Requirement, asks him what he seeks, and offers him more power than he could dream of. Neville refuses, runs, and accidentally sets the room on fire. Several months later, Voldemort is meeting with Headmaster Snape in his office about the dissatisfactory performance of the Malfoys when Neville, Ginny, and Luna try to break in. Voldemort commends Neville on his courage and offers to train him as his second in command. Neville refuses and says he’ll only consider it if he can be Voldemort’s equal. Furious, Voldemort says no one is his equal, that to say so is as ridiculous as that old hat being equal to Nagini. He pulls the hat down over Neville’s eyes and orders Nagini to kill the three students. Neville pulls the sword of Gryffindor out of the hat, kills Nagini, and runs. Flying, Voldemort pursues him to the Hogwarts grounds, where he summons Dementors to attack Neville. But Neville performs the Patronus charm and the Dementors turn on their commander. With no happy memories, Voldemort is unable to produce a Patronus, and is defeated by magic he knows not, as the Dementors suck out the last bit of his soul.
	THE END
	You’re dead, but at least you destroyed the Horcrux within your scar. Good thing the prophecy had a spare.""")

        elif Epilogue == "The Noseless One":
            print("""Two years later, Dumbledore dies of a mysterious curse that withered his hand. Then, in a stunning coup, the Dark Lord takes over the Ministry and reveals himself returned to full power. Ron and Hermione drop out of school and go underground together. Rumor has it they are on Dumbledore’s last mission, searching for a way to kill Voldemort. The Order of the Phoenix frantically tries to reconstitute itself. However, without warning of Voldemort’s return and without Dumbledore’s leadership, half the members are killed before they establish a safe house. In one such skirmish, Cedric Diggory kills Neville Longbottom, who is escorting Order Members into Hogwarts through the Hog’s Head Inn. Voldemort grows stronger and stronger until none can oppose him.
	THE END
		You’re dead and Voldemort won. You probably should have been nicer to Cedric.""")

    return True


# Opening text
print("""Ladies and gentlemen, the third and final task of the Triwizard Tournament is about to begin! Let me remind you how the points currently stand! Tied in first place, with eighty-five points each - Mr. Cedric Diggory and Mr. Harry Potter, both of Hogwarts School! In second place, with eighty points - Mr. Viktor Krum, of Durmstrang Institute! And in third place - Miss Fleur Delacour, of Beauxbatons Academy!”
	He lowers his voice. “Remember, champions, you will enter the east side of the maze. The Cup is in the very center. If you run into trouble and want to be rescued, send up red sparks and one of our patrollers will come to your aid.” He lowers his voice even further. “And, er, Harry, if you need any help, just ask. Checking your 'options' is a good place to start.” He winks at you, then remagnifies his voice.
	“So ... on my whistle, Harry and Cedric! Three - two - one -"
　　He gives a short blast on his whistle. You and Cedric hurry into the maze.
　　The towering hedges cast black shadows across the path and the sound of the surrounding crowd is silenced. After about fifty yards, you and Cedric reach a fork. Cedric turns right and disappears into the maze. You turn left.""")

while finished == False:
    # check paths and give location update (unless at some high-activity area)
    # print(encounter_name)
    # print(Encounter)
    if Encounter == False or ((Encounter == False and Harry.x != 7 or Harry.y != -8) and (
            Harry.x != 1 or Harry.y != -10 and Sph_counter != 5) and (Harry.x != 0 or Harry.y < -7) and (
                                      Harry.x != 3 or Harry.y != -5) and (Harry.x != 10 or Harry.y != -6)):
        # print(Harry.x)
        # print(Harry.y)
        print(explain_path_check(Harry.x, Harry.y, Harry.compass))
    # check whether an encounter ought to be activated
    if not Encounter:
        encounter_name = Harry.activate_Encounter()
        if encounter_name != "None":
            Encounter = True
    if encounter_name == 'None':
        Encounter = False
    # If Encounter is activated, run Encounter description
    if Encounter:
        if encounter_name == "Cedric and Krum":
            if CK_counter == -2:
                if Harry.compass == 4:
                    true_north = "to your right"
                elif Harry.compass == 2:
                    true_north = "to your left"
                print(
                    ' The hedge ' + true_north + 'is thinner in this spot. You hear something in the path on the '
                                                 'opposite side. Cedric’s voice is yelling, “What are you doing? What '
                                                 'the hell d\'you think you\'re doing?" \n Then you hear Krum’s '
                                                 'voice. "Crucio!" \n The air is suddenly full of Cedric\'s yells.')
                CK_counter = -1
            elif CK_counter == -1:
                if Harry.x == 7 and Harry.y == -8:
                    CK_counter = 0
                else:
                    print(" You continue to hear Cedric's yells, growing fainter.")
                    CK_ignored_counter += 1
                    if CK_ignored_counter == 14:
                        encounter_name = "None"
                        Encounter = False
            if CK_counter == 0:
                print("You see Cedric jerking and twitching on the ground, Krum standing over him.")
                local_objects = ['cedric'] + ['krum'] + local_objects
                CK_counter += 1

        elif encounter_name == "Cedric and Skrewt":
            if CS_counter == 0:
                print(" You hear movement right behind you. Something bursts out of a path on the right.")
                local_objects = ['cedric'] + local_objects
                CS_counter = 1
            elif CS_counter == 1:
                if Harry.Cedric_relations < 0:
                    print(' He dodges down a separate path.')
                else:
                    print(
                        'The thing behind you turns out to be Cedric. He looks shaken and the sleeve of his robe is '
                        'smoking.\n "Hagrid\'s Blast-Ended Skrewts!" he hisses. "They\'re enormous - I only just got '
                        'away!"\n Shaking his head, he dives out of sight along another path. Maybe you shouldn’t go '
                        'that way.')
                Encounter = False
        elif encounter_name == "Mist":
            if Mist_counter == 0:
                Mist_counter = 1
            elif Mist_counter == 1:
                Fleur_attacked = True
                print(
                    "A scream shatters the silence. There’s only one person in the maze capable of producing such a "
                    "scream: Fleur. \nThere is silence. Her scream seems to have come from somewhere ahead.")
                Mist_counter = 2
            elif Mist_counter == 2 and Harry.y == -6:
                Mist_counter = 3
        elif encounter_name == "Hinkypunk":
            if Harry.y == -11:
                if Harry.x == 5:
                    print(" The bobbing light is to your left. You think it wants you to follow it.")
                elif Harry.x == 4:
                    print(
                        "You are getting closer to the light, which is directly ahead of you. You can make out that "
                        "it is actually\n a tiny bobbing lantern.")
                elif Harry.x > 1:
                    print(" The lantern is directly in front of you. You hurry to keep it in sight.")
                elif Harry.x == 1:
                    print(
                        "The lantern turns the corner, heading left. You are very close now and can tell that it is "
                        "held by a wispy\n blue smoke-like creature.")
            elif Harry.y == -12:
                if Harry.x == 1:
                    print(
                        "The wisp is around the corner to your right. You fancy you see it gesturing for you to "
                        "hurry, that you're\n almost there.")
                elif Harry.x == 0:
                    print(
                        "Apparently, the wisp is not a friendly guide after all. You hastily duck as it launches a "
                        "fireball at you.\n Then it slowly fades through the hedge wall, cackling. You are relieved "
                        "for a moment, then look up and\n realize you have a bigger problem.")
                    encounter_name = "Skrewt"
        elif encounter_name == "Sphinx":
            if Sph_counter == 0:
                print(
                    '\tAhead of you is a sphinx. It has the body of an over-large lion: great clawed paws and a long '
                    'yellowish\n tail ending in a brown tuft, but it has the head of a woman. She turns her long, '
                    'almond-shaped eyes\n upon you. However, she does not seem about to attack, but instead paces '
                    'from side to side of the path,\n blocking your progress. Then she speaks in a deep, '
                    'hoarse voice.\n\t"You are very near your goal. The quickest way is past me."')
                if 'sphinx' not in local_objects:
                    local_objects = ['sphinx'] + local_objects
            elif Harry.x == 1 and Harry.y == -10:
                print(' The sphinx remains in the middle of the path, blocking your way forward.')
            elif Sph_counter == 5:
                Encounter = False
        elif encounter_name == "Spider":
            if Spider_counter == 0:
                print(
                    'The Triwizard Cup is gleaming on a plinth a hundred yards away.\n Suddenly a dark figure hurtles '
                    'out onto the path in front of you. It is Cedric, running for the cup.')
                local_objects = ['cedric'] + local_objects
                Spider_counter += 1
            elif Spider_counter == 1 and Harry.y == -6:
                print(
                    '\tYou charge forward, but Cedric is going to get there first. Cedric is sprinting as fast as he '
                    'can toward\n the cup, and you have no chance of catching up; Cedric is much taller, '
                    'with much longer legs.\n\tThen you see something immense over a hedge to your left, '
                    'moving quickly along a path that intersects\n with your own; it is moving so fast Cedric is '
                    'about to run into it, and Cedric, his eyes on the cup,\n has not seen it –')
                local_objects = ['spider'] + local_objects
                Spider_counter += 1
            elif Spider_counter == 3:
                print(
                    "Cedric looks around just in time to hurl himself past the thing and avoid colliding with it, "
                    "but in his\n haste he trips. Cedric’s wand flies out of his hand as a gigantic spider steps into "
                    "the path and begins\n to bear down on him.")
            elif Spider_counter == 4:
                pass
            if Harry.status == "under_Spider":
                Spider_counter = 5
        elif encounter_name == "Dementor":
            if Harry.x != 3 or Harry.y != -5:
                Boggle_counter = 0
                local_objects = ['hedge']
                Encounter = False
            else:
                if 'dementor' not in local_objects:
                    local_objects = ['dementor'] + local_objects
                if Boggle_counter == 0:
                    print(
                        "\tAs you turn a corner, you see ... a dementor gliding toward you. Twelve feet tall, "
                        "its face hidden by\n its hood, its rotting, scabbed hands outstretched, it advances, "
                        "sensing its way blindly toward you. You\n can hear its rattling breath; you feel clammy "
                        "coldness stealing over you.")
                    Boggle_counter = 1
                elif Boggle_counter == 1:
                    print(" The monster glides closer towards you. All the worst memories of your life overwhelm you.")
                    Boggle_counter = 2
                elif Boggle_counter == 2:
                    print(" You can feel the Dementor's cold breath on your face as it prepares to suck out your soul.")
                    Boggle_counter = 3
                elif Boggle_counter == 3:
                    finished = Endings("Killed by Dementor")
        elif encounter_name == "Peeves":
            if 'peeves' not in local_objects:
                local_objects = ['peeves'] + local_objects
            if Harry.x != 12 and Harry.y != -12:
                Encounter = False
                local_objects = ['hedge']
            elif Peeves_counter == 0:
                print(
                    '\tYou encounter Peeves the Poltergeist floating ahead of you. Seeing you, he blows a raspberry '
                    'and\n laughs, “Ooh look! There’s ickle Potter, as far as possible from his goal! But also more '
                    'than halfway there!”')
                Peeves_counter = 1
            elif Peeves_counter == 1:
                print(' Peeves is floating in front of you.')
            else:
                Encounter = False
                local_objects = ['hedge']

        if encounter_name == "Skrewt":
            if Skrewt_counter == 0:
                print(" \tYou find yourself facing a Blast-Ended Skrewt.", end="")
                if 'skrewt' not in local_objects:
                    local_objects = ['skrewt'] + local_objects
                if First_Skrewt == True:
                    if CS_counter > 0:
                        print(" Cedric was right – it’s enormous.")
                    print(
                        "\tTen feet long, it looks more like a giant scorpion than anything, with its long sting "
                        "curled over its\n back, its thick armor glinting in the light.")
                    First_Skrewt = False
                Skrewt_counter = 1
            elif Skrewt_counter == 1:
                print(
                    "The skrewt shoots a blast of fire from its end and flies forward towards you. You hastily "
                    "stumble backward.")
                Skrewt_counter = 2
            elif Skrewt_counter == 2:
                print(" The skrewt is nearly on top of you. As you try to evade it, you trip and fall to the ground.")
                Harry.status = 'under_Skrewt'
                Skrewt_counter = 3
            elif Skrewt_counter == 3:
                print(
                    "You feel a sharp pain in your leg, whether from fire or stinger, you cannot tell. You’re a bit "
                    "preoccupied\n with your predicament.")
                Harry.health -= 1
                if Harry.health <= 0:
                    finished = Endings("Killed by Skrewt")

    else:
        local_objects = ['hedge']

    # banner alerts, not full encounters
    if Harry.x == 4 and Harry.y == -8:
        if not Flobberworms_dead:
            print(" A pile of Flobberworms lies in the middle of the path, oozing sluggishly over each other.")
            if 'flobberworms' not in local_objects:
                local_objects = ['flobberworms'] + local_objects
        else:
            print(" A smoking crater containing bits of Flobberworm is in the middle of the path.")
    elif Harry.x == 10:  # mist
        if -7 <= Harry.y <= -5:
            if 'mist' not in local_objects:
                local_objects = ['mist'] + local_objects
            if Harry.y == -7 and Harry.compass == 1:
                print(" An odd golden mist is floating in the path ahead of you.")
            if Harry.y == -5:
                if Harry.compass == 3:
                    print(" An odd golden mist is floating in the path ahead of you.")
                elif Harry.compass == 2:
                    print(" An odd golden mist is floating in the path to your right.")
                elif Harry.compass == 4:
                    print(" An odd golden mist is floating in the path to your left.")
            if Harry.y == -6:
                if Mist_counter == 2:
                    print("""You take a deep breath and run through the enchanted mist.
                    The world turns upside down. You are hanging from the ground, hair on end, glasses dangling off your nose, threatening to fall into the bottomless sky. It feels as though your feet are glued to the grass, which is now the ceiling. Below you the dark, star-spangled heavens stretch endlessly. You feel as though if you tried to move one of your feet, you would fall away from the earth completely. """)
                else:
                    print(" The world is upside down.")
        Encounter = False
        Skrewt_counter = 0
    elif Harry.x == 5 and Harry.y == -12:
        if Harry.compass == 4:
            true_north = "to your right."
        elif Harry.compass == 3:
            true_north = "directly behind you."
        elif Harry.compass == 1:
            true_north = "directly in front of you."
        else:
            true_west = "to your left."
        print(" You see a bobbing light " + true_north)
        local_objects = ['hinkypunk'] + local_objects
        Encounter = False

    # CHOOSING AN ACTION
    chosen = False
    while not chosen:
        action = input(" What would you like to do? ")
        action = action.lower()
        if action == "menu" or action == "options":  # Options menu
            print(" forward \n right \n left \n back \n look \n wait \n cast spell \n speak \n")
            questions = input(
                "If you would like further explanation of your options, type 'Hermione'. Otherwise, type 'back' to "
                "return to the game.\n ")
            if questions == "'Hermione'" or questions == "Hermione" or questions == "hermione":
                print(
                    "forward: moves you forward one space. \n right: turns you to the right. \n left: turns you to "
                    "the left. \n back: turns you to face the opposite direction. \n look: gives you a choice of "
                    "things to look at. \n wait: do nothing for a turn. \n cast spell: gives you a choice of spells "
                    "to cast \n speak: gives you a choice of things to say.")
            else:
                pass  # Return to "what would you like to do?"
        else:
            chosen = True

    # SPELLS
    if action in spell_choices or "spell" in action or "cast" in action:
        if action in spell_choices:
            spell = action
        else:
            spell = input(" Which spell would you like to cast?\n " + " \n ".join(
                str(i + 1) + ". " + spell_choices[i].capitalize() for i in range(9)) + '\n')
        spell = spell.lower()
        pass_through = True
        general_attack = False
        if spell == "1" or spell == "lumos":
            Harry.cast_Lumos()
        elif spell == "2" or spell == "point me":
            print(Harry.cast_PointMe())

        elif spell == "3" or spell == "red sparks":
            which_rescuer = random.randint(1, 4)
            if which_rescuer == 1:
                rescuer = "Hagrid"
            elif which_rescuer == 2:
                rescuer = "Professor Moody"
            elif which_rescuer == 3:
                rescuer = "Professor McGonagall"
            elif which_rescuer == 4:
                rescuer = "Professor Flitwick"
            print(
                "You point your wand to the sky and send red sparks cascading upward. From outside the maze's walls,\n " + rescuer + " sees your distress signal and hurries to your aid.\n If you wish to be rescued, remain here.")
        else:  # combat spells
            print("What is your target?")
            for i in range(len(local_objects)):
                print(" " + str(i + 1) + ". " + local_objects[i])
            target = input()
            if target.isdigit():
                try:
                    target = local_objects[int(target) - 1]
                except:
                    target = ''
                    print("You do not seem able to count.")
            else:
                target = target.lower()
                if target not in local_objects:
                    print("You can't cast a spell on that right now.")
                    target = ''

            underside_hit = False
            if target == "skrewt" and encounter_name == "Skrewt":
                underside_chance = random.randint(1, 3)
                if underside_chance == 1:
                    underside_hit = True
                elif Harry.status == "under_Skrewt":
                    if underside_chance == 2:
                        underside_hit = True
                    elif Harry.health < 3:
                        underside_hit = True

            if spell == "4" or spell == "expelliarmus":
                if Encounter:
                    if encounter_name == "Cedric and Krum":
                        if Krum_status == "active":
                            if target == "cedric":
                                print(
                                    "As Cedric’s wand has already fallen from his twitching fingers, this spell has "
                                    "no effect.")
                                Harry.Cedric_relations -= 1
                                Cedric_status = "attacked"
                                pass_through = False
                            elif target == "krum":
                                if CK_counter == 1:
                                    print("You point your wand at Krum just as he looks up. Krum turns and runs.")
                                print(
                                    'You yell, “Expelliarmus!” The spell sends his wand flying out of his hand, '
                                    'but he keeps running, vanishing\n into the maze.')
                                Krum_status = "fled"
                                pass_through = False
                    elif encounter_name == 'Spider':
                        if target == "cedric" & Spider_counter > 1:
                            general_attack = True
                            pass_through = False
                        elif target == "spider":
                            if Spider_counter == 4:
                                print(
                                    'You raise your wand as the spider opens its pincers once more and shout, '
                                    '“Expelliarmus!”\n It works – the Disarming Spell makes the spider drop you, '
                                    'but that means you fall twelve feet onto your already injured leg, '
                                    'which crumples beneath you. Unable to run, you gaze up at the spider’s '
                                    'underbelly.')
                                Harry.status = 'under_Spider'
                            elif Spider_counter == 5:
                                print(" Sadly, the disarming spell only works if your target is holding something.")
                            else:
                                general_attack = True
                    elif underside_hit:  # Encounter is Skrewt
                        print(
                            "You successfully hit the Skrewt's unprotected underbelly. Unfortunately, however, "
                            "as Skrewts do not carry wands, your spell has no effect.")
                    elif target == encounter_name.lower():
                        general_attack = True

                if (not (Encounter and not pass_through)) and not general_attack:
                    if target == "cedric":
                        if encounter_name == "Cedric and Skrewt":
                            print(" The thing behind you turns out to be Cedric. ", end="")
                        Harry.attacking_Cedric(4)
                    elif target == "hedge":
                        print(" As the hedge does not have a wand, this spell has no effect.")
                    elif target == "flobberworms":
                        print(" As Flobberworms do not carry wands, this spell has no effect")


            elif spell == "5" or spell == "stupefy":
                if Encounter:
                    if encounter_name == "Cedric and Krum":
                        if Krum_status == 'active':
                            if target == "cedric":
                                print(
                                    'Your spell knocks Cedric out, saving him from further pain. Krum continues to '
                                    'cast Crucio for a moment\n before realizing that his victim is no longer '
                                    'screaming. He turns and runs.')
                                Harry.Cedric_relations -= 1
                                Krum_status = 'fled'
                                Cedric_status = 'unconscious'
                                pass_through = False
                            elif target == 'krum':
                                print(
                                    'You point your wand at Krum just as he looks up. Krum turns and runs. You yell, '
                                    '“Stupefy!” The spell hits\n Krum in the back. He stops in his tracks, '
                                    'falls forward, and lies motionless facedown.')
                                Krum_status = 'vanquished'
                    elif encounter_name == 'Spider':
                        if Spider_counter > 1:
                            general_attack = True
                            pass_through = False
                    elif underside_hit:  # Encounter is Skrewt
                        print(
                            "The skrewt is inches from you when it falls over – you managed to hit it on its fleshy, "
                            "shell-less underside.\n It won’t stay down for long, though.")
                        Encounter = False
                        Skrewt_counter = -1
                    elif target == encounter_name.lower():
                        general_attack = True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        if encounter_name == "Cedric and Skrewt":
                            print(" The thing behind you turns out to be Cedric. ", end="")
                        Harry.attacking_Cedric(5)
                    elif target == "hedge":
                        print(
                            "You attempt to stun the hedge. As hedges normally remain still, it is difficult to tell "
                            "whether your spell had any effect.")
                    elif target == "flobberworms":
                        print(
                            "You cast a stunning spell at the pile of Flobberworms. They stop wriggling and go limp. "
                            "That is, limper than they are normally.")

            elif spell == "6" or spell == "impedimenta":
                if Encounter:
                    if encounter_name == "Cedric and Krum":
                        if Krum_status == 'active':
                            if target == "cedric":
                                print(
                                    "Hit by your Impediment jinx, Cedric stops struggling for a moment, but continues "
                                    "to scream.")
                                Harry.Cedric_relations -= 1
                                Cedric_status = "attacked"
                                pass_through = False
                            elif target == "krum":
                                if CK_counter == 1:
                                    print(" You point your wand at Krum just as he looks up. Krum turns and runs.")
                                print(
                                    'You yell, “Impedimenta!” The spell hits Krum in the back, stopping him in his '
                                    'tracks. He spins and turns \ntoward you. He raises his wand threateningly '
                                    'towards you, then a confused look comes over his face. He \nturns his wand back '
                                    'towards Cedric and yells, “Crucio!”')
                    elif encounter_name == 'Spider':
                        # if target == "cedric":
                        #     if Spider_counter == 2:
                        if Spider_counter > 1:
                            general_attack = True
                            pass_through = False
                        # elif target == "spider":
                        #     general_attack == True
                    elif Encounter == 'Skrewt' and underside_hit == True:  # Encounter is Skrewt
                        print(
                            "The skrewt is inches from you when it freezes – you managed to hit it on its fleshy, "
                            "shell-less underside.\n It won’t stay down for long, though.")
                        Encounter = False
                        Skrewt_counter = -1
                    elif target == encounter_name.lower():
                        general_attack = True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        if encounter_name == "Cedric and Skrewt":
                            print(" The thing behind you turns out to be Cedric. ", end="")
                        Harry.attacking_Cedric(6)
                    elif target == "hedge":
                        print(
                            "You attempt to immobilize the hedge. As hedges normally remain still, it is difficult to "
                            "tell whether your spell had any effect.")
                    elif target == "flobberworms":
                        print(
                            "You immobilize the Flobberworms. They stop crawling and do nothing. As is usual for "
                            "Flobberworms.")

            elif spell == "7" or spell == "reducto":
                if Encounter == True:
                    if encounter_name == "Cedric and Krum":
                        if Harry.x == 7 and Harry.y == -9:
                            if target == "hedge":
                                print(
                                    "It isn’t very effective, but you manage to burn a small hole into the hedge, "
                                    "then force your way through.")
                                CK_counter = 0
                                Harry.y = -8
                                pass_through = False
                        if target == "cedric":
                            print(
                                'You point your wand at Cedric and yell, “Reducto!” The spell blasts Cedric away from '
                                'Krum. He lands several yards away and lies motionless, smoking slightly. Realizing '
                                'that his victim has been successfully incapacitated, Krum turns and runs.')
                            Harry.Cedric_relations -= 1
                            Krum_status = 'fled'
                            Cedric_status = 'unconscious'
                            pass_through = False
                        elif target == "krum":
                            if CK_counter == 1:
                                print(" You point your wand at Krum just as he looks up. Krum turns and runs.")
                            print(
                                'You yell, “Reducto!” The spell hits Krum in the back, blasting him off his feet. He '
                                'goes flying and lies\n motionless, smoking slightly.')
                            Krum_status = 'vanquished'
                    elif encounter_name == 'Spider':
                        # if target == "cedric":
                        #     if Spider_counter == 2:
                        #         general_attack = True
                        #         pass_through = False
                        # elif target == "spider":
                        if Spider_counter > 1:
                            general_attack = True
                            pass_through = False
                    elif Encounter == 'Skrewt' and underside_hit == True:  # Encounter is Skrewt
                        print(
                            "The skrewt is inches from you when it you blast it off its feet – you managed to hit it "
                            "on its fleshy, shell-less underside.\n It won’t stay down for long, though.")
                        Encounter = False
                        Skrewt_counter = -1
                    elif target == encounter_name.lower():
                        general_attack = True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        if encounter_name == "Cedric and Skrewt":
                            print(" The thing behind you turns out to be Cedric. ", end="")
                        Harry.attacking_Cedric(7)
                    elif target == "hedge":
                        print(" The hedge is too thick in this location to blast through.")
                    elif target == "flobberworms":
                        print(
                            "You cast Reducto at the flobberworms. This is a bit overkill, considering first that "
                            "Flobberworms are harmless\n and second that they can be killed by too much lettuce. "
                            "Blasting them to bits was not at all necessary.\n But you did it anyway.")
                        Flobberworms_dead = True

            elif spell == "8" or spell == "expecto patronum":
                if Encounter:
                    if encounter_name == "Cedric and Krum":
                        if target == "cedric":
                            print(
                                'You yell, “Expecto Patronum!” A silver stag bursts from your wand and charges at '
                                'Cedric. As he is not a\n Dementor, however, it has no effect.')
                            Harry.Cedric_relations -= 1
                            Cedric_status = 'attacked'
                            pass_through = False
                        elif target == "krum":
                            if CK_counter == 1:
                                print(" You point your wand at Krum just as he looks up. Krum turns and runs.")
                            print(
                                'You yell, “Expecto Patronum!” A silver stag bursts from your wand and charges at '
                                'Krum. As he is not a\n Dementor, however, he merely keeps running, vanishing into '
                                'the maze.')
                            Krum_status = 'fled'
                    elif encounter_name == "Sphinx":
                        if target == "sphinx":
                            print(
                                "Your Patronus charges straight through her with no effect. Actually, there is one "
                                "small side effect.\n She pounces on you.",
                                end="")
                            finished = Endings("Killed by Sphinx")
                    elif encounter_name == "Dementor":
                        if target == 'dementor':
                            print(
                                'You summon the happiest thought you can, concentrating with all your might on the '
                                'thought of getting out\n of the maze and celebrating with Ron and Hermione, '
                                'raise your wand, and shout, "Expecto Patronum!"\n A silver stag erupts from the end '
                                'of your wand and gallops towards the dementor, which falls back and trips\n over the '
                                'hem of its robes. . . . You have never seen a dementor stumble.\n Maybe it\s not a '
                                'real dementor, but only mimicking one.')
                    elif encounter_name == "Skrewt" and target == "Skrewt":
                        print(' Your Patronus has no effect on the Skrewt.')
                    elif encounter_name == 'Spider':
                        if target == "cedric" and Spider_counter > 1:
                            general_attack = True
                            pass_through = False
                        elif target == "spider":
                            print(" A spider is not a Dementor, so this spell is useless.")
                            if Spider_counter != 5:
                                general_attack = True
                    elif target == encounter_name.lower():
                        general_attack = True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        if encounter_name == "Cedric and Skrewt":
                            print(" The thing behind you turns out to be Cedric. ", end="")
                        Harry.attacking_Cedric(8)
                    elif target == "hedge":
                        print(" You send a Patronus at the hedge. It passes straight through with no effect.")
                    elif target == "flobberworms":
                        print(" You send a Patronus at the Flobberworms. They take no notice of it whatsoever.")

            elif spell == "9" or spell == "riddikulus":
                if Encounter:
                    if encounter_name == "Cedric and Krum":
                        if target == "cedric":
                            print(
                                'You yell, “Riddikulus!” The spell hits Cedric in the chest. As he is not a Boggart, '
                                'however, it has no effect.')
                            Harry.Cedric_relations -= 1
                            Cedric_status = 'attacked'
                            pass_through = False
                        elif target == "krum":
                            if CK_counter == 1:
                                print(" You point your wand at Krum just as he looks up. Krum turns and runs.")
                            print(
                                'You yell, “Riddikulus!” The spell hits Krum in the back. As he is not a Boggart, '
                                'however, he merely keeps\n running, vanishing into the maze.')
                            Krum_status = 'fled'
                    elif encounter_name == "Dementor":
                        if target == "dementor":
                            print(
                                '"Hang on!" you shout. "You\'re a Boggart! Riddikulus!" \n With a loud crack, '
                                'the shape-shifter explodes in a wisp of smoke.')
                            Boggle_counter = 4
                            Encounter = False
                    elif underside_hit == True:  # Encounter is Skrewt
                        print(
                            "You successfully manage to hit the Skrewt's unprotected underbelly. Unfortunately, "
                            "as it is not a Boggart,\n your spell has no effect.")
                    elif encounter_name == 'Spider':
                        if target == "cedric" and Spider_counter > 1:
                            general_attack = True
                            pass_through = False
                        elif target == "spider":
                            print(" A spider is not a Boggart, so this spell is useless.")
                            if Spider_counter != 5:
                                general_attack = True
                    elif target == encounter_name.lower():
                        general_attack = True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        if encounter_name == "Cedric and Skrewt":
                            print(" The thing behind you turns out to be Cedric. ", end="")
                        Harry.attacking_Cedric(9)
                    elif target == "hedge":
                        print(
                            "You may consider this maze your worst fear. However, it is not a Boggart and cannot be "
                            "dispelled by Riddikulus.")
                    elif target == "flobberworms":
                        print(" These Flobberworms are not Boggarts, so Riddikulus has no effect.")

            if general_attack:
                if encounter_name == "Sphinx":
                    print(
                        "Your spell bounces off her thick skin, with no effect. After all, sphinxes don't carry "
                        "wands. Actually, there is one\n small side effect. She pounces on you.",
                        end="")
                    finished = (Endings("Killed by Sphinx"))
                elif encounter_name == "Skrewt":
                    print(" The spell hits the skrewt's armor and rebounds. You duck just in time.")
                elif encounter_name == "Mist":
                    print(' The spell shoots straight through the mist, leaving it intact.')
                elif encounter_name == "Dementor":
                    print(" Your spell passes through the creature like vapor.")
                elif encounter_name == "Spider":
                    if target == "cedric":
                        if Spider_counter == 2:
                            if Harry.Cedric_relations < -1:
                                print(
                                    'Cedric dodges your spell and fires one back at you, parting your hair. Then, '
                                    'not looking where he is going,\n he runs straight into the oncoming spider.')
                                finished = Endings('Take the Cup Alone, you Jerk')
                            else:
                                print(
                                    'Cedric dodges your spell and turns around. “What –” he begins before the spider '
                                    'crashes straight into him.')
                                finished = Endings('Take the Cup Alone, you Jerk')
                        else:
                            if Harry.status == 'held' or Harry.status == 'under_Spider':
                                print(" It's kind of stupid to attack the only person who can help rescue you. ")
                                finished = Endings('Take the Cup, Cedric, you Jerk')
                            else:
                                print("You Slytherin, hitting a man while he's down. If your goal is to win the "
                                      "tournament, though, you succeeded.")
                                finished = Endings('Take the Cup Alone, you Jerk')
                    elif target == "spider":
                        if Spider_counter == 2:
                            print(
                                'The monster is out of range behind the hedge, so your spell flies wide, but your '
                                'action alerts Cedric to the danger.')
                            Cedric_status = 'warned'
                            Spider_counter = 3
                        elif Spider_counter == 3:
                            Harry.Cedric_relations += 1
                            print(
                                "\tYour spell hits the spider's gigantic, hairy black body, but for all the good it "
                                "does, you might\n as well have thrown a stone at it; the spider jerks, "
                                "scuttles around, and runs at you instead. \n\tYou continue casting spells at it, "
                                "but it’s no use - the spider is either so large, or so magical, that the\n spells "
                                "are doing no more than aggravating it. You have one horrifying glimpse of eight "
                                "shining black eyes\n and razor-sharp pincers before it is upon you. \n\tYou are "
                                "lifted into the air in its front legs; struggling madly, you try to kick it; your "
                                "leg connects\n with the pincers and next moment you are in excruciating pain.")
                            Harry.health -= 2
                            Harry.status = "held"
                            if Harry.health < 0:
                                finished = Endings("Killed by Spider")
                            if Harry.Cedric_relations < 1:
                                finished = Endings('Take the Cup, Cedric, you Jerk')
                            else:
                                print(
                                    'You can hear Cedric yelling “Stupefy!” but his spell has no more effect than '
                                    'yours.')
                                Spider_counter = 4
                        elif Spider_counter == 4:
                            print(
                                ' Your spell has no effect. Do you have any spell to make an opponent drop something? ')
                        elif Spider_counter == 5:
                            print(" Desperately, you aim high at the spider's underbelly and cast your spell", end="")
                            if Harry.Cedric_relations < 1:
                                print(". But, without Cedric's help, your magic is of no avail.")
                                finished = Endings('Take the Cup, Cedric, you Jerk')
                            else:
                                print(
                                    'just as Cedric shouts the same thing.\n The two spells combined do what one '
                                    'alone had not: The spider keels over sideways, flattening a nearby hedge, '
                                    'and strewing the path with a tangle of hairy legs. \n "Harry!" you hear Cedric '
                                    'shouting. "You all right? Did it fall on you?" \n "No," You call back, '
                                    'panting. "')
                                Spider_counter = 6
                elif encounter_name == "Hinkypunk":
                    print(" Your spell has no effect on the wispy creature.")
                elif encounter_name == "Peeves":
                    print(
                        "Your spell passes straight through the poltergeist. He makes a rude hand gesture and "
                        "vanishes.")
                    Peeves_counter = 2

    # MOVING
    if action == "go forward" or action == "forward" or action == "go right" or action == "right" or action == "go left" or action == "left" or action == "go back" or action == "back" or action == "f" or action == "b" or action == "l" or action == "r":
        action = action.replace("go ", "\0")
        action_abb = action[0]
        Harry.move(action_abb)
        print('')
        if Encounter:
            if encounter_name == "Sphinx":
                if Harry.x == 0:
                    print(
                        'You attempt to slip past the sphinx. But you have not yet answered the riddle. She pounces '
                        'on you.')
                    finished = Endings("Killed by Sphinx")
            elif encounter_name == "Hinkypunk":
                if action_abb == "b":
                    Encounter = False
            elif encounter_name == "Dementor":
                Boggle_counter += 1
            elif encounter_name == "Mist":
                if Harry.y == -6:
                    print('You take a deep breath and run through the enchanted mist. \n The world turns upside down.',
                          end='')
                    Harry.status = "Inverted"
                if Harry.status == "Inverted" and Harry.y != -6:
                    print(
                        '\tYou shut your eyes, so you can’t see the view of endless space below, and pull your right '
                        'foot as\t hard as you can away from the grassy ceiling. \n\t Immediately, the world rights '
                        'itself. You fall forward onto the wonderfully solid ground. You take a\n deep, '
                        'steadying breath, then get up again. The golden mist twinkles innocently at you in the '
                        'moonlight.')
                    Harry.status = "Normal"
                    Encounter = False
            elif encounter_name == "Skrewt":
                if action_abb == 'b':
                    Skrewt_counter = 0
                    Encounter = False
                elif action_abb == 'f':
                    Skrewt_counter += 1
            elif encounter_name == "Spider":
                if Spider_counter == 2:
                    if action_abb == "f":
                        print(
                            'You sprint forward. But, in your haste, you trip and your wand flies out of your hand as '
                            'a gigantic spider\n steps into the path and begins to bear down on you. You scramble to '
                            'retrieve it and find yourself directly\n under the spider, gazing up at its underbelly.')
                        Harry.status = 'under_Spider'
                        Spider_counter = 3
        rescuer = 0

    if action == "speak":
        if Encounter:
            if encounter_name == "Sphinx":
                wordChoice = 0
                while wordChoice == 0:
                    if Sph_counter == 0:
                        wordChoice = input(' 1. Ask her to move\n 2. Ask her how to pass.\n 3. Say "Spider"\n ')
                        wordChoice = wordChoice.lower()
                        if wordChoice == "3" or wordChoice == 'say "spider"' or wordChoice == "say spider":
                            print(' She pounces on you, shrieking, "Cheater! You haven\'t even heard the riddle yet!"')
                            finished = Endings("Killed by Sphinx")
                        else:
                            if wordChoice == "1" or wordChoice == "ask her to move":
                                print(
                                    'So … so will you move, please?” you say.\n “No,” she replies. “Not unless you '
                                    'can answer my riddle. Answer on your first guess - I let you pass. Answer\n '
                                    'wrongly - I attack. Remain silent - I will let you walk away from me unscathed.')
                                Sph_counter = 1
                            elif wordChoice == "2" or wordChoice == "ask her how to pass":
                                print(
                                    '“What do I have to do to pass you?” you ask.\n “Clever human,” she says. “You '
                                    'must answer my riddle, of course. Answer on your first guess - I let you pass.\n '
                                    'Answer wrongly - I attack. Remain silent - I will let you walk away from me '
                                    'unscathed.')
                                Sph_counter = 1
                            else:
                                print(' She says, "I couldn\'t understand that, foolish human. Try again."')
                                wordChoice = 0
                    if Sph_counter > 0:
                        if Sph_counter < 2:
                            wordChoice = input(' 1. Ask to hear the riddle \n 2. Never mind\n')
                            wordChoice = wordChoice.lower()
                            if wordChoice == "1" or wordChoice == "ask to hear the riddle":
                                print(
                                    '“Okay," you say. "Can I hear the riddle?" \n The sphinx sits down upon her hind '
                                    'legs, in the very middle of the path, and recites:\n“First think of the person '
                                    'who lives in disguise, Who deals in secrets and tells naught but lies. \n Next, '
                                    'tell me what\'s always the last thing to mend, The middle of middle and end of '
                                    'the end? \n And finally give me the sound often heard During the search for a '
                                    'hard-to-find word. \n Now string them together, and answer me this, '
                                    'Which creature would you be unwilling to kiss?"')
                                Sph_counter = 2
                            else:
                                print(' "Never mind," you say. The sphinx stares at you, smiling her mysterious smile.')
                        if Sph_counter >= 2:
                            wordChoice = input(' 1. Ask to hear the riddle. \n 2. Answer the riddle \n 3. Never mind\n')
                            wordChoice = wordChoice.lower()
                            if wordChoice == "1" or wordChoice == "ask to hear the riddle":
                                print(
                                    '“Can I hear the riddle again, please?" you ask." \n The sphinx blinks at you, '
                                    'smiles, and repeats the poem:\n“First think of the person who lives in disguise, '
                                    'Who deals in secrets and tells naught but lies. \n Next, tell me what\'s always '
                                    'the last thing to mend, The middle of middle and end of the end? \n And finally '
                                    'give me the sound often heard During the search for a hard-to-find word. \n Now '
                                    'string them together, and answer me this, Which creature would you be unwilling '
                                    'to kiss?"')
                            elif wordChoice == "2" or wordChoice == "answer the riddle":
                                riddle_response = input(" What is your answer? ")
                                if riddle_response == "spider" or riddle_response == "Spider":
                                    print(
                                        "The sphinx smiles more broadly. She gets up, stretches her front legs, "
                                        "and then moves aside for you to pass.")
                                    Encounter = False
                                    Sph_counter = 5
                                else:
                                    print(' "Wrong!" she shrieks, and pounces on you.', end="")
                                    finished = Endings("Killed by Sphinx")
                            else:
                                print(' “Never mind,” you say. The sphinx stares at you, smiling her mysterious smile.')
            elif encounter_name == "Spider":
                wordChoice = 0
                while wordChoice == 0:
                    if Spider_counter == 2:  # Spider seen, interacting w/ Cedric
                        wordChoice = input(' 1. Warn Cedric\n 2. Distract Cedric.\n ')
                        wordChoice = wordChoice.lower()
                        if wordChoice == "1" or wordChoice == "warn cedric":
                            print('“Cedric!” you yell. “On your left!”')
                            if Harry.Cedric_relations < -1:
                                print(' Cedric, not trusting you, hurries on. He runs straight into the spider.')
                                finished = Endings('Take the Cup Alone, you Jerk')
                            else:
                                Harry.Cedric_relations += 1
                                Cedric_status = 'warned'
                                Spider_counter = 3
                        else:
                            print('“Cedric!” you yell. “Look at me!”')
                            if Harry.Cedric_relations < -1:
                                print(' Cedric, not trusting you, hurries on. He runs straight into the spider.')
                                finished = Endings('Take the Cup Alone, you Jerk')
                            else:
                                print(
                                    'At your shout, Cedric turns around. “What –” he begins before the spider crashes '
                                    'straight into him.')
                                finished = Endings('Take the Cup Alone, you Jerk')
                    else:
                        wordChoice = 1
            elif encounter_name == "Peeves":
                print(' 1. Ask for directions\n 2. Ask him to explain\n 3. Threaten him with the Bloody Baron')
                choice = input()
                choice = choice.lower()
                if choice == '1' or choice == 'ask for directions' or choice == 'directions':
                    print(
                        '\t“Go that way,” he smirks, pointing in opposite directions. “Ooh, or cast pretty red sparks '
                        'to get out!\n You’d be safer. Don\'t say I didn\'t warn you!""')
                elif choice == '2' or choice == 'ask him to explain' or choice == 'explain':
                    print(
                        '\tHe cackles. “What makes you think I’ll explain anything to you, ickle Potter? But '
                        'remember, all that\n glitters is not gold. Beware false guides and false rewards!”')
                else:
                    print(
                        '\t"Peeves, I’ll tell the Bloody Baron on you!” you threaten.\n\t"Why should I care?” Peeves '
                        'whines. “He\n sent me here. You don’t have enough obstacles to face. They’re all '
                        'disappearing, including your competitors.”\n\t“So you’re just distracting me from the '
                        'maze?”\n\t“Exactly!” He grins evilly.')
            else:
                print(" You can't think of anything to say right now.")
        else:
            print(' "I\'m Harry Potter, Harry Harry Potter!"')

    # LOOKING
    if action == "look":
        print("What would you like to inspect? ")
        for i in range(len(local_objects)):
            print(" " + str(i + 1) + ". " + local_objects[i])
        target = input()
        if target.isdigit():
            try:
                target = local_objects[int(target) - 1]
            except:
                target = ''
                print("You do not seem able to count.")
        else:
            target = target.lower()
            if target not in local_objects:
                print("You can't look at that right now.")
                target = ''
        if target == "cedric":
            if encounter_name == "Cedric and Krum":
                if Krum_status == 'active':
                    print(
                        " Cedric is on the ground, twitching and screaming. Maybe you should do something about that.")
                elif Cedric_status == 'unconscious':
                    print(" Cedric is lying on the ground, unconscious.")
            else:
                print(" Cedric is a perfectly ordinary seventh-year Hufflepuff.")
        elif target == "krum":
            print(
                "On closer inspection, you realize that Krum's eyes seem glazed over, almost as though he were under "
                "the Imperius curse. Hmm.")
        elif target == "hedge":
            if Harry.x == 7 and Harry.y == -9:
                print(" The hedge seems to be thinner in this part of the maze.")
            else:
                print(
                    "The hedge seems a perfectly ordinary magical hedge growing out of a Quidditch field. *Perfectly "
                    "normal\n meaning normal for Hogwarts*")
        elif target == "sphinx":
            print(
                "The sphinx has the head of a woman, the body of a lion, and the riddle which holds your future. "
                "You\n should probably be polite to her.")
        elif target == "spider":
            print(
                "On closer inspection, you decide that this spider is not Aragog. It's not big enough. However, "
                "it is certainly\n one of his descendants, and it's certainly about to attack you. Why are you "
                "wasting your time looking at it?!")
        elif target == "mist":
            print(" You can see through the golden mist, but unfortunately cannot discern what it does.")
        elif target == "flobberworms":
            print(
                "You inspect a Flobberworm. It is a ten-inch long, toothless, brown magical worm. It is not a "
                "particularly interesting\n creature. Why you are looking at it this closely you do not know.")
        elif target == 'peeves':
            print(
                "Peeves is a little man with wickedly slanted, orange eyes, dressed in loud, outlandish clothes "
                "including a bell-covered hat and an orange bow tie.")

    # QUITTING
    if action == "quit":
        finished = True

    if action == "ludo":
        Harry.Bagman()

    # WAITING
    if action == "wait":
        if rescuer != 0:
            endingTitle = "Rescued by " + rescuer
            finished = Endings(endingTitle)

    if Encounter:  # Encounter endings
        if encounter_name == "Cedric and Krum":
            if Krum_status != 'active':
                if Cedric_status == 'friendly':
                    Harry.Cedric_relations += 2
                    print(
                        'You dash over to Cedric, who has stopped twitching and lies panting, his hands over his '
                        'face. “Are you all right?” you ask.\n "Yeah," pants Cedric. "Yeah ... I don\'t believe it... '
                        'he crept up behind me. ... I heard him, I turned around, and he had his wand on me. . . ." '
                        '\n Cedric gets up, still shaking.\n"I can\'t believe this ... I thought he was all right,'
                        '" you say.\n"So did I," agrees Cedric.')
                    if Fleur_attacked == True:
                        print(
                            '"Did you hear Fleur scream earlier?" you ask.\n"Yeah," says Cedric. "You don\'t think '
                            'Krum got her too?"')
                        newAction = 0
                        while newAction == 0:
                            newAction = input('1. Yes\n 2. Unsure\n')
                            if newAction == "1" or newAction == "Yes" or newAction == "yes":
                                print('"Definitely"')
                            elif newAction == "2" or newAction == "Unsure" or newAction == "unsure":
                                print('"I don\'t know"')
                    if Krum_status == 'vanquished':
                        print('"Should we leave him here?" Cedric mutters.')
                        newAction = 0
                        while newAction == 0:
                            newAction = input(' 1. Yes\n 2. No\n')
                            if newAction == "1" or newAction == "Yes" or newAction == "yes":
                                print(
                                    '“Yeah,” you say. “When the tournament’s over someone will come get him. And if a '
                                    'skrewt eats him in the\n meantime … he deserves it.”')
                            elif newAction == "2" or newAction == "No" or newAction == "no":
                                print(
                                    '“No,” you say. “I reckon we should send up red sparks. Someone\'ll come and '
                                    'collect him . . . otherwise\n he\'ll probably be eaten by a skrewt."\n"He\'d '
                                    'deserve it," Cedric mutters, but he raises his wand and shoots a shower of red '
                                    'sparks into the air, which hover high above Krum.')
                    print(
                        'You and Cedric stand together in the darkness for a moment. Then Cedric says, "Well... I '
                        's\'pose we\'d better go on. . . ."\n"What?" you say. "Oh . . . yeah . . . right. . ." '
                        '\nAfter all, you and Cedric are opponents. Cedric turns and walks off. His footsteps soon '
                        'die away.')
                    Encounter = False
                elif Cedric_status == 'attacked':
                    Harry.Cedric_relations += 1
                    print(
                        'You walk over to Cedric, who has stopped twitching and lies panting, his hands over his '
                        'face. “Are you all right?” you ask.\n“No thanks to you. What did you attack me for? Krum was '
                        'the aggressor!”')
                    newAction = 0
                    while newAction == 0:
                        newAction = input(' 1. Apologize\n 2. Defend your actions\n')
                        if newAction == "1" or newAction == "Apologize" or newAction == "apologize":
                            print(
                                '“I’m sorry,” you say. “It was an accident."\n"If your aim is really that bad, '
                                'it’s a wonder you’ve made it this far,” he says. “We’d better go on.”\n Cedric turns '
                                'and walks off. His footsteps soon die away.')
                        elif newAction == "2" or newAction == "Defend your actions" or newAction == "defend your actions":
                            print(
                                '“I couldn’t tell who was the aggressor," you say. "So I attacked both of '
                                'you.”\n“Seriously?” he growls. “If your judgment is really that bad, it’s a wonder '
                                'you’ve made it this far. I’m going on.” Cedric turns and walks off. His footsteps '
                                'soon die away.')
                            Harry.Cedric_relations -= 1
                        Encounter = False
                elif Cedric_status == 'unconscious':
                    if Krum_status == 'vanquished':
                        print('You stand victorious over the field, with two unconscious competitors at your feet.')
                    elif Krum_status == 'fled':
                        print('You stand victorious over the field, Krum fled and Cedric at your feet.')
                    Encounter = False
        elif encounter_name == "Spider":
            if not finished:
                if Spider_counter == 1 and Harry.y == -7:
                    print(' This is no time to delay! The cup’s right there!')
                    Harry.move("forward")
                elif Spider_counter == 2:
                    print(' Not seeing the spider, Cedric runs straight into it.')
                    finished = Endings('Take the Cup Alone, you Jerk')
                elif Spider_counter == 5:
                    print(' Your action was of no avail.')
                    print(" Underneath the spider, you are easy prey. It grabs you in its pincers once more.")
                    finished = Endings("Killed by Spider")
                elif Spider_counter == 6:
                    if Harry.health < 2:
                        print(
                            '\tYour leg is bleeding freely. You try to get up, but your leg is shaking badly and does '
                            'not want to\n support your weight. You lean against the hedge, gasping for breath, '
                            'and look around.')
                    print(
                        '\tCedric is standing feet from the Triwizard Cup, which gleams behind him. \n\t"Take it, '
                        'then," you pant to Cedric. "Go on, take it. You\'re there." ')
                    if Harry.Cedric_relations < 1:
                        finished = Endings('Take the Cup, Cedric, Please')
                    elif Harry.Cedric_relations < 2:
                        print(
                            '\tBut Cedric doesn’t move. He merely stands there, looking at you. Then he turns to '
                            'stare at the cup.\n You can see the longing expression on his face.')
                        finished = Endings('Take the Cup, Cedric, Please')
                    else:
                        print(
                            '\tHe looks around at you again and takes a deep breath.\n\t"You take it. You should win. '
                            'That''s twice you\'ve saved my neck in here." \n\t"That\'s not how it\'s supposed to '
                            'work," you say. “The one who reaches the cup first gets the points.\n That\'s you.',
                            end='')
                        if Harry.health < 2:
                            print(' I\'m telling you, I\'m not going to win any races on this leg."')
                        else:
                            print(' You’re right there."')
                        print(
                            '\tCedric takes a few paces nearer to the Stunned spider, away from the cup, shaking his '
                            'head. \n\t"No," he says. \n\t“Stop being noble," you say, irritably. "Just take it, '
                            'then we can get out of here." \n\t"You told me about the dragons," Cedric says. "I '
                            'would\'ve gone down in the first task if you hadn\'t\n told me what was coming." \n\t"I '
                            'had help on that too," you snap. "You helped me with the egg - we\'re square." \n\t"I '
                            'had help on the egg in the first place," says Cedric. \n\t"We\'re still square," you say',
                            end="")
                        if Harry.health < 2:
                            print(
                                ', testing your leg gingerly; it shakes violently as you put weight on it;\n '
                                'apparently your ankle is sprained.')
                        else:
                            print('.')
                        print(
                            '\t"You should\'ve got more points on the second task," says Cedric mulishly. "You stayed '
                            'behind to get\n all the hostages. I should\'ve done that." \n\t"I was the only one who '
                            'was thick enough to take that song seriously! Just take the cup!" \n\t"No," says Cedric. '
                            'He steps over the spider\'s tangled legs to join you. \n\t"Go on," he says. He looks\n '
                            'as though this costs him every ounce of resolution he has, but his face is set, '
                            'his arms are folded, he seems decided.')
                        wordChoice = input(' 1. Take the Cup Alone\n 2. Distract Cedric.\n ')
                        wordChoice = wordChoice.lower()
                        if wordChoice == "1" or wordChoice == "take the cup alone" or wordChoice == 'alone':
                            finished = Endings('Take the Cup Alone, at Cedric’s Prompting')
                        elif wordChoice == "2" or wordChoice == "give the cup to cedric" or wordChoice == "cedric":
                            print(
                                '\t“Cedric, I’m sick of the limelight,” you say. “I don’t deserve to be here, '
                                'didn’t want to be here, and\n definitely don’t need my face plastered all over the '
                                'Daily Prophet again. Hufflepuff House hasn’t had this\n kind of glory in centuries. '
                                'Go ahead. Take the cup. You deserve it.”\n\tAfter wrestling with himself, '
                                'Cedric reluctantly nods. “If you’re certain.” \n\t“I’m certain, Cedric. Go ahead.” ')
                            finished = Endings('Take the Cup, Cedric, Please')
                        else:
                            finished = Endings('Take the Cup Together')
