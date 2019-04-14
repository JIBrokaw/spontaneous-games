#Time taken: 1233
# Compass directions: 1-N, 2-E, 3-S, 4-W
import random

direction = 4
# HarryX = 12
# HarryY = 0

local_objects = ['hedge']

rescuer = 0
Encounter = False
encounter_name = "None"

Krum_status = "active"
Cedric_status = "friendly"


CK_counter = -2 # -2 = first overheard. -1 = continuous overheard. 0 = arrived. 1 = first seen. 2 = continuous seen
CK_ignored_counter = 0
Sph_counter = 0 # 0 = first seen. 1 = first spoken to. 2 = riddle heard
Spider_counter = 0
Fleur_attacked = False
finished = False

#stuff: 0,0 = cup. 1,-10 = sphinx.  2, -12 = skrewt.  2,-4 = post-skrewt Cedric.  3,-5 = Boggart.  4,-3 = skrewt.  4,-8 = flobberworms.  5, -12 = torch.  7,-5 = egg.  8,-9 = trigger C&K encounter.  9,-1 = skrewt. 10,-6 = mist. 12,-12 = Peeves

N_paths = [
    [True,True,True,True,True,False,True,True,False,False,False,False,False],
    [True,True,True,True,True,True,True,True,False,False,False,False,False],
    [True,False,True,True,True,False,False,True,False,False,True,False,True],
    [True,True,False,True,False,True,False,True,False,False,True,False,True],
    [True,True,True,True,False,True,True,False,True,False,True,True,True],
    [True,True,True,False,False,True,True,True,True,True,True,True,True],
    [True,True,True,True,True,True,False,True,False,False,True,True,True],
    [True,True,False,False,True,True,False,False,False,True,True,True,True],
    [True,True,False,False,False,True,False,False,True,True,True,False,False],
    [True,True,True,False,False,True,False,False,False,False,False,False,False],
    [True,False,False,False,False,False,False,False,False,True,False,True,True],
    [True,False,False,False,False,False,True,False,False,False,True,True,True],
    [False,True,False,True,False,True,True,True,False,False,False,True,True],
    [False,False,False,False,False,False,False,False,False,False,False,False,False]
]

W_paths = [
    [False,True,False,False,False,False,False,False,True,True,True,True,True,True],
    [False,True,False,False,False,False,True,False,False,True,True,False,True,False],
    [False,False,True,False,True,True,True,True,True,True,True,True,True,True,False],
    [False,False,False,False,True,False,False,False,False,False,True,False,False,False],
    [False,False,False,True,True,True,False,False,False,True,False,False,False,False],
    [False,False,False,False,True,False,False,True,True,False,True,True,False,False],
    [False,True,False,True,False,True,True,False,True,True,False,False,False,False],
    [False,False,False,True,True,False,False,True,True,False,False,False,True,False],
    [False,False,False,True,True,True,True,True,True,True,True,True,True,False],
    [False,False,False,True,True,False,True,True,True,True,True,True,False,False],
    [False,True,True,True,True,True,True,True,True,False,False,False,False,False],
    [False,False,True,True,True,True,False,False,True,True,True,True,False,False],
    [False,True,False,True,True,False,True,True,True,False,True,True,True,False]

]


def general_path_check(positionX,positionY,direction):
    if direction == 1 or direction == 5:
        return N_paths[abs(positionY)][positionX]
    elif direction == 2:
        return W_paths[abs(positionY)][positionX+1]
    elif direction == 3 or direction == -1:
        return N_paths[abs(positionY)+1][positionX]
    elif direction == 4 or direction == 0:
        return W_paths[abs(positionY)][positionX]

def explain_path_check(positionX,positionY,direction_facing):
    Left = general_path_check(positionX,positionY,direction_facing-1)
    Right = general_path_check(positionX,positionY,direction_facing+1)
    Back = general_path_check(positionX,positionY,direction_facing-2)
    Front = general_path_check(positionX,positionY,direction_facing)
    direction_option_list = [Front,Right,Left]
    open_path_list = []
    option_count = 0
    for i in range(3):
        if direction_option_list[i] == True:
            open_path_list.append(i)
            option_count +=1
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

