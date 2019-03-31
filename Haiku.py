#NP = 1-3
#PP = 2-4
#VP = 3-5

from random import randint, gauss
from copy import deepcopy

Theme = 'nature'

if Theme == 'normal':
    nouns = [
        ['case', 'book', 'brick', 'child', 'day', 'eye', 'fact', 'hand', 'home','job', 'life', 'lot', 'man', 'night', 'part', 'place', 'point', 'right','room', 'school', 'state', 'thing', 'time', 'tree', 'way', 'week', 'word', 'work','world', 'year'],
        ['apple','country', 'griffin', 'money', 'mother', 'number', 'people','problem', 'program', 'question', 'story', 'student', 'study', 'system','woman'],
        ['area', 'business', 'company', 'family', 'government']
        ]

    verbs = [
        ['adds', 'aims', 'asks', 'bakes', 'beats', 'begs', 'cares','chops', 'cooks', 'cuts', 'cries', 'does', 'eats', 'fails', 'flies','fits', 'folds', 'goes', 'grinds', 'sits','sleeps'],
        ['accepts', 'achieves', 'adapts','agrees', 'allows', 'appears', 'becomes', 'borrows', 'depends', 'deserves','exists', 'explains', 'dislikes', 'enjoys', 'follows', 'happens', 'hurries'],
        ['admires', 'announces','discovers', 'determines', 'enhances', 'finishes', 'hesitates', 'purifies']
        ]

    adjectives = [
        ['dull', 'drab', 'bad', 'blue', 'black', 'bored', 'bright','brave', 'calm', 'clear', 'cruel', 'dead', 'dark', 'fierce', 'fine', 'frail','good', 'hurt', 'ill', 'kind', 'long', 'nice', 'plain', 'poor', 'poised','proud', 'wrong', 'vast', 'tough', 'tame', 'tense', 'sore', 'shy', 'rich',
    'real', 'quaint'],
        ['alert', 'alive', 'angry', 'anxious', 'ashamed', 'awful','better', 'bloody', 'brainy', 'busy', 'careful', 'clever', 'cloudy', 'confused','crazy', 'creepy', 'grumpy', 'graceful', 'gorgeous', 'gentle', 'gifted','funny', 'friendly', 'frantic', 'foolish', 'filthy', 'fancy', 'evil', 'eager',
    'distinct', 'hungry', 'itchy', 'jealous', 'jolly', 'joyous', 'lonely','lovely', 'lucky', 'modern', 'mushy', 'muddy', 'nasty', 'nutty', 'ugly','tired', 'witty', 'worried', 'zany', 'upset', 'selfish'],
    ['annoying','arrogant', 'attractive', 'average', 'beautiful', 'breakable', 'colorful','combative', 'dangerous', 'determined', 'disgusted', 'enchanting','glamorous', 'important', 'innocent', 'jittery', 'motionless', 'obnoxious','worrisome', 'wandering', 'vivacious', 'unsightly', 'unusual', 'terrible',
    'successful', 'repulsive']
        ]

elif Theme == 'WM':
    nouns = [
        ['book', 'brick', 'Twamp', 'day', 'Flex', 'hand', 'dorm','job', 'life','meme', 'night', 'part', 'place','room', 'school', 'swamp', 'thing', 'time', 'week', 'word', 'work','world', 'year'],
        ['campus', 'coffee', 'griffin', 'freshman','homework', 'junior','senior','laptop', 'money', 'number','problem', 'program', 'question','roommate', 'story', 'student', 'system','squirrel'],
        ['old campus','new campus', 'business', 'bicycle','computer', 'dining hall', 'scholarship', 'schedule', 'family', 'library','tradition','sophomore','stress culture','professor']
        ]

    verbs = [
        ['adds', 'aims', 'asks', 'begs', 'cares', 'cries',  'eats', 'fails', 'folds', 'goes', 'grinds', 'reads', 'sits','sleeps','works'],
        ['accepts', 'achieves', 'adapts','agrees', 'allows', 'appears', 'borrows', 'depends', 'deserves','exists', 'explains', 'dislikes', 'enjoys', 'follows', 'happens', 'hurries','studies'],
        ['admires', 'announces','discovers', 'determines', 'enhances', 'finishes', 'hesitates']
        ]

    adjectives = [
        ['dull', 'green','gold', 'bored', 'bright','brave', 'calm', 'dead', 'dark', 'fierce', 'fine', 'good', 'ill', 'kind', 'long', 'nice', 'plain', 'poor', 'poised','proud', 'wrong', 'old', 'vast', 'tough', 'tense', 'shy', 'real', 'quaint'],
        ['alert', 'alive', 'anxious', 'ashamed', 'awful','better', 'brainy', 'busy', 'careful', 'clever', 'cloudy', 'confused','crazy', 'gentle', 'gifted','funny', 'friendly', 'frisky', 'foolish', 'eager', 'hungry', 'itchy', 'lonely','lovely', 'lucky', 'modern', 'muddy', 'nasty', 'nutty', 'ugly','tired', 'witty', 'worried', 'zany', 'upset', 'selfish'],
        ['annoying','arrogant', 'average', 'beautiful', 'determined', 'disgusted', 'important', 'innocent', 'obnoxious','worrisome', 'wandering', 'unusual', 'terrible','successful', 'repulsive']
        ]

