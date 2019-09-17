#!/usr/bin/env python3

import sys, logging, os, json

version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Players need to Shower, Brush Teeth, Take Medicine, Wash Face, Do Makeup, Style Hair, and Get Dressed, in that order


# Game loop functions
def render(game,current,moves):
    ''' Displays the current room, moves '''
    r = game['rooms']
    c = r[current]

    print('\n\nMoves: {moves}'.format(moves=moves))
    print('\n\n{name}'.format(name=c['name']))
    print(c['desc'])
    if len(c['inventory'])>0:
        print('You have done the following things:')

def getInput(game,current,verbs):
    ''' Asks the user for input and normalizes the inputted value. Returns a list of commands '''

    toReturn = input('\nWhat would you like to do? ').strip().upper().split()
    if (len(toReturn)):
        #assume the first word is the verb
        toReturn[0] = normalizeVerb(toReturn[0],verbs)
    return toReturn


def update(selection,game,current,inventory):
    ''' Process the input and update the state of the world '''
    s = list(selection)[0]  #We assume the verb is the first thing typed\
    
    if s == "":
        print("\nSorry, I don't understand.")
        return current

    elif s == 'EXITS':
        printExits(game,current)
        return current

#Actions needed to complete game; genuinely couldn't get them to work in the json file, so they're here ¯\_(ツ)_/¯
    elif current == "SHOWER" and s == "BATHE":
        if len(inventory) == 0:
            inventory.append("SHOWERED")
            print("\nYou successfully TAKE a SHOWER\nNothing beats a shower after a night of too much drinking in a self-destructive streak!")
        else:
            print("\nYou already showered! No need to raise your water bill any higher than it is.")

    elif current == "SINK" and s == "TEETH":
        if len(inventory) == 1:
            inventory.append("BRUSHED TEETH")
            print("\nYou successfully BRUSH you TEETH\nYou already start to feel better.")
        elif len(inventory) == 0:
            print("\nYou know you can technically brush your teeth before showering, but it just feels weird.")
        else:
            print("\nYou already brushed your teeth.  If your brush them too much, you'll end up getting cavities (weirdly enough).")

    elif current == "SINK" and s == "MEDS":
        if len(inventory) == 2:
            inventory.append("TOOK MEDS")
            print("You successfully TOOK your MEDS\n Take that, depression and anxiety!  You throw in a tylenol for good measure.")
        elif len(inventory) == 0:
            print("\nUgh, you're too distracted by how gross you feel.  Should probably shower first.")
        elif len(inventory) == 1:
            print("\nThe taste of your mouth is getting the better of you.  Better take care of that.")
        else:
            print("\nYou already took your meds.  They'll kick in soon.")

    elif current == "SINK" and s == "FACE":
        if len(inventory) == 3:
            inventory.append("WASHED FACE")
            print("You successfully WASHED your FACE\n Take that, oils and acne!")
        elif len(inventory) == 0:
            print("\nIf you wash your face before showering, all the moisturizer in your soap will get washed out.  It's better to\n shower first.")
        elif len(inventory) == 1:
            print("\nYou've always been messy when brushing your teeth.  Better do that first, then you can rinse off the paste\n from your mouth")
        elif len(inventory) == 2:
            print("\nIt's usually best to take your meds after brushing your teeth. \nThat way you don't have to wait for the water to cool back down to a drinking temperature.")
        else:
            print("\nYou already washed your face.  Why would you wash out the moisturizer?")

    elif current == "MIRROR" and s == "MAKEUP":
        if len(inventory) == 4:
            inventory.append("APPLIED MAKEUP")
            print("You successfully APPLIED your MAKEUP\nHave to make sure the world doesn't know just how hard you\nwent last night.")
        elif len(inventory) == 0:
            print("\nYou really need to shower.")
        elif len(inventory) == 1:
            print("\nYou can't just skip brushing your teeth.")
        elif len(inventory) == 2:
            print("\nYou need to take your meds before you forget.")
        elif len(inventory) == 3:
            print("\nYou have to wash your face before putting on makeup.")
        else:
            print("\nYou have enough makeup on.")
            
    elif current == "MIRROR" and s == "HAIR":
        if len(inventory) == 5:
            inventory.append("STYLED HAIR")
            print("You successfully STYLED your HAIR\nIf your hair looks good, no one will know just how messy you really are!")
        elif len(inventory) == 0:
            print("\nYou're hair is too gross to style.'")
        elif len(inventory) == 1:
            print("\nYou should brush your teeth first.")
        elif len(inventory) == 2:
            print("\nYou need to take your meds before you forget.")
        elif len(inventory) == 3:
            print("\nYou have to wash your face first.")
        elif len(inventory) == 4:
            print("\nYou should do your makeup first, since your hair needs to be pulled back for that.")    
        else:
            print("\nYour hair is styled enough.")

    elif current == "OPEN" and s == "DRESS":
        if len(inventory) == 6:
            inventory.append("GOT DRESSED")
            print("You successfully GOT DRESSED\nNow you are ready to face the day!")
            current = 'END'
        elif len(inventory) == 0:
            print("\nUgh, you still smell like the bar from last night.  Should probably take care of that.")
        elif len(inventory) == 1:
            print("\nYou should brush your teeth first.")
        elif len(inventory) == 2:
            print("\nYou need to take your meds before you forget.")
        elif len(inventory) == 3:
            print("\nYou have to wash your face first.")
        elif len(inventory) == 4:
            print("\nYou should do your makeup first, so you don't get it on your clothes")
        elif len(inventory) == 5:
            print("\nYou've made the mistake of doing you hair after getting dressed in the past, and ended up with hairspray all\nover your clothes.")
        

    else:
        for e in game['rooms'][current]['exits']:
            if s == e['verb'] and e['target'] != 'NoExit':
                return e['target']

    
    return current


# Helper functions

def printExits(game,current):
    e = ", ".join(str(x['verb']) for x in game['rooms'][current]['exits'])
    print('\nYou can move to the following: {directions}'.format(directions = e))

def normalizeVerb(selection,verbs):
    for v in verbs:
        if selection == v['v']:
            return v['map']
    return ""

def end_game(winning,moves):
    if winning:
        print('You have won! Congratulations')
        print('You finished in {moves} moves! Nicely done!'.format(moves=moves))
    else:
        print('Thanks for playing!')
        print('You finished in {moves} moves. See you next time!'.format(moves=moves))





def main():
    gameFile = 'game.json'

    game = {}
    with open(gameFile) as json_file:
        game = json.load(json_file)

    current = 'START'
    win = ['END']
    lose = []
    moves = 0
    inventory = []

    while True:

        render(game,current,moves)

        selection = getInput(game,current,game['verbs'])

        if selection[0] == 'QUIT':
            end_game(False,moves)
            break

        current = update(selection,game,current,inventory)

        if current in win:
            end_game(True,moves)
            break
        if current in lose:
            end_game(False,moves)
            break

        moves += 1





if __name__ == '__main__':
	main()