class character():
    def __init__(self, name):
        self.name = name
        self.x = 9
        self.y = -9
        self.compass = 4
        self.Cedric_relations = 0
        self.health = 3
        self.status = "normal"

    def move(self, direction):
        #Rotate to face correct direction
        current_direction = self.compass
        if direction == "left":
            self.compass -=1
        elif direction == "right":
            self.compass +=1
            if self.compass >4:
                self.compass-=4
        elif direction == "back":
            self.compass-=2
        if self.compass <1:
            self.compass +=4
        #check for wall in the way
        if general_path_check(self.x,self.y,self.compass) == True:
            if self.compass == 1:
                self.y+=1
            elif self.compass == 2:
                self.x+=1
            elif self.compass == 3:
                self.y-=1
            elif self.compass == 4:
                self.x-=1
        else:
            print("You attempt to go "+ direction +", but there is a hedge in the way. Pay better attention to your surroundings!")
            self.compass = current_direction

    def activate_Encounter(self):
        if self.x == 1 and self. y == -10:
            if encounter_name != "Sphinx":
                return "Sphinx"
        # elif (self.x == 2 and self.y == -12) or (self.x == 4 and self.y == -3) or(self.x == 9 and self.y == -1):
        #     return "Skrewt"
        # elif self.x == 2 and self.y == -4:
        #     return "Cedric and Skrewt"
        # elif self.x == 3 and self.y == -5:
        #     return "Boggart"
        # elif self.x == 4 and self.y == -8:
        #     return "Flobberworms"
        # elif self.x == 5 and self.y == -12:
        #     return "Hinkypunk"
        # elif self.x == 7 and self.y == -5:
        #     return "Dragon Egg"
        elif self.x == 8 and self.y == -9 and CK_counter == -2:
            return "Cedric and Krum"
        # elif self.x == 10 and self.y == -6:
        #     return "Mist"
        # elif self.x == 12 and self.y == -12:
        #     return "Peeves"
        elif self.x == 0 and self.y == -7:
            return "Spider"
        else: return "None"


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
        pass

    def attacking_Cedric(self,spell):
        if spell == 4:
            self.Cedric_relations -=1
            print('You hit him with the Disarming Charm and his wand flies out of his hand. You catch it.\n')
            newAction = 0
            while newAction == 0:
                newAction = input('He stares at you. “I’d like my wand back, please.” \n 1. Yes\n 2. No.\n')
                if newAction == 1 or newAction == "Yes" or newAction =="yes":
                    print('“Sorry, Cedric. Here you go.”\n You return his wand.')
                elif newAction == 2 or newAction == "No" or newAction =="no":
                    newAction =2
                    print ('"No," you say. "I won its allegiance. Your wand is mine now."')
                else: newAction = 0
            if newAction == 2:
                self.Cedric_relations -=1
                newAction = 0
                while newAction == 0:
                    newAction = input('Cedric stares at you in disbelief. “Seriously, Harry? I need that wand to finish the tournament.”\n 1. Yes\n 2. No\n')
                    if newAction == 1 or newAction == "Yes" or newAction =="yes":
                        print('"You\'re right. I\'m sorry."\n You return his wand.')
                    elif newAction == 2 or newAction == "No" or newAction =="no":
                        self.Cedric_relations -=1
                        print('"I\’ll send up red sparks for you if you want." \n He stares at you in disgust. "You foul little – ! So that’s how we stand. I see."')
                        print('He suddenly lunges at you, knocking both wands out of your hand. In the ensuing struggle, his superior height and weight give him the advantage, so that he ends up with both wands. He traps you in a full Body-Bind, then drops your wand on your chest. \n “We Hufflepuffs are forgiving. So I’ll give you a second chance. This will wear off in a few minutes. But cross me again and I won’t be so nice.”\n He departs')
                    else: newAction = 0
        if spell > 4 and spell < 10:
            print('Your spell whizzes past his ear. He turns and stares at you in disbelief. ', end = '')
            if spell == 8:
                print('"I\'m not a Dementor!', end = " ")
            elif spell == 9:
                print('"I\'m not a Boggart!',end = ' ')
            elif self.Cedric_relations>-3:
                print('"',end = '')

            if self.Cedric_relations > -1:
                print('You git! Why are you attacking me?"')
            elif self.Cedric_relations > -3:
                print('My dad was right. There’s something wrong with you."')
                if self.Cedric_relations == -2:
                    print('He traps you in a full Body-Bind. “We Hufflepuffs are forgiving. So I’ll give you a second chance. This will wear off in a few minutes. But cross me again and I won’t be so nice.”')
            else:
                print ("He whips out his own wand and knocks you cold. You come to with McGonagall standing above you.")
                Endings("Rescued by Professor McGonagall")
            self.Cedric_relations -=1

Harry = character("Harry")