elif Theme == 'nature':
    nouns = [
        ['bridge','child','moon', 'day','oak', 'eye','fly','bug','bear','leaf', 'fact', 'hand','snow', 'home','life', 'man', 'night', 'part', 'place', 'point', 'right','room', 'thing', 'time', 'sun','tree', 'stream','way', 'word','world', 'year'],
        ['apple','cherry','blossom','maple','insect','squirrel','willow','rabbit','country','flower', 'mother','problem', 'question', 'river', 'story','sunshine','woman'],
        ['area', 'ladybug', 'family','hummingbird','butterfly','cherry tree']
        ]

    verbs = [
        ['adds', 'aims', 'asks', 'beats', 'begs', 'cares','cuts', 'cries', 'does', 'lives', 'eats', 'fails', 'falls', 'flies','fits', 'folds', 'goes', 'sits','sleeps','rests'],
        ['accepts', 'achieves', 'adapts','agrees', 'allows', 'appears', 'becomes', 'borrows', 'depends', 'deserves','exists', 'explains', 'dislikes', 'enjoys', 'follows','searches', 'happens', 'hurries'],
        ['admires', 'announces','clarifies','discovers', 'determines', 'enhances', 'finishes', 'hesitates', 'purifies','rejoices']
        ]

    adjectives = [
        ['red','blue','green','yellow','brown','white', 'black', 'bored', 'bright','calm', 'clear', 'cruel', 'dead', 'dark', 'fierce', 'fresh','fine', 'frail','good', 'kind', 'long', 'nice', 'plain','proud', 'wrong', 'vast', 'tame', 'tense', 'wild', 'shy', 'real'],
        ['alert', 'alive', 'anxious', 'ashamed', 'awful','better','careful', 'clever', 'cloudy','sunny', 'confused','crazy', 'graceful', 'gentle', 'gifted', 'foolish', 'eager','distinct', 'hungry',  'joyous', 'lonely','lovely', 'lucky','muddy', 'nasty','selfish'],
        ['annoying','arrogant', 'attractive', 'average', 'beautiful','colorful','dangerous', 'enchanting','glorious', 'important', 'innocent','motionless', 'wandering', 'vivacious', 'unusual', 'terrible']
        ]

articles = ['the', 'a','no']

prepositions = [
    ['at', 'by', 'for', 'in', 'from', 'off', 'on','out', 'up', 'with', 'near', 'through', 'toward'],
    ['about', 'above','after', 'around', 'before', 'behind', 'below', 'onto', 'outside','over', 'throughout','under', 'inside', 'upon', 'up to', 'within'],
    ['because of','concerning', 'in spite of', 'instead of', 'in front of', 'excepting','regarding', 'underneath']
    ]




def line_builder(syllables_required):
    word_syllables = []
    syllables_left = syllables_required
    i = 0
    while syllables_left != 0:
        if syllables_left >3:
            word_syllables += [randint(1,3)]
        else:
            word_syllables += [randint(1,syllables_left)]
        syllables_left-= word_syllables[i]
        i+=1
    return word_syllables