def Endings(title):
    Epilogue = "Nope"
    if title.startswith("Rescued"):
        if title == "Rescued by Hagrid":
            pass
        elif title == "Rescued by Professor Moody":
            pass
        elif title == "Rescued by Professor McGonagall":
            pass
        elif title == "Rescued by Professor Flitwick":
            pass

    elif title.startswith("Killed"):
        if title == "Killed by Spider":
            print(" You were killed by a spider")
            if Harry.Cedric_relations >= 0:
                Epilogue = "The Chosen One"
            else:
                Epilogue = "The Noseless One"
        else:
            if title == "Killed by Sphinx":
                print(" You are quickly torn to shreds by her fierce claws. Sphinxes have little tolerance for stupidity.")
            print("\tOvercome by your wounds, you die. Cedric comes upon your body and casts red sparks.")

            if Harry.Cedric_relations>0:
                Epilogue = "The Chosen One"
                print(" He remains at your side until McGonagall comes. At the death of a student, the tournament is immediately called off.")
                if Fleur_attacked == True:
                    print(" Because Fleur was already rescued and Krum was disqualified by using Dark Magic, Cedric wins by default.")
                else:
                    print(" Because Cedric was in the lead before this final task, he is declared the winner of the Triwizard Tournament.")
            else:
                print(" He then continues deeper into the maze. He never returns.", end = "")
                if Harry.Cedric_relations<0:
                    print(" Rumor has it has joined Voldemort’s followers.")
                    Epilogue = "The Noseless One"
                else:
                    Epilogue = "The Chosen One"
                    print(" Several days later, his body is found in a graveyard in Little Hangleton, with a gash in the crook of his elbow.")

    elif title.startswith("Take the Cup"):
        if title.startswith("Take the Cup Alone"):
            if title == "Take the Cup Alone, at Cedric's Prompting":
                print(" You look from Cedric to the cup. For one shining moment, you see yourself emerging from the maze, holding it. You see yourself holding the Triwizard Cup aloft, hear the roar of the crowd, see Cho's face shining with admiration.\n With difficulty, you limp to the cup, not wanting to accept any more of Cedric’s help than necessary. Reaching the cup, you grasp both handles at once. Instantly, you feel a jerk behind your navel. Your feet leave the ground. You cannot release your prize as the Cup pulls you onward in a howl of wind and swirling color, leading you to Voldemort.")
                print("\tTHE END")
                print(" You're selfish, but you saved Cedric's life.")
            if title == "Take the Cup Alone, you Jerk":
                print(" The spider seizes Cedric and carries him off. With the path now clear, you run towards the cup. Reaching it, you you grasp both handles at once. Instantly, you feel a jerk behind your navel. Your feet leave the ground. You cannot release your prize as the Cup pulls you onward in a howl of wind and swirling color, leading you to Voldemort.")
                print("\tTHE END")
                print(" You\'re selfish, and you didn\'t even save Cedric, you jerk.")

        if title.startswith("Take the Cup, Cedric"):
            if title == "Take the Cup, Cedric, Please":
                print(' "Cedric, I\'m sick of the limelight,” you say. “I don’t deserve to be here, didn’t want to be here, and definitely don’t need my face plastered all over the Daily Prophet again. Hufflepuff House hasn’t had this kind of glory in centuries. Go ahead. Take the cup. You deserve it.”\nAfter wrestling with himself, Cedric reluctantly nods. “If you’re certain." \n “I’m certain, Cedric. Go ahead.”\nHe walks up to the cup, stretches out his hands, then seizes the cup by both handles. Immediately, he and the cup disappear. Something is definitely very wrong with this tournament. \n As you stand there, wondering, someone comes up behind you. It is Professor Moody. “What happened?” he asks gruffly.\n“Cedric took the cup. But then he disappeared.” \n “I knew there was something fishy about this whole mess,” he growls. “Here, Potter. Lean on me. I’ll get you out of here.”\nAs you lean on him to get the weight off your damaged leg, he grips you firmly and suddenly everything goes black; you are being pressed very hard from all directions; you can’t breathe, there are iron bands tightening around your chest; your eyeballs are being forced back into your head; your eardrums are being pushed into your skull --\nYou arrive. Gulping great lungfuls of cold night air, you open your streaming eyes to see Cedric, dead on the ground. You are in a graveyard')
                print("\tTHE END")
                print(" Hufflepuff got its glory at last, shortly before its champion was killed. At least you tried.")
            if title == "Take the Cup, Cedric, You jerk":
                print(' You can hear Cedric running for the Cup as the spider carries you away and begins to swaddle you in sticky strands. It injects you with a paralyzer and you lose consciousness. \n You wake up hazily when someone brushes the web away from your face. It is Professor Moody. As you try to tell him what happened, he shushes you and says, “Don’t worry about that now. I’ll get you out of here first.” You suddenly feel as though you are being forced through a very tight rubber tube, and you lose consciousness again.')
                print(' You wake to find yourself still bound. But when you look down, you are no longer bound by webs, but ropes. There is a fresh cut in the crook of your elbow. As you blink blearily, you realize that you are in a graveyard. As you look more closely, you realize that Voldemort himself is standing in front of you, with a semicircle of Death Eaters behind him. Cedric stands among them. \n “Now untie him, Wormtail, and give him back his wand.” \n Wormtail approaches you, raises a silver hand, and slashes through your ropes. Still groggy from the poison, you crumple in a heap at the base of the tombstone. Someone places a wand in your hand, but your nerveless fingers cannot hold it.\nVoldemort laughs, high and cold. “See how spineless he really is. Avada Kedavra!”\nYou wake up in a strange misty emptiness that reminds you vaguely of King’s Cross Station. There is a small, ugly, naked, wounded creature nearby. Your father comes to you and asks whether you would like to go on or return to the world for a second chance.')
                action = input("1. Go on\n2. Return to life")
                if action == "1" or action == "go on" or action == "Go on":
                    print(' You choose to continue on, not to return to your life of pain. Not even J.K. Rowling knows what you find there.')
                else:
                    print(' You awaken on the ground and play dead. It seems that Voldemort, too, was briefly unconscious. Now he asks coldly. “Is the boy dead?” No one responds, so he orders, “You there. Examine him. Tell me whether he is dead." There is a bang and a gasp of pain.\nLong blond hair drifts over your face. Your heart thumps traitorously, and you know your inspector feels it. Lucius Malfoy leaps back and yells, “He’s alive!”\nYou struggle to rise to your feet and defend yourself, but are still too weak. Overwhelmed by the Death Eaters, you die ignominiously. This time you do not return.')
                Epilogue = "The Noseless One"
        elif title == "Take the Cup Together":
            print(' "Both of us," you say.\n"What?" Cedric asks.\n"We\'ll take it at the same time. It\'s still a Hogwarts victory. We\'ll tie for it."\nCedric stares at you. "You - you sure?"\n"Yeah," you say. "Yeah . . . we\'ve helped each other out, haven\'t we? We both got here. Let\'s just take it together."Cedric grins. "You\'re on. Come here."\nHe grabs your arm and helps you limp toward the plinth where the cup stands. You both hold a hand out over one of the cup\'s gleaming handles.\n"On three, right? One - two - three -" You both grasp a handle.\nInstantly, you feel a jerk somewhere behind your navel. Your feet leave the ground. You can’t unclench the hand holding the Triwizard Cup; it pulls you onward in a howl of wind and swirling color, Cedric at your side.')
            print("\tTHE END")
            print(" Nice job staying accurate to the story. Cedric’s going to die, but at least you know it all turns out right in the end.")
    if Epilogue != "Nope":
        if Epilogue == "The Chosen One":
            print(" Two years later, Dumbledore dies of a mysterious curse that withered his hand. Then, in a stunning coup, the Dark Lord takes over the Ministry and reveals himself returned to full power. Ron and Hermione drop out of school and go underground together. Rumor has it they are on Dumbledore’s last mission, searching for a way to kill Voldemort. The Order of the Phoenix frantically tries to reconstitute itself. However, without warning of Voldemort’s return and without Dumbledore’s leadership, half the members are killed before they establish a safe house. Voldemort is unstoppable until he tries to recruit Neville Longbottom, leader of a student resistance group, the Defense Alliance.\nVoldemort first encounters Neville in the Room of Requirement, asks him what he seeks, and offers him more power than he could dream of. Neville refuses, runs, and accidentally sets the room on fire. Several months later, Voldemort is meeting with Headmaster Snape in his office about the dissatisfactory performance of the Malfoys when Neville, Ginny, and Luna try to break in. Voldemort commends Neville on his courage and offers to train him as his second in command. Neville refuses and says he’ll only consider it if he can be Voldemort’s equal. Furious, Voldemort says no one is his equal, that to say so is as ridiculous as that old hat being equal to Nagini. He pulls the hat down over Neville’s eyes and orders Nagini to kill the three students. Neville pulls the sword of Gryffindor out of the hat, kills Nagini, and runs. Flying, Voldemort pursues him to the Hogwarts grounds, where he summons Dementors to attack Neville. But Neville performs the Patronus charm and the Dementors turn on their commander, who is unable to produce a Patronus, and suck out the last bit of his soul. Voldemort is defeated at last, by magic he knew not.")
            print("\tTHE END")
            print(" You're dead, but at least you destroyed the Horcrux within your scar. Good thing the prophecy had a spare.")
        elif Epilogue == "The Noseless One":
            print(" Two years later, Dumbledore dies of a mysterious curse that withered his hand. Then, in a stunning coup, the Dark Lord takes over the Ministry and reveals himself returned to full power. Ron and Hermione drop out of school and go underground together. Rumor has it they are on Dumbledore’s last mission, searching for a way to kill Voldemort. The Order of the Phoenix frantically tries to reconstitute itself. However, without warning of Voldemort’s return and without Dumbledore’s leadership, half the members are killed before they establish a safe house. In one such skirmish, Cedric Diggory kills Neville Longbottom, who is escorting Order Members into Hogwarts. Voldemort grows stronger and stronger until none can oppose him.")
            print("\tTHE END")
            print(" You’re dead and Voldemort won. You probably should have been nicer to Cedric.")

    return True

while finished == False:
    #check paths and give location update
    if Encounter == False or ((Harry.x != 8 or Harry.y != -8) and (Harry.x != 1 or Harry.y != -10) and (Harry.x != 0 or Harry.y <-7)):
        print(Harry.x)
        print(Harry.y)
        print(explain_path_check(Harry.x, Harry.y, Harry.compass))
    # check whether an encounter ought to be activated
    if Encounter == False:
        encounter_name = Harry.activate_Encounter()
        if encounter_name != "None":
            Encounter = True
    #If Encounter is activated, run Encounter description
    if Encounter == True:
        if encounter_name == "Cedric and Krum":
            if CK_counter == -2:
                if Harry.compass == 4:
                    true_north = "to your right"
                elif Harry.compass == 2:
                    true_north = "to your left"
                print(' The hedge ' + true_north + ' is thinner in this spot. You hear something in the path on the opposite side. Cedric’s voice is yelling, “What are you doing? What the hell d\'you think you\'re doing?" \n Then you hear Krum’s voice. "Crucio!" \n The air is suddenly full of Cedric\'s yells.')
                CK_counter = -1
            elif CK_counter == -1:
                if Harry.x == 8 and Harry.y == -8:
                    CK_counter = 0
                else:
                    print(" You continue to hear Cedric's yells, growing fainter.")
                    CK_ignored_counter +=1
                    if CK_ignored_counter == 14:
                        encounter_name = "None"
                        Encounter = False
            if CK_counter == 0:
                print("You see Cedric jerking and twitching on the ground, Krum standing over him.")
                local_objects = ['cedric'] + ['krum'] + local_objects
                CK_counter +=1

        elif encounter_name == "Sphinx":
            if Sph_counter == 0:
                print(' Ahead of you is a sphinx. It has the body of an over-large lion: great clawed paws and a long yellowish tail ending in a brown tuft, but it has the head of a woman. She turns her long, almond-shaped eyes upon you. However, she does not seem about to attack, but instead paces from side to side of the path, blocking your progress. Then she speaks in a deep, hoarse voice.\n "You are very near your goal. The quickest way is past me."')
                if 'Sphinx' not in local_objects:
                    local_objects = ['sphinx'] + local_objects
            elif Harry.x == 1 and Harry.y == -10:
                print(' The sphinx remains in the middle of the path, blocking your way forward.')

        elif encounter_name == "Spider":
            if Spider_counter == 0:
                print(' The Triwizard Cup is gleaming on a plinth a hundred yards away. Suddenly a dark figure hurtles out onto the path in front of you. It is Cedric, running for the cup.')
                local_objects = ['cedric'] + local_objects
                Spider_counter +=1
            elif Spider_counter ==1 and Harry.y == -6:
                print(' You charge forward, but Cedric is going to get there first. Cedric is sprinting as fast as he can toward the cup, and you have no chance of catching up; Cedric is much taller, with much longer legs.\n Then you see something immense over a hedge to your left, moving quickly along a path that intersects with your own; it is moving so fast Cedric is about to run into it, and Cedric, his eyes on the cup, has not seen it –')
                local_objects = ['spider'] + local_objects
                Spider_counter +=1
            elif Spider_counter == 3:
                print(" Cedric looks around just in time to hurl himself past the thing and avoid colliding with it, but in his haste he trips. Cedric’s wand flies out of his hand as a gigantic spider steps into the path and begins to bear down on him.")
            if Harry.status == "under_Spider":
                Spider_counter = 5

    else: local_objects = ['hedge']


    # CHOOSING AN ACTION
    chosen = False
    while chosen == False:
        action = input(" What would you like to do? ")
        action = action.lower()
        if action == "menu" or action == "options": #Options menu
            print(" forward \n right \n left \n back \n look \n wait \n cast spell \n speak \n")
            questions = input(" If you would like further explanation of your options, type 'Hermione'. Otherwise, type 'back' to return to the game.\n ")
            if questions == "'Hermione'" or questions == "Hermione" or questions == "hermione":
                print(" forward: moves you forward one space. \n right: turns you to the right. \n left: turns you to the left. \n back: turns you to face the opposite direction. \n look: gives you a choice of things to look at. \n wait: do nothing for a turn. \n cast spell: gives you a choice of spells to cast \n speak: gives you a choice of things to say.")
            else:
                pass #Return to "what would you like to do?"
        else:
            chosen = True

    #SPELLS
    if action == "cast spell" or action == "spell" or action == "cast":
        spell = input(" Which spell would you like to cast? \n 1. Lumos \n 2. Point Me \n 3. Red Sparks \n 4. Expelliarmus \n 5. Stupefy \n 6. Impedimenta \n 7. Reducto \n 8. Expecto Patronum \n 9. Riddikulus\n ")
        spell = spell.lower()
        pass_through = True
        general_attack = False
        if spell == "1" or spell == "lumos":
            pass
        elif spell == "2" or spell == "point me":
            print(Harry.cast_PointMe())
        elif spell == "3" or spell == "red sparks":
            which_rescuer = random.randint(1,4)
            if which_rescuer == 1:
                rescuer = "Hagrid"
            elif which_rescuer == 2:
                rescuer = "Professor Moody"
            elif which_rescuer == 3:
                rescuer = "Professor McGonagall"
            elif which_rescuer == 4:
                rescuer = "Professor Flitwick"
            print ("You point your wand to the sky and send red sparks cascading upward. From outside the maze's walls, " + rescuer + " sees your distress signal and hurries to your aid.\n If you wish to be rescued, remain here." )
        else: #combat spells
            print("What is your target?")
            for i in range(len(local_objects)):
                print(" " + str(i+1)+ ". " + local_objects[i])
            target = input()
            if target.isdigit() == True:
                try:
                    target = local_objects[int(target)-1]
                except:
                    target = ''
                    print("You do not seem able to count.")
            else:
                target = target.lower()
                if target not in local_objects:
                    print("You can't cast a spell on that right now.")
                    target = ''

            if spell == "4" or spell == "expelliarmus":
                if Encounter == True:
                    if encounter_name == "Cedric and Krum":
                        if Krum_status == "active":
                            if target == "cedric":
                                print("As Cedric’s wand has already fallen from his twitching fingers, this spell has no effect.")
                                Harry.Cedric_relations -=1
                                Cedric_status = "attacked"
                                pass_through = False
                            elif target == "krum":
                                if CK_counter == 1:
                                    print("You point your wand at Krum just as he looks up. Krum turns and runs.", end = "")
                                print('You yell, “Expelliarmus!” The spell sends his wand flying out of his hand, but he keeps running, vanishing into the maze.')
                                Krum_status = "fled"
                                pass_through = False
                    elif encounter_name == "Sphinx":
                        if target == "sphinx":
                            general_attack = True
                    elif encounter_name == 'Spider':
                        if target == "cedric":
                            if Spider_counter == 2:
                                general_attack = True
                                pass_through = False
                        elif target == "spider":
                            if Spider_counter == 4:
                                print(' You raise your wand as the spider opens its pincers once more and shout, “Expelliarmus!”\n It works – the Disarming Spell makes the spider drop you, but that means you fall twelve feet onto your already injured leg, which crumples beneath you. Unable to run, you gaze up at the spider’s underbelly.')
                                Harry.status = 'under_Spider'
                            elif Spider_counter == 5:
                                print(" Sadly, the disarming spell only works if your target is holding something.")
                            else:
                                general_attack == True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        Harry.attacking_Cedric(4)
                    elif target == "hedge":
                        print(" As the hedge does not have a wand, this spell has no effect.")


            elif spell == "5" or spell == "stupefy":
                if Encounter == True:
                    if encounter_name == "Cedric and Krum":
                        if Krum_status == 'active':
                            if target == "cedric":
                                print(' Your spell knocks Cedric out, saving him from further pain. Krum continues to cast Crucio for a moment before realizing that his victim is no longer screaming. He turns and runs.')
                                Harry.Cedric_relations -=1
                                Cedric_status = 'unconscious'
                                pass_through = False
                            elif target == 'krum':
                                print(' You point your wand at Krum just as he looks up. Krum turns and runs. You yell, “Stupefy!” The spell hits Krum in the back. He stops in his tracks, falls forward, and lies motionless facedown.')
                                Krum_status = 'vanquished'

                    elif encounter_name == "Sphinx":
                        if target == "sphinx":
                            general_attack = True

                    elif encounter_name == 'Spider':
                        if target == "cedric":
                            if Spider_counter == 2:
                                general_attack = True
                                pass_through = False
                        elif target == "spider":
                            general_attack == True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        Harry.attacking_Cedric(5)
                    elif target == "hedge":
                        print(" You attempt to stun the hedge. As hedges normally remain still, it is difficult to tell whether your spell had any effect.")

            elif spell == "6" or spell == "impedimenta":
                if Encounter == True:
                    if encounter_name == "Cedric and Krum":
                        if Krum_status == 'active':
                            if target == "cedric":
                                print(" Hit by your Impediment jinx, Cedric stops struggling for a moment, but continues to scream.")
                                Harry.Cedric_relations -=1
                                Cedric_status = "attacked"
                                pass_through = False
                            elif target == "krum":
                                if CK_counter == 1:
                                    print(" You point your wand at Krum just as he looks up. Krum turns and runs.", end = "")
                                print(' You yell, “Impedimenta!” The spell hits Krum in the back, stopping him in his tracks. He spins and turns toward you. He raises his wand threateningly towards you, then a confused look comes over his face. He turns his wand back towards Cedric and yells, “Crucio!”')
                    elif encounter_name == "Sphinx":
                        if target == "sphinx":
                            general_attack = True

                    elif encounter_name == 'Spider':
                        if target == "cedric":
                            if Spider_counter == 2:
                                general_attack = True
                                pass_through = False
                        elif target == "spider":
                            general_attack == True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        Harry.attacking_Cedric(6)
                    elif target == "hedge":
                        print(" You attempt to immobilize the hedge. As hedges normally remain still, it is difficult to tell whether your spell had any effect.")

            elif spell == "7" or spell == "reducto":
                if Encounter == True:
                    if encounter_name == "Cedric and Krum":
                        if Harry.x == 8 and Harry.y == -9:
                            if target == "hedge":
                                print(" It isn’t very effective, but you manage to burn a small hole into the hedge, then force your way through.")
                                CK_counter = 0
                                Harry.y = -8
                                pass_through = False
                        if target == "cedric":
                            print(' You point your wand at Cedric and yell, “Reducto!” The spell blasts Cedric away from Krum. He lands several yards away and lies motionless, smoking slightly. Realizing that his victim has been successfully incapacitated, Krum turns and runs.')
                            Harry.Cedric_relations -=1
                            Cedric_status = 'unconscious'
                            pass_through = False
                        elif target == "krum":
                            if CK_counter == 1:
                                print(" You point your wand at Krum just as he looks up. Krum turns and runs.", end = "")
                            print(' You yell, “Reducto!” The spell hits Krum in the back, blasting him off his feet. He goes flying and lies motionless, smoking slightly.')
                            Krum_status = 'vanquished'
                    elif encounter_name == "Sphinx":
                        if target == "sphinx":
                            general_attack = True

                    elif encounter_name == 'Spider':
                        if target == "cedric":
                            if Spider_counter == 2:
                                general_attack = True
                                pass_through = False
                        elif target == "spider":
                            general_attack == True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        Harry.attacking_Cedric(7)
                    elif target == "hedge":
                        print(" The hedge is too thick in this location to blast through.")

            elif spell == "8" or spell == "expecto patronum":
                if Encounter == True:
                    if encounter_name == "Cedric and Krum":
                        if target == "cedric":
                            print(' You yell, “Expecto Patronum!” A silver stag bursts from your wand and charges at Cedric. As he is not a Dementor, however, it has no effect.')
                            Harry.Cedric_relations -=1
                            Cedric_status = 'attacked'
                            pass_through = False
                        elif target == "krum":
                            if CK_counter == 1:
                                print(" You point your wand at Krum just as he looks up. Krum turns and runs.", end = "")
                            print(' You yell, “Expecto Patronum!” A silver stag bursts from your wand and charges at Krum. As he is not a Dementor, however, he merely keeps running, vanishing into the maze.')
                            Krum_status = 'fled'
                    if encounter_name == "Sphinx":
                        if target == "sphinx":
                            print(" Your Patronus charges straight through her with no effect. Actually, there is one small side effect. She pounces on you.", end = "")
                            finished = Endings("Killed by Sphinx")

                    elif encounter_name == 'Spider':
                        if target == "cedric":
                            if Spider_counter == 2:
                                general_attack = True
                                pass_through = False
                        elif target == "spider":
                            print(" A spider is not a Dementor, so this spell is useless.")
                            if Spider_counter != 5:
                                general_attack == True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        Harry.attacking_Cedric(8)
                    elif target == "hedge":
                        print(" You send a Patronus at the hedge. It passes straight through with no effect.")

            elif spell == "9" or spell == "riddikulus":
                if Encounter == True:
                    if encounter_name == "Cedric and Krum":
                        if target == "cedric":
                            print(' You yell, “Riddikulus!” The spell hits Cedric in the chest. As he is not a Boggart, however, it has no effect.')
                            Harry.Cedric_relations -=1
                            Cedric_status = 'attacked'
                            pass_through = False
                        elif target == "krum":
                            if CK_counter == 1:
                                print(" You point your wand at Krum just as he looks up. Krum turns and runs.", end = "")
                            print(' You yell, “Riddikulus!” The spell hits Krum in the back. As he is not a Boggart, however, he merely keeps running, vanishing into the maze.')
                            Krum_status = 'fled'

                    if encounter_name == "Sphinx":
                        if target == "sphinx":
                            general_attack = True

                    elif encounter_name == 'Spider':
                        if target == "cedric":
                            if Spider_counter == 2:
                                general_attack = True
                                pass_through = False
                        elif target == "spider":
                            print (" A spider is not a Boggart, so this spell is useless.")
                            if Spider_counter !=5:
                                general_attack == True

                if (Encounter == False or pass_through == True) and general_attack == False:
                    if target == "cedric":
                        Harry.attacking_Cedric(6)
                    elif target == "hedge":
                        print(" You may consider this maze your worst fear. However, it is not a Boggart and cannot be dispelled by Riddikulus.")

            if general_attack == True:
                if encounter_name == "Sphinx":
                    print("Your spell bounces off her thick skin, with no effect. After all, sphinxes don't carry wands. Actually, there is one small side effect. She pounces on you.", end = "")
                    finished = (Endings("Killed by Sphinx"))
                elif encounter_name == "Spider":
                    if target == "cedric":
                        if Spider_counter == 2:
                            if Harry.Cedric_relations < -1:
                                print('Cedric dodges your spell and fires one back at you, parting your hair. Then, not looking where he is going, he runs straight into the oncoming spider.')
                                finished = Endings('Take the Cup Alone, you Jerk')
                            else:
                                print('Cedric dodges your spell and turns around. “What –” he begins before the spider crashes straight into him.')
                                finished = Endings('Take the Cup Alone, you Jerk')
                        elif Cedric_status == 'warned':
                            print(" You Slytherin, hitting a man while he's down. If your goal is to win the tournament, though, you succeeded.")
                            finished = Endings('Take the Cup Alone, you Jerk')
                    elif target == "spider":
                        if Spider_counter == 2:
                            print(' The monster is out of range behind the hedge, so your spell flies wide, but your action alerts Cedric to the danger.')
                            Cedric_status = 'warned'
                            Spider_counter = 3
                        elif Spider_counter == 3:
                            Harry.Cedric_relations +=1
                            print(" Your spell hits the spider's gigantic, hairy black body, but for all the good it does, you might as well have thrown a stone at it; the spider jerks, scuttles around, and runs at you instead. \n You continue casting spells at it, but it’s no use - the spider is either so large, or so magical, that the spells are doing no more than aggravating it. You have one horrifying glimpse of eight shining black eyes and razor-sharp pincers before it is upon you. \n You are lifted into the air in its front legs; struggling madly, you try to kick it; your leg connects with the pincers and next moment you are in excruciating pain.")
                            Harry.health -=2
                            if Cedric_relations < 1:
                                finished = Endings('Take the Cup, Cedric, you Jerk')
                            else:
                                print(' You can hear Cedric yelling “Stupefy!” but his spell has no more effect than yours.')
                                Spider_counter = 4
                        elif Spider_counter == 4:
                            print(' Your spell has no effect')
                        elif Spider_counter == 5:
                            print(" Desperately, you aim high at the spider's underbelly and cast your spell",end = "")
                            if Harry.Cedric_relations <1:
                                print(". But, without Cedric's help, your magic is of no avail.")
                                finished = Endings('Take the Cup, Cedric, you Jerk')
                            else:
                                print(' just as Cedric shouts the same thing. The two spells combined do what one alone had not: The spider keels over sideways, flattening a nearby hedge, and strewing the path with a tangle of hairy legs. \n "Harry!" you hear Cedric shouting. "You all right? Did it fall on you?" \n "No," You call back, panting. "')
                                Spider_counter = 6




    #MOVING
    if action == "go forward" or action == "forward" or action == "go right" or action == "right" or action == "go left" or action == "left" or action == "go back" or action == "back":
        action = action.replace("go ","\0")
        Harry.move(action)
        print('')
        if Encounter == True:
            if encounter_name == "Spider":
                if Spider_counter == 2:
                    if action == "forward":
                        print(' You sprint forward. But, in your haste, you trip and your wand flies out of your hand as a gigantic spider steps into the path and begins to bear down on you. You scramble to retrieve it and find yourself directly under the spider, gazing up at its underbelly.')
                        Harry.status = under_Spider
                        Spider_counter = 3
        rescuer = 0

    if action == "speak":
        if Encounter == True:
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
                                print(' So … so will you move, please?” you say.\n “No,” she replies. “Not unless you can answer my riddle. Answer on your first guess - I let you pass. Answer wrongly - I attack. Remain silent - I will let you walk away from me unscathed.')
                                Sph_counter = 1
                            elif wordChoice == "2" or wordChoice == "ask her how to pass":
                                print(' “What do I have to do to pass you?” you ask.\n “Clever human,” she says. “You must answer my riddle, of course. Answer on your first guess - I let you pass. Answer wrongly - I attack. Remain silent - I will let you walk away from me unscathed.')
                                Sph_counter =1
                            else:
                                print(' She says, "I couldn\'t understand that, foolish human. Try again."')
                                wordChoice == 0
                    if Sph_counter > 0:
                        if Sph_counter < 2:
                            wordChoice = input(' 1. Ask to hear the riddle \n 2. Never mind\n')
                            wordChoice = wordChoice.lower()
                            if wordChoice == "1" or wordChoice == "ask to hear the riddle":
                                print(' “Okay," you say. "Can I hear the riddle?" \n The sphinx sits down upon her hind legs, in the very middle of the path, and recites:\n“First think of the person who lives in disguise, Who deals in secrets and tells naught but lies. \n Next, tell me what\'s always the last thing to mend, The middle of middle and end of the end? \n And finally give me the sound often heard During the search for a hard-to-find word. \n Now string them together, and answer me this, Which creature would you be unwilling to kiss?"')
                                Sph_counter = 2
                            else:
                                print(' "Never mind," you say. The sphinx stares at you, smiling her mysterious smile.')
                        if Sph_counter >=2:
                            wordChoice = input(' 1. Ask to hear the riddle. \n 2. Answer the riddle \n 3. Never mind\n')
                            wordChoice = wordChoice.lower()
                            if wordChoice == "1" or wordChoice == "ask to hear the riddle":
                                print(' “Can I hear the riddle again, please?" you ask." \n The sphinx blinks at you, smiles, and repeats the poem:\n“First think of the person who lives in disguise, Who deals in secrets and tells naught but lies. \n Next, tell me what\'s always the last thing to mend, The middle of middle and end of the end? \n And finally give me the sound often heard During the search for a hard-to-find word. \n Now string them together, and answer me this, Which creature would you be unwilling to kiss?"')
                            elif wordChoice == "2" or wordChoice == "answer the riddle":
                                riddle_response = input(" What is your answer? " )
                                if riddle_response == "spider" or riddle_response == "Spider":
                                    print(" The sphinx smiles more broadly. She gets up, stretches her front legs, and then moves aside for you to pass.")
                                    Encounter = False
                                else:
                                    print(' "Wrong!" she shrieks, and pounces on you.', end = "")
                                    finished = Endings("Killed by Sphinx")
                            else:
                                print(' “Never mind,” you say. The sphinx stares at you, smiling her mysterious smile.')
            elif encounter_name == "Spider":
                wordChoice = 0
                while wordChoice == 0:
                    if Spider_counter == 2: #Spider seen, interacting w/ Cedric
                        wordChoice = input(' 1. Warn Cedric\n 2. Distract Cedric.\n ')
                        wordChoice = wordChoice.lower()
                        if wordChoice == "1" or wordChoice == "warn cedric":
                            print('“Cedric!” you yell. “On your left!”')
                            if Harry.Cedric_relations < -1:
                                print(' Cedric, not trusting you, hurries on. He runs straight into the spider.')
                                finished = Endings('Take the Cup Alone, you Jerk')
                            else:
                                Harry.Cedric_relations +=1
                                Cedric_status = 'warned'
                                Spider_counter = 3
                        else:
                            print('“Cedric!” you yell. “Look at me!”')
                            if Harry.Cedric_relations < -1:
                                print(' Cedric, not trusting you, hurries on. He runs straight into the spider.')
                                finished = Endings('Take the Cup Alone, you Jerk')
                            else:
                                print(' At your shout, Cedric turns around. “What –” he begins before the spider crashes straight into him.')
                                finished = Endings('Take the Cup Alone, you Jerk')
                    else:
                        wordChoice = 1
            else print(" You can't think of anything to say right now.")
        else:
            print(' "I\'m Harry Potter, Harry Harry Potter!"')



    #QUITTING
    if action == "quit":
        finished = True

    #WAITING
    if action == "wait":
        if rescuer != 0:
            endingTitle = "Rescued by " + rescuer
            finished = Endings(endingTitle)

    if Encounter == True: #Encounter endings
        if encounter_name == "Cedric and Krum":
            if Krum_status != 'active':
                if Cedric_status == 'friendly':
                    Harry.Cedric_relations +=2
                    print('You dash over to Cedric, who has stopped twitching and lies panting, his hands over his face. “Are you all right?” you ask.\n "Yeah," pants Cedric. "Yeah ... I don\'t believe it... he crept up behind me. ... I heard him, I turned around, and he had his wand on me. . . ." \n Cedric gets up, still shaking.\n"I can\'t believe this ... I thought he was all right," you say.\n"So did I," agrees Cedric.')
                    if Fleur_attacked == True:
                        print('"Did you hear Fleur scream earlier?" you ask.\n"Yeah," says Cedric. "You don\'t think Krum got her too?"')
                        newAction = 0
                        while newAction == 0:
                            newAction = input('1. Yes\n 2. Unsure\n')
                            if newAction == "1" or newAction == "Yes" or newAction =="yes":
                                print('"Definitely"')
                            elif newAction == "2" or newAction == "Unsure" or newAction =="unsure":
                                print('"I don\'t know"')
                    if Krum_status == 'vanquished':
                         print('"Should we leave him here?" Cedric mutters.')
                         newAction = 0
                         while newAction == 0:
                             newAction = input('1. Yes\n 2. No\n')
                             if newAction == "1" or newAction == "Yes" or newAction =="yes":
                                 print('“Yeah,” you say. “When the tournament’s over someone will come get him. And if a skrewt eats him in the meantime … he deserves it.”')
                             elif newAction == "2" or newAction == "No" or newAction =="no":
                                 print('“No,” you say. “I reckon we should send up red sparks. Someone\'ll come and collect him . . . otherwise he\'ll probably be eaten by a skrewt."\n"He\d deserve it," Cedric mutters, but he raises his wand and shoots a shower of red sparks into the air, which hover high above Krum.')
                    print('You and Cedric stand together in the darkness for a moment. Then Cedric says, "Well... I s\'pose we\'d better go on. . . ."\n"What?" you say. "Oh . . . yeah . . . right. . ." \nAfter all, you and Cedric are opponents. Cedric turns and walks off. His footsteps soon die away.')
                    Encounter = False
                elif Cedric_status == 'attacked':
                    Harry.Cedric_relations +=1
                    print('You walk over to Cedric, who has stopped twitching and lies panting, his hands over his face. “Are you all right?” you ask.\n“No thanks to you. What did you attack me for? Krum was the aggressor!”')
                    newAction = 0
                    while newAction == 0:
                        newAction = input('1. Apologize\n 2. Defend your actions\n')
                        if newAction == "1" or newAction == "Apologize" or newAction =="apologize":
                           print('“I’m sorry,” you say. “It was an accident."\n"If your aim is really that bad, it’s a wonder you’ve made it this far,” he says. “We’d better go on.”\n Cedric turns and walks off. His footsteps soon die away.')
                       elif newAction == "2" or newAction == "Defend your actions" or newAction =="defend your actions":
                           print('“I couldn’t tell who was the aggressor," you say. "So I attacked both of you.”\n“Seriously?” he growls. “If your judgment is really that bad, it’s a wonder you’ve made it this far. I’m going on.” Cedric turns and walks off. His footsteps soon die away.')
                           Harry.Cedric_relations -=1
                        Encounter = False
                elif Cedric_status == 'unconscious':
                   if Krum_status == 'vanquished':
                       print('You stand victorious over the field, with two unconscious competitors at your feet.')
                   elif Krum_status == 'fled':
                       print('You stand victorious over the field, Krum fled and Cedric at your feet.')
                   Encounter = False
        if encounter_name == "Spider":
            if finished == False:
                if Spider_counter == 1 and Harry.y == -7:
                    print(' This is no time to delay! The cup’s right there!')
                    Harry.move("forward")
                elif Spider_counter == 2:
                    print(' Not seeing the spider, Cedric runs straight into it.')
                    finished = Endings('Take the Cup Alone, you Jerk')
                elif Spider_counter == 5:
                    print(' Your action was of no avail.')
                    finished = Endings("Killed by Spider")
                elif Spider_counter == 6:
                    if Harry.health <2:
                        print(' Your leg is bleeding freely. You try to get up, but your leg is shaking badly and does not want to support your weight. You lean against the hedge, gasping for breath, and look around.')
                    print(' Cedric is standing feet from the Triwizard Cup, which gleams behind him. \n "Take it, then," you pant to Cedric. "Go on, take it. You\'re there." ')
                    if Harry.Cedric_relations <1:
                        finished = Endings('Take the Cup, Cedric, Please')
                    elif Harry.Cedric_relations <2:
                        print(' But Cedric doesn’t move. He merely stands there, looking at you. Then he turns to stare at the cup. You can see the longing expression on his face.')
                        finished = Endings('Take the Cup, Cedric, Please')
                    else:
                        print(' He looks around at you again and takes a deep breath.  \n "You take it. You should win. That''s twice you\'ve saved my neck in here." \n "That\'s not how it\'s supposed to work," you say. “The one who reaches the cup first gets the points. That\'s you.' , end = '')
                        if Harry.health <2:
                            print(' I\'m telling you, I\'m not going to win any races on this leg."')
                        else: print(' You’re right there."')
                        print('	Cedric takes a few paces nearer to the Stunned spider, away from the cup, shaking his head. \n "No," he says. \n “Stop being noble," you say, irritably. "Just take it, then we can get out of here." \n "You told me about the dragons," Cedric says. "I would\'ve gone down in the first task if you hadn\'t told me what was coming." \n "I had help on that too," you snap. "You helped me with the egg - we\'re square." \n "I had help on the egg in the first place," says Cedric. \n "We\'re still square," you say', end = "")
                        if Harry.health < 2:
                            print(', testing your leg gingerly; it shakes violently as you put weight on it; apparently your ankle is sprained.')
                        else: print('.')
                        print(' "You should\'ve got more points on the second task," says Cedric mulishly. "You stayed behind to get all the hostages. I should\'ve done that." \n "I was the only one who was thick enough to take that song seriously! Just take the cup!" \n "No," says Cedric. He steps over the spider\'s tangled legs to join you. \n "Go on," he says. He looks as though this costs him every ounce of resolution he has, but his face is set, his arms are folded, he seems decided.')
                        wordChoice = input(' 1. Take the Cup Alone\n 2. Distract Cedric.\n ')
                        wordChoice = wordChoice.lower()
                        if wordChoice == "1" or wordChoice == "take the cup alone" or wordChoice == 'alone':
                            finished = Endings('Take the Cup Alone, at Cedric’s Prompting')
                        elif wordChoice == "2" or wordChoice == "give the cup to cedric" or wordChoice == "cedric":
                            print(' “Cedric, I’m sick of the limelight,” you say. “I don’t deserve to be here, didn’t want to be here, and definitely don’t need my face plastered all over the Daily Prophet again. Hufflepuff House hasn’t had this kind of glory in centuries. Go ahead. Take the cup. You deserve it.”\n After wrestling with himself, Cedric reluctantly nods. “If you’re certain.” \n “I’m certain, Cedric. Go ahead.” ')
                            finished = Endings('Take the Cup, Cedric, Please')
                        else:
                            finished = Endings('Take the Cup Together')