def noun_phrase(sylable_outline):
    if len(sylable_outline) == 1:
        word1 = nouns[sylable_outline[0]-1][randint(0,len(nouns[sylable_outline[0]-1])-1)]
        return word1 #N
    elif len(sylable_outline) == 2:
        picker = 2
        if sylable_outline[0]==1:
            picker = randint(1,2)
            if picker == 1: #AA N
                word1 = articles[randint(0,len(articles)-1)]
                word2 = nouns[sylable_outline[1]-1][randint(0,len(nouns[sylable_outline[1]-1])-1)]
        if picker == 2: # Adj, N
            word1 = adjectives[sylable_outline[0]-1][randint(0,len(adjectives[sylable_outline[0]-1])-1)]
            word2 = nouns[sylable_outline[1]-1][randint(0,len(nouns[sylable_outline[1]-1])-1)]
        return word1 + " " + word2
    elif len(sylable_outline) == 3:
        picker = 2
        if sylable_outline[0] == 1:
            picker = randint(1,2)
            if picker == 1: #Starts with article
                word1 = articles[randint(0,len(articles)-1)]
                word2 = adjectives[sylable_outline[1]-1][randint(0,len(adjectives[sylable_outline[1]-1])-1)]
                word3 = nouns[sylable_outline[2]-1][randint(0,len(nouns[sylable_outline[2]-1])-1)]
        if picker == 2: #Adj, Adj, N
            word1 = adjectives[sylable_outline[0]-1][randint(0,len(adjectives[sylable_outline[0]-1])-1)]
            word2 = adjectives[sylable_outline[1]-1][randint(0,len(adjectives[sylable_outline[1]-1])-1)]
            word3 = nouns[sylable_outline[2]-1][randint(0,len(nouns[sylable_outline[2]-1])-1)]
        return (word1 + " " + word2 + " " + word3)

def prep_phrase(sylable_outline):
    word1 = prepositions[sylable_outline[0]-1][randint(0,len(prepositions[sylable_outline[0]-1])-1)]
    word2 = noun_phrase(sylable_outline[1:])
    return word1 + " " + word2

def verb_phrase(sylable_outline):
    word1 = verbs[sylable_outline[0]-1][randint(0,len(verbs[sylable_outline[0]-1])-1)]
    word2 = prep_phrase(sylable_outline[1:])
    return (word1 + " " + word2)

poem = ""
output_phrase = ""
INCOMPLETE = False

for i in range(3):
    if i !=1:
        syllable_outline = deepcopy(line_builder(5))
    else: syllable_outline = deepcopy(line_builder(7))


    if len(syllable_outline) == 2:
        picker = randint(1,2)
        if picker == 1: #N, V
            word1 = nouns[syllable_outline[0]-1][randint(0,len(nouns[syllable_outline[0]-1])-1)]
            word2 = verbs[syllable_outline[1]-1][randint(0,len(verbs[syllable_outline[1]-1])-1)]
            output_phrase = word1 + " " + word2
        elif picker == 2: #NP (2)
            output_phrase = noun_phrase(syllable_outline)

    elif len(syllable_outline) == 3:
        if INCOMPLETE == False:
            picker = randint(1,3)
            if picker == 1: #NP(2) V
                word1 = noun_phrase(syllable_outline[:2])
                word3 = verbs[syllable_outline[2]-1][randint(0,len(verbs[syllable_outline[2]-1])-1)]
                output_phrase = word1 + " " + word3
            elif picker == 2: #NP(3)   NOMINAL
                output_phrase = noun_phrase(syllable_outline)
                INCOMPLETE = True
            else: #Prep phrase (3)
                output_phrase = prep_phrase(syllable_outline)
        else: #V, PP(2)  VERBAL
            output_phrase = verb_phrase(syllable_outline)
            INCOMPLETE = False

    elif len(syllable_outline) == 4:
        if INCOMPLETE == False:
            picker = randint(1,4)
            if picker == 1: #NP (3), V
                word1 = noun_phrase(syllable_outline[:3])
                word4 = verbs[syllable_outline[3]-1][randint(0,len(verbs[syllable_outline[3]-1])-1)]
                output_phrase = word1 + " " + word4
            elif picker == 2: #PP(4)
                output_phrase = prep_phrase(syllable_outline)
            elif picker == 3: # N, VP (3)
                word1 = nouns[syllable_outline[0]-1][randint(0,len(nouns[syllable_outline[0]-1])-1)]
                word2 = verb_phrase(syllable_outline[1:])
                output_phrase = word1 + " " + word2
            elif picker == 4: #NP(2), PP(2)
                word1 = noun_phrase(syllable_outline[:2])
                word3 = prep_phrase(syllable_outline[2:])
                output_phrase = word1 + " " + word3
        else: #VP (4)
            output_phrase = verb_phrase(syllable_outline)
            INCOMPLETE = False

    elif len(syllable_outline) == 5:
        if INCOMPLETE == False:
            picker = randint(1,4)
            if picker == 1: #NP(2), VP(3)
                word1 = noun_phrase(syllable_outline[:2])
                word3 = verb_phrase(syllable_outline[2:])
                output_phrase = word1+ " " + word3
            elif picker == 2: #NP(1), VP(4)
                word1 = noun_phrase(syllable_outline[:1])
                word2 = verb_phrase(syllable_outline[1:])
                output_phrase = word1+ " " + word2
            elif picker == 3: #NP(2), PP(3)
                word1 = noun_phrase(syllable_outline[:2])
                word3 = prep_phrase(syllable_outline[2:])
                output_phrase = word1 + " " + word3
            elif picker == 4: #NP(1),PP(4)
                word1 = noun_phrase(syllable_outline[:1])
                word2 = prep_phrase(syllable_outline[1:])
                output_phrase = word1+ " " + word2
                INCOMPLETE = True
        else: #VP(5)
            output_phrase = verb_phrase(syllable_outline)
            INCOMPLETE = False

    elif len(syllable_outline) == 6:
        if INCOMPLETE == False:
            picker = randint(1,5)
            if picker == 1: #NP(3), VP(3)
                word1 = noun_phrase(syllable_outline[:3])
                word4 = verb_phrase(syllable_outline[3:])
                output_phrase = word1+ " " + word4
            elif picker == 2: #NP(2), VP(4)
                word1 = noun_phrase(syllable_outline[:2])
                word3 = verb_phrase(syllable_outline[2:])
                output_phrase = word1+ " " + word3
            elif picker == 3: #NP(1), VP(5)
                word1 = noun_phrase(syllable_outline[:1])
                word2 = verb_phrase(syllable_outline[1:])
                output_phrase = word1+ " " + word2
            elif picker == 4: #NP(3), PP(3)
                word1 = noun_phrase(syllable_outline[:3])
                word4 = prep_phrase(syllable_outline[3:])
                output_phrase = word1+ " " + word4
                INCOMPLETE = True
            elif picker == 5: #NP(2), PP(4)
                word1 = noun_phrase(syllable_outline[:2])
                word3 = prep_phrase(syllable_outline[2:])
                output_phrase = word1+ " " + word3
                INCOMPLETE = True
        else:
            picker = randint(1,2)
            if picker == 1: #V, PP(2), PP(3)
                word1 = verb_phrase(syllable_outline[:3])
                word4 = prep_phrase(syllable_outline[3:])
            else:#V, PP(3), PP(2)
                word1 = verb_phrase(syllable_outline[:4])
                word5 = prep_phrase(syllable_outline[4:])
            INCOMPLETE = False

    elif len(syllable_outline) == 7:
        if INCOMPLETE == False:
            picker = randint(1,3)
            if picker == 1: #NP(3), #VP(4)
                word1 = noun_phrase(syllable_outline[:3])
                word4 = verb_phrase(syllable_outline[3:])
                output_phrase = word1+ " " + word4
            elif picker == 2: #NP(2), #VP(5)
                word1 = noun_phrase(syllable_outline[:2])
                word3 = verb_phrase(syllable_outline[2:])
                output_phrase = word1+ " " + word3
            elif picker == 3: #NP(3), PP(4)
                word1 = noun_phrase(syllable_outline[:3])
                word4 = prep_phrase(syllable_outline[3:])
                output_phrase = word1+ " " + word4
                INCOMPLETE = True
        else:
            picker = randint(1,3)
            if picker == 1: #V, PP(2), PP(4)
                word1 = verb_phrase(syllable_outline[:3])
                word4 = prep_phrase(syllable_outline[3:])
            elif picker == 2:#V, PP(3), PP(3)
                word1 = verb_phrase(syllable_outline[:4])
                word5 = prep_phrase(syllable_outline[4:])
            else:#V, PP(4), PP(2)
                word1 = verb_phrase(syllable_outline[:5])
                word6 = prep_phrase(syllable_outline[5:])
            INCOMPLETE = False
    output_phrase = output_phrase.capitalize()
    poem += "\n" + output_phrase

print(poem)
