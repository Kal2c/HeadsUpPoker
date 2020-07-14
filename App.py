import os
from Cards import NewHand
from Players import Player
from time import sleep


def clear_screen():
    _ = os.system('cls' if os.name == 'nt' else 'clear')


player1_name = input('Enter the name for Player1: ').title()
player2_name = input('Enter the name for Player2: ').title()

player1 = Player(player1_name)
player2 = Player(player2_name)


def valid_input(s: str, allowed: list):
    if s in allowed:
        return True
    else:
        return False


def dealer_preflop_raise():
    minimum_raise = (2 * (hand.bb.put_in_pot_pre - hand.dealer.put_in_pot_pre))

    try:
        raisesize = float(input(f'How much would you like to raise to? (Stack = {hand.dealer.stack}): $'))
        if raisesize >= hand.dealer.stack + hand.dealer.put_in_pot_pre:  # if bet constitutes all (or more than all) the
            raisesize = hand.dealer.stack + hand.dealer.put_in_pot_pre   # chips that a player has, sets them all in.
            hand.pot += raisesize - hand.dealer.put_in_pot_pre           # Also ensures that if they bet more than they have
            hand.dealer.put_in_pot_pre = raisesize                       # that only the chips they have are added to the
            hand.dealer.all_in = True                                    # pot.
            print(f'{hand.dealer.name} is all in!')
            hand.dealer.stack = 0.00
        elif raisesize < minimum_raise and not hand.dealer.all_in:
            print(f'You must raise to at least ${minimum_raise}!')
            dealer_preflop_raise()
        else:  # adjusts the stacks and pot for normal case
            hand.dealer.stack -= raisesize - hand.dealer.put_in_pot_pre
            hand.pot += raisesize - hand.dealer.put_in_pot_pre
            hand.dealer.put_in_pot_pre = raisesize
            print(f'{hand.dealer.name} raises to ${raisesize}')
    except ValueError:
        print('Please enter a valid bet size.')
        dealer_preflop_raise()


def bb_preflop_raise():
    minimum_raise = (2 * (hand.dealer.put_in_pot_pre - hand.bb.put_in_pot_pre))

    try:
        raisesize = float(input(f'How much would you like to raise to? (Stack = {hand.bb.stack}): $'))
        if raisesize >= hand.bb.stack + hand.bb.put_in_pot_pre:
            raisesize = hand.bb.stack + hand.bb.put_in_pot_pre
            hand.pot += raisesize
            hand.bb.all_in = True
            print(f'{hand.bb.name} is all in!')
            hand.bb.stack = 0.00
        elif raisesize < minimum_raise:
            print(f'You must raise to at least ${minimum_raise}!')
            bb_preflop_raise()
        else:
            hand.bb.stack -= raisesize - hand.bb.put_in_pot_pre
            hand.pot += raisesize - hand.bb.put_in_pot_pre
            hand.bb.put_in_pot_pre = raisesize
            print(f'{hand.bb.name} raises to ${raisesize}')
    except ValueError:
        print('Please enter a valid bet size.')
        bb_preflop_raise()


def dealer_preflop_call():
    hand.dealer.stack -= hand.bb.put_in_pot_pre - hand.dealer.put_in_pot_pre
    hand.pot += hand.bb.put_in_pot_pre - hand.dealer.put_in_pot_pre
    hand.dealer.put_in_pot_pre += hand.bb.put_in_pot_pre - hand.dealer.put_in_pot_pre
    
    if hand.bb.all_in:
        if hand.dealer.stack > 0:  # case where dealer has bb covered 
            print(f'{hand.dealer.name} calls the ${hand.bb.put_in_pot_pre} all in.')
            print(f'The pot is ${hand.pot}')
            sleep(2)
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            sleep(2)
            hand.get_winner()
            hand.allocate_pot()
        elif hand.dealer.stack >= 0:  # case where bb has dealer covered (limits the pot from becoming impossibly big)
            hand.pot += hand.dealer.stack
            hand.dealer.put_in_pot_pre += hand.dealer.stack
            remainder = hand.bb.put_in_pot_pre - hand.dealer.put_in_pot_pre
            hand.pot -= remainder
            hand.bb.stack += remainder
            hand.dealer.stack = 0
            hand.dealer.all_in = True
            hand.bb.all_in = False  # if player goes all in and is called by a smaller stack they are no longer all in
            print(f'{hand.dealer.name} is all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
    else:
        if hand.dealer.stack <= 0:
            hand.pot += hand.dealer.stack
            hand.dealer.put_in_pot_pre += hand.dealer.stack
            hand.dealer.stack = 0
            hand.dealer.all_in = True
            remainder = hand.bb.put_in_pot_pre - hand.dealer.put_in_pot_pre
            hand.pot -= remainder
            hand.bb.stack += remainder
            print(f'{hand.dealer.name} calls all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        else:
            print(f'{hand.dealer.name} calls the ${hand.bb.put_in_pot_pre} bet.')


def bb_preflop_call():
    hand.bb.stack -= hand.dealer.put_in_pot_pre - hand.bb.put_in_pot_pre
    hand.pot += hand.dealer.put_in_pot_pre - hand.bb.put_in_pot_pre
    hand.bb.put_in_pot_pre += hand.dealer.put_in_pot_pre - hand.bb.put_in_pot_pre
    
    if hand.dealer.all_in:  # case when the other player bets all in
        if hand.bb.stack > 0:  # bb has dealer covered
            print(f'{hand.bb.name} calls the ${hand.dealer.put_in_pot_pre} all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        elif hand.bb.stack >= 0:  # case where dealer has bb covered (limits the pot from becoming impossibly big)
            hand.pot += hand.bb.stack
            hand.bb.put_in_pot_pre += hand.bb.stack
            hand.bb.stack = 0
            remainder = hand.dealer.put_in_pot_pre - hand.bb.put_in_pot_pre
            hand.pot -= remainder
            hand.dealer.stack += remainder
            hand.bb.all_in = True
            hand.dealer.all_in = False  # if player goes all in and is called by a smaller stack they are no longer all in
            print(f'{hand.bb.name} is all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
    else:
        if hand.bb.stack <= 0:
            hand.pot += hand.bb.stack
            hand.bb.put_in_pot_pre += hand.bb.stack
            hand.bb.stack = 0
            hand.bb.all_in = True
            remainder = hand.dealer.put_in_pot_pre - hand.bb.put_in_pot_pre
            hand.pot -= remainder
            hand.dealer.stack += remainder
            print(f'{hand.bb.name} calls all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        else:
            print(f'{hand.bb.name} calls the ${hand.dealer.put_in_pot_pre} bet.')


def pre_flop_decision_tree():
    bb_action = 'r'
    dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
    while not valid_input(dealer_action, ['c', 'f', 'r']):
        print(f'Invalid input please enter: "c", "f", or "r".')
        dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
        valid_input(dealer_action, ['c', 'f', 'r'])
    while dealer_action == 'r' and bb_action == 'r':
        dealer_preflop_raise()
        bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
        while not valid_input(bb_action, ['c', 'f', 'r']):
            print(f'Invalid input please enter: "c", "f", or "r".')
            bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
            valid_input(bb_action, ['c', 'f', 'r'])
        if bb_action == 'r':
            bb_preflop_raise()
            dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
            while not valid_input(dealer_action, ['c', 'f', 'r']):
                print(f'Invalid input please enter: "c", "f", or "r".')
                dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                valid_input(dealer_action, ['c', 'f', 'r'])
    else:
        if dealer_action == 'c' and hand.pot == 1.50:  # case where dealer 'limps' into pot
            dealer_preflop_call()
            bb_action = input(f'{hand.bb.name}, would you like to check(x), or raise(r)?: ').lower()
            while not valid_input(bb_action, ['x', 'r']):
                print(f'Invalid input please enter: "x" or "r".')
                bb_action = input(f'{hand.bb.name}, would you like to check(x), or raise(r)?: ').lower()
                valid_input(bb_action, ['x', 'r'])
            if bb_action == 'x':
                pass  # if bb checks nothing happens and hand continues to the flop
            elif bb_action == 'r':  
                dealer_action = 'r'
                while dealer_action == 'r' and bb_action == 'r':
                    bb_preflop_raise()
                    dealer_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                    while not valid_input(dealer_action, ['c', 'f', 'r']):
                        print(f'Invalid input please enter: "c", "f", or "r".')
                        dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                        valid_input(dealer_action, ['c', 'f', 'r'])
                    if dealer_action == 'r':
                        dealer_preflop_raise()
                        bb_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                        while not valid_input(bb_action, ['c', 'f', 'r']):
                            print(f'Invalid input please enter: "c", "f", or "r".')
                            bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                            valid_input(bb_action, ['c', 'f', 'r'])
                else:
                    if dealer_action == 'c':
                        dealer_preflop_call()
                    elif bb_action == 'c':
                        bb_preflop_call()
                    elif dealer_action == 'f':
                        hand.bb.stack += hand.pot
                        hand.player_folded = True
                    elif bb_action == 'f':
                        hand.dealer.stack += hand.pot
                        hand.player_folded = True
        elif dealer_action == 'c' and hand.pot > 1.50:
            dealer_preflop_call()
        elif bb_action == 'c':
            bb_preflop_call()
        elif dealer_action == 'f':
            hand.bb.stack += hand.pot
            hand.player_folded = True
        elif bb_action == 'f':
            hand.dealer.stack += hand.pot
            hand.player_folded = True


def dealer_flop_raise():
    minimum_raise = (2 * (hand.bb.put_in_pot_flop - hand.dealer.put_in_pot_flop))

    try:
        raisesize = float(input(f'How much would you like to raise to? (Stack = {hand.dealer.stack}): $'))
        if raisesize >= hand.dealer.stack + hand.dealer.put_in_pot_flop:
            raisesize = hand.dealer.stack + hand.dealer.put_in_pot_flop
            hand.pot += raisesize
            hand.dealer.all_in = True
            print(f'{hand.dealer.name} is all in!')
            hand.dealer.stack = 0.00
        elif raisesize < minimum_raise:
            print(f'You must raise to at least ${minimum_raise}!')
            dealer_flop_raise()
        else:
            hand.dealer.stack -= raisesize - hand.dealer.put_in_pot_flop
            hand.pot += raisesize - hand.dealer.put_in_pot_flop
            hand.dealer.put_in_pot_flop = raisesize
            print(f'{hand.dealer.name} raises to ${raisesize}')
    except ValueError:
        print('Please enter a valid bet size.')
        dealer_flop_raise()


def bb_flop_raise():
    minimum_raise = (2 * (hand.dealer.put_in_pot_flop - hand.bb.put_in_pot_flop)) + hand.dealer.put_in_pot_flop

    try:
        raisesize = float(input(f'How much would you like to raise to? (Stack = {hand.bb.stack}): $'))
        if raisesize >= hand.bb.stack + hand.bb.put_in_pot_flop:
            raisesize = hand.bb.stack + hand.bb.put_in_pot_flop
            hand.pot += raisesize
            hand.bb.all_in = True
            print(f'{hand.bb.name} is all in!')
            hand.bb.stack = 0.00
        elif raisesize < minimum_raise:
            print(f'You must raise to at least ${minimum_raise}!')
            bb_flop_raise()
        else:
            hand.bb.stack -= raisesize - hand.bb.put_in_pot_flop
            hand.pot += raisesize - hand.bb.put_in_pot_flop
            hand.bb.put_in_pot_flop = raisesize
            print(f'{hand.bb.name} raises to ${raisesize}')
    except ValueError:
        print('Please enter a valid bet size.')
        bb_flop_raise()


def dealer_flop_call():
    hand.dealer.stack -= hand.bb.put_in_pot_flop - hand.dealer.put_in_pot_flop
    hand.pot += hand.bb.put_in_pot_flop - hand.dealer.put_in_pot_flop
    hand.dealer.put_in_pot_flop += hand.bb.put_in_pot_flop - hand.dealer.put_in_pot_flop
    
    if hand.bb.all_in:
        if hand.dealer.stack > 0:  # case where dealer has bb covered 
            print(f'{hand.dealer.name} calls the ${hand.bb.put_in_pot_flop} all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        elif hand.dealer.stack >= 0:  # case where bb has dealer covered (limits the pot from becoming impossibly big)
            hand.pot += hand.dealer.stack
            hand.dealer.put_in_pot_flop += hand.dealer.stack
            hand.dealer.stack = 0
            remainder = hand.bb.put_in_pot_flop - hand.dealer.put_in_pot_flop
            hand.pot -= remainder
            hand.bb.stack += remainder
            hand.dealer.all_in = True
            hand.bb.all_in = False  # if player goes all in and is called by a smaller stack they are no longer all in
            print(f'{hand.dealer.name} is all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
    else:
        if hand.dealer.stack <= 0:
            hand.pot += hand.dealer.stack
            hand.dealer.put_in_pot_flop += hand.dealer.stack
            hand.dealer.stack = 0
            remainder = hand.bb.put_in_pot_flop - hand.dealer.put_in_pot_flop
            hand.pot -= remainder
            hand.bb.stack += remainder
            hand.dealer.all_in = True
            print(f'{hand.dealer.name} calls all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        else:
            print(f'{hand.dealer.name} calls the ${hand.bb.put_in_pot_flop} bet.')


def bb_flop_call():
    hand.bb.stack -= hand.dealer.put_in_pot_flop - hand.bb.put_in_pot_flop
    hand.pot += hand.dealer.put_in_pot_flop - hand.bb.put_in_pot_flop
    hand.bb.put_in_pot_flop += hand.dealer.put_in_pot_flop - hand.bb.put_in_pot_flop
    
    if hand.dealer.all_in:
        if hand.bb.stack > 0:  # case where bb has dealer covered 
            print(f'{hand.bb.name} calls the ${hand.dealer.put_in_pot_flop} all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        elif hand.bb.stack >= 0:  # case where dealer has bb covered (limits the pot from becoming impossibly big)
            hand.pot += hand.bb.stack
            hand.bb.put_in_pot_flop += hand.bb.stack
            hand.bb.stack = 0
            remainder = hand.dealer.put_in_pot_flop - hand.bb.put_in_pot_flop
            hand.pot -= remainder
            hand.dealer.stack += remainder
            hand.bb.all_in = True
            hand.dealer.all_in = False  # if player goes all in and is called by a smaller stack they are no longer all in
            print(f'{hand.bb.name} is all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
    else:
        if hand.bb.stack <= 0:
            hand.pot += hand.bb.stack
            hand.bb.put_in_pot_flop += hand.bb.stack
            hand.bb.stack = 0
            remainder = hand.dealer.put_in_pot_flop - hand.bb.put_in_pot_flop
            hand.pot -= remainder
            hand.dealer.stack += remainder
            hand.bb.all_in = True
            print(f'{hand.bb.name} calls all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        else:
            print(f'{hand.bb.name} calls the ${hand.dealer.put_in_pot_flop} bet.')


def flop_decision_tree():
    print(f'The flop is: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]}')
    print(f'The pot is: ${hand.pot}')
    bb_action = input(f'{hand.bb.name}, would you like to check(x), or raise(r)?: ').lower()
    while not valid_input(bb_action, ['x', 'r']):
        print(f'Invalid input please enter: "x" or "r".')
        bb_action = input(f'{hand.bb.name}, would you like to check(x), or raise(r)?: ').lower()
        valid_input(bb_action, ['x', 'r'])
    dealer_action = 'r'
    while dealer_action == 'r' and bb_action == 'r':
        bb_flop_raise()
        dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
        while not valid_input(dealer_action, ['c', 'f', 'r']):
            print(f'Invalid input please enter: "c", "f", or "r".')
            dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
            valid_input(dealer_action, ['c', 'f', 'r'])
        if dealer_action == 'r':
            dealer_flop_raise()
            bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
            while not valid_input(bb_action, ['c', 'f', 'r']):
                print(f'Invalid input please enter: "c", "f", or "r".')
                bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                valid_input(bb_action, ['c', 'f', 'r'])
    else:
        if bb_action == 'x':
            dealer_action = input(f'{hand.dealer.name}, would you like to check(x), or raise(r)?: ').lower()
            while not valid_input(dealer_action, ['x', 'r']):
                print(f'Invalid input please enter: "x", or "r".')
                dealer_action = input(f'{hand.dealer.name}, would you like to check(x), or raise(r)?: ').lower()
                valid_input(dealer_action, ['x', 'r'])
            if dealer_action == 'x':
                pass
            elif dealer_action == 'r':
                bb_action = 'r'
                while dealer_action == 'r' and bb_action == 'r':
                    dealer_flop_raise()
                    bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                    while not valid_input(bb_action, ['c', 'f', 'r']):
                        print(f'Invalid input please enter: "c", "f", or "r".')
                        bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                        valid_input(bb_action, ['c', 'f', 'r'])
                    if bb_action == 'r':
                        bb_flop_raise()
                        dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                        while not valid_input(dealer_action, ['c', 'f', 'r']):
                            print(f'Invalid input please enter: "c", "f", or "r".')
                            dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                            valid_input(dealer_action, ['c', 'f', 'r'])
                else:
                    if dealer_action == 'c':
                        dealer_flop_call()
                    elif bb_action == 'c':
                        bb_flop_call()
                    elif dealer_action == 'f':
                        hand.bb.stack += hand.pot
                        hand.player_folded = True
                        print(f'{hand.bb.name} wins the hand.')
                    elif bb_action == 'f':
                        hand.dealer.stack += hand.pot
                        print(f'{hand.dealer.name} wins the hand.')
                        hand.player_folded = True
        elif dealer_action == 'c':
            dealer_flop_call()
        elif bb_action == 'c':
            bb_flop_call()
        elif dealer_action == 'f':
            hand.bb.stack += hand.pot
            hand.player_folded = True
            print(f'{hand.bb.name} wins the hand.')
            hand.player_folded = True
        elif bb_action == 'f':
            hand.dealer.stack += hand.pot
            hand.player_folded = True
            print(f'{hand.dealer.name} wins the hand.')
            hand.player_folded = True


def dealer_turn_raise():
    minimum_raise = (2 * (hand.bb.put_in_pot_turn - hand.dealer.put_in_pot_turn))

    try:
        raisesize = float(input(f'How much would you like to raise to? (Stack = {hand.dealer.stack}): $'))
        if raisesize >= hand.dealer.stack + hand.dealer.put_in_pot_turn:
            raisesize = hand.dealer.stack + hand.dealer.put_in_pot_turn
            hand.pot += raisesize
            hand.dealer.all_in = True
            print(f'{hand.dealer.name} is all in!')
            hand.dealer.stack = 0.00
        elif raisesize < minimum_raise:
            print(f'You must raise to at least ${minimum_raise}!')
            dealer_turn_raise()
        else:
            hand.dealer.stack -= raisesize - hand.dealer.put_in_pot_turn
            hand.pot += raisesize - hand.dealer.put_in_pot_turn
            hand.dealer.put_in_pot_turn = raisesize
            print(f'{hand.dealer.name} raises to ${raisesize}')
    except ValueError:
        print('Please enter a valid bet size.')
        dealer_turn_raise()


def bb_turn_raise():
    minimum_raise = (2 * (hand.dealer.put_in_pot_turn - hand.bb.put_in_pot_turn)) + hand.dealer.put_in_pot_turn

    try:
        raisesize = float(input(f'How much would you like to raise to? (Stack = {hand.bb.stack}): $'))
        if raisesize >= hand.bb.stack + hand.bb.put_in_pot_turn:
            raisesize = hand.bb.stack + hand.bb.put_in_pot_turn
            hand.pot += raisesize
            hand.bb.all_in = True
            print(f'{hand.bb.name} is all in!')
            hand.bb.stack = 0.00
        elif raisesize < minimum_raise:
            print(f'You must raise to at least ${minimum_raise}!')
            bb_turn_raise()
        else:
            hand.bb.stack -= raisesize - hand.bb.put_in_pot_turn
            hand.pot += raisesize - hand.bb.put_in_pot_turn
            hand.bb.put_in_pot_turn = raisesize
            print(f'{hand.bb.name} raises to ${raisesize}')
    except ValueError:
        print('Please enter a valid bet size.')
        bb_turn_raise()


def dealer_turn_call():
    hand.dealer.stack -= hand.bb.put_in_pot_turn - hand.dealer.put_in_pot_turn
    hand.pot += hand.bb.put_in_pot_turn - hand.dealer.put_in_pot_turn
    hand.dealer.put_in_pot_turn += hand.bb.put_in_pot_turn - hand.dealer.put_in_pot_turn
    
    if hand.bb.all_in:
        if hand.dealer.stack > 0:  # case where dealer has bb covered 
            print(f'{hand.dealer.name} calls the ${hand.bb.put_in_pot_turn} all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        elif hand.dealer.stack >= 0:  # case where bb has dealer covered (limits the pot from becoming impossibly big)
            hand.pot += hand.dealer.stack
            hand.dealer.put_in_pot_turn += hand.dealer.stack
            hand.dealer.stack = 0
            remainder = hand.bb.put_in_pot_turn - hand.dealer.put_in_pot_turn
            hand.pot -= remainder
            hand.bb.stack += remainder
            hand.dealer.all_in = True
            hand.bb.all_in = False  # if player goes all in and is called by a smaller stack they are no longer all in
            print(f'{hand.dealer.name} is all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
    else:
        if hand.dealer.stack <= 0:
            hand.pot += hand.dealer.stack
            hand.dealer.put_in_pot_turn += hand.dealer.stack
            hand.dealer.stack = 0
            remainder = hand.bb.put_in_pot_turn - hand.dealer.put_in_pot_turn
            hand.pot -= remainder
            hand.bb.stack += remainder
            hand.dealer.all_in = True
            print(f'{hand.dealer.name} calls all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        else:
            print(f'{hand.dealer.name} calls the ${hand.bb.put_in_pot_turn} bet.')


def bb_turn_call():
    hand.bb.stack -= hand.dealer.put_in_pot_turn - hand.bb.put_in_pot_turn
    hand.pot += hand.dealer.put_in_pot_turn - hand.bb.put_in_pot_turn
    hand.bb.put_in_pot_turn += hand.dealer.put_in_pot_turn - hand.bb.put_in_pot_turn
    
    if hand.dealer.all_in:
        if hand.bb.stack > 0:  # case where bb has dealer covered 
            print(f'{hand.bb.name} calls the ${hand.dealer.put_in_pot_turn} all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        elif hand.bb.stack >= 0:  # case where dealer has bb covered (limits the pot from becoming impossibly big)
            hand.pot += hand.bb.stack
            hand.bb.put_in_pot_turn += hand.bb.stack
            hand.bb.stack = 0
            remainder = hand.dealer.put_in_pot_turn - hand.bb.put_in_pot_turn
            hand.pot -= remainder
            hand.dealer.stack += remainder
            hand.bb.all_in = True
            hand.dealer.all_in = False  # if player goes all in and is called by a smaller stack they are no longer all in
            print(f'{hand.bb.name} is all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
    else:
        if hand.bb.stack <= 0:
            hand.pot += hand.bb.stack
            hand.bb.put_in_pot_turn += hand.bb.stack
            hand.bb.stack = 0
            remainder = hand.dealer.put_in_pot_turn - hand.bb.put_in_pot_turn
            hand.pot -= remainder
            hand.dealer.stack += remainder
            hand.bb.all_in = True
            print(f'{hand.bb.name} calls all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        else:
            print(f'{hand.bb.name} calls the ${hand.dealer.put_in_pot_turn} bet.')


def turn_decision_tree():
    print(f'The turn is: {hand.community_cards[3]}')
    print(f'The board is: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} {hand.community_cards[3]}')
    print(f'The pot is: ${hand.pot}')
    bb_action = input(f'{hand.bb.name}, would you like to check(x), or raise(r)?: ').lower()
    while not valid_input(bb_action, ['x', 'r']):
        print(f'Invalid input please enter: "x", or "r".')
        bb_action = input(f'{hand.bb.name}, would you like to check(x), or raise(r)?: ').lower()
        valid_input(bb_action, ['x', 'r'])
    dealer_action = 'r'
    while dealer_action == 'r' and bb_action == 'r':
        bb_turn_raise()
        dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
        while not valid_input(dealer_action, ['c', 'f', 'r']):
            print(f'Invalid input please enter: "c", "f", or "r".')
            dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
            valid_input(dealer_action, ['c', 'f', 'r'])
        if dealer_action == 'r':
            dealer_turn_raise()
            bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
            while not valid_input(bb_action, ['c', 'f', 'r']):
                print(f'Invalid input please enter: "c", "f", or "r".')
                bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                valid_input(bb_action, ['c', 'f', 'r'])
    else:
        if bb_action == 'x':
            dealer_action = input(f'{hand.dealer.name}, would you like to check(x), or raise(r)?: ').lower()
            while not valid_input(dealer_action, ['x', 'r']):
                print(f'Invalid input please enter: "x", or "r".')
                dealer_action = input(f'{hand.dealer.name}, would you like to check(x), or raise(r)?: ').lower()
                valid_input(dealer_action, ['x', 'r'])
            if dealer_action == 'x':
                pass
            elif dealer_action == 'r':
                bb_action = 'r'
                while dealer_action == 'r' and bb_action == 'r':
                    dealer_turn_raise()
                    bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                    while not valid_input(bb_action, ['c', 'f', 'r']):
                        print(f'Invalid input please enter: "c", "f", or "r".')
                        bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                        valid_input(bb_action, ['c', 'f', 'r'])
                    if bb_action == 'r':
                        bb_turn_raise()
                        dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                        while not valid_input(dealer_action, ['c', 'f', 'r']):
                            print(f'Invalid input please enter: "c", "f", or "r".')
                            dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                            valid_input(dealer_action, ['c', 'f', 'r'])
                else:
                    if dealer_action == 'c':
                        dealer_turn_call()
                    elif bb_action == 'c':
                        bb_turn_call()
                    elif dealer_action == 'f':
                        hand.bb.stack += hand.pot
                        print(f'{hand.bb.name} wins the hand.')
                        hand.player_folded = True
                    elif bb_action == 'f':
                        hand.dealer.stack += hand.pot
                        print(f'{hand.dealer.name} wins the hand.')
                        hand.player_folded = True
        elif dealer_action == 'c':
            dealer_turn_call()
        elif bb_action == 'c':
            bb_turn_call()
        elif dealer_action == 'f':
            hand.bb.stack += hand.pot
            print(f'{hand.bb.name} wins the hand.')
            hand.player_folded = True
        elif bb_action == 'f':
            hand.dealer.stack += hand.pot
            print(f'{hand.dealer.name} wins the hand.')
            hand.player_folded = True


def dealer_river_raise():
    minimum_raise = (2 * (hand.bb.put_in_pot_river - hand.dealer.put_in_pot_river))

    try:
        raisesize = float(input(f'How much would you like to raise to? (Stack = {hand.dealer.stack}): $'))
        if raisesize >= hand.dealer.stack + hand.dealer.put_in_pot_river:
            raisesize = hand.dealer.stack + hand.dealer.put_in_pot_river
            hand.pot += raisesize
            hand.dealer.all_in = True
            print(f'{hand.dealer.name} is all in!')
            hand.dealer.stack = 0.00
        elif raisesize < minimum_raise:
            print(f'You must raise to at least ${minimum_raise}!')
            dealer_river_raise()
        else:
            hand.dealer.stack -= raisesize - hand.dealer.put_in_pot_river
            hand.pot += raisesize - hand.dealer.put_in_pot_river
            hand.dealer.put_in_pot_river = raisesize
            print(f'{hand.dealer.name} raises to ${raisesize}')
    except ValueError:
        print('Please enter a valid bet size.')
        dealer_river_raise()


def bb_river_raise():
    minimum_raise = (2 * (hand.dealer.put_in_pot_river - hand.bb.put_in_pot_river)) + hand.dealer.put_in_pot_river

    try:
        raisesize = float(input(f'How much would you like to raise to? (Stack = {hand.bb.stack}): $'))
        if raisesize >= hand.bb.stack + hand.bb.put_in_pot_river:
            raisesize = hand.bb.stack + hand.bb.put_in_pot_river
            hand.pot += raisesize
            hand.bb.all_in = True
            print(f'{hand.bb.name} is all in!')
            hand.bb.stack = 0.00
        elif raisesize < minimum_raise:
            print(f'You must raise to at least ${minimum_raise}!')
            bb_river_raise()
        else:
            hand.bb.stack -= raisesize - hand.bb.put_in_pot_river
            hand.pot += raisesize - hand.bb.put_in_pot_river
            hand.bb.put_in_pot_river = raisesize
            print(f'{hand.bb.name} raises to ${raisesize}')
    except ValueError:
        print('Please enter a valid bet size.')
        bb_river_raise()


def dealer_river_call():
    hand.dealer.stack -= hand.bb.put_in_pot_river - hand.dealer.put_in_pot_river
    hand.pot += hand.bb.put_in_pot_river - hand.dealer.put_in_pot_river
    hand.dealer.put_in_pot_river += hand.bb.put_in_pot_river - hand.dealer.put_in_pot_river
    
    if hand.bb.all_in:
        if hand.dealer.stack > 0:  # case where dealer has bb covered 
            print(f'{hand.dealer.name} calls the ${hand.bb.put_in_pot_river} all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        elif hand.dealer.stack >= 0:  # case where bb has dealer covered (limits the pot from becoming impossibly big)
            hand.pot += hand.dealer.stack
            hand.dealer.put_in_pot_river += hand.dealer.stack
            hand.dealer.stack = 0
            remainder = hand.bb.put_in_pot_river - hand.dealer.put_in_pot_river
            hand.pot -= remainder
            hand.bb.stack += remainder
            hand.dealer.all_in = True
            hand.bb.all_in = False  # if player goes all in and is called by a smaller stack they are no longer all in
            print(f'{hand.dealer.name} is all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
    else:
        if hand.dealer.stack <= 0:
            hand.pot += hand.dealer.stack
            hand.dealer.put_in_pot_river += hand.dealer.stack
            hand.dealer.stack = 0
            remainder = hand.bb.put_in_pot_river - hand.dealer.put_in_pot_river
            hand.pot -= remainder
            hand.bb.stack += remainder
            hand.dealer.all_in = True
            print(f'{hand.dealer.name} calls all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        else:
            print(f'{hand.dealer.name} calls the ${hand.bb.put_in_pot_river} bet.')


def bb_river_call():
    hand.bb.stack -= hand.dealer.put_in_pot_river - hand.bb.put_in_pot_river
    hand.pot += hand.dealer.put_in_pot_river - hand.bb.put_in_pot_river
    hand.bb.put_in_pot_river += hand.dealer.put_in_pot_river - hand.bb.put_in_pot_river
    
    if hand.dealer.all_in:
        if hand.bb.stack > 0:  # case where bb has dealer covered 
            print(f'{hand.bb.name} calls the ${hand.dealer.put_in_pot_river} all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        elif hand.bb.stack >= 0:  # case where dealer has bb covered (limits the pot from becoming impossibly big)
            hand.pot += hand.bb.stack
            hand.bb.put_in_pot_river += hand.bb.stack
            hand.bb.stack = 0
            remainder = hand.dealer.put_in_pot_river - hand.bb.put_in_pot_river
            hand.pot -= remainder
            hand.dealer.stack += remainder
            hand.bb.all_in = True
            hand.dealer.all_in = False  # if player goes all in and is called by a smaller stack they are no longer all in
            print(f'{hand.bb.name} is all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
    else:
        if hand.bb.stack <= 0:
            hand.pot += hand.bb.stack
            hand.bb.put_in_pot_river += hand.bb.stack
            hand.bb.stack = 0
            remainder = hand.dealer.put_in_pot_river - hand.bb.put_in_pot_river
            hand.pot -= remainder
            hand.dealer.stack += remainder
            hand.bb.all_in = True
            print(f'{hand.bb.name} calls all in.')
            print(f'The pot is ${hand.pot}')
            print(f'''The board runs out: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} 
            {hand.community_cards[3]} {hand.community_cards[4]}''')
            hand.get_winner()
            hand.allocate_pot()
        else:
            print(f'{hand.bb.name} calls the ${hand.dealer.put_in_pot_river} bet.')


def river_decision_tree():
    print(f'The river is: {hand.community_cards[4]}')
    print(f'The board is: {hand.community_cards[0]} {hand.community_cards[1]} {hand.community_cards[2]} {hand.community_cards[3]} {hand.community_cards[4]}')
    print(f'The pot is: ${hand.pot}')
    bb_action = input(f'{hand.bb.name}, would you like to check(x), or raise(r)?: ').lower()
    while not valid_input(bb_action, ['x', 'r']):
        print(f'Invalid input please enter: "x", or "r".')
        bb_action = input(f'{hand.bb.name}, would you like to check(x), or raise(r)?: ').lower()
        valid_input(bb_action, ['x', 'r'])
    dealer_action = 'r'
    while dealer_action == 'r' and bb_action == 'r':
        bb_river_raise()
        dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
        while not valid_input(dealer_action, ['c', 'f', 'r']):
            print(f'Invalid input please enter: "c", "f", or "r".')
            dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
            valid_input(dealer_action, ['c', 'f', 'r'])
        if dealer_action == 'r':
            dealer_river_raise()
            bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
            while not valid_input(bb_action, ['c', 'f', 'r']):
                print(f'Invalid input please enter: "c", "f", or "r".')
                bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                valid_input(bb_action, ['c', 'f', 'r'])
    else:
        if bb_action == 'x':
            dealer_action = input(f'{hand.dealer.name}, would you like to check(x), or raise(r)?: ').lower()
            while not valid_input(dealer_action, ['x', 'r']):
                print(f'Invalid input please enter: "x", or "r".')
                dealer_action = input(f'{hand.dealer.name}, would you like to check(x), or raise(r)?: ').lower()
                valid_input(dealer_action, ['x', 'r'])
            if dealer_action == 'x':
                hand.get_winner()
                hand.allocate_pot()
            elif dealer_action == 'r':
                bb_action = 'r'
                while dealer_action == 'r' and bb_action == 'r':
                    dealer_river_raise()
                    bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                    while not valid_input(bb_action, ['c', 'f', 'r']):
                        print(f'Invalid input please enter: "c", "f", or "r".')
                        bb_action = input(f'{hand.bb.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                        valid_input(bb_action, ['c', 'f', 'r'])
                    if bb_action == 'r':
                        bb_river_raise()
                        dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                        while not valid_input(dealer_action, ['c', 'f', 'r']):
                            print(f'Invalid input please enter: "c", "f", or "r".')
                            dealer_action = input(f'{hand.dealer.name}, would you like to call(c), fold(f), or raise(r)?: ').lower()
                            valid_input(dealer_action, ['c', 'f', 'r'])
                else:
                    if dealer_action == 'c':
                        dealer_river_call()
                        hand.get_winner()
                        hand.allocate_pot()
                    elif bb_action == 'c':
                        bb_river_call()
                        hand.get_winner()
                        hand.allocate_pot()
                    elif dealer_action == 'f':
                        hand.bb.stack += hand.pot
                        print(f'{hand.bb.name} wins the hand.')
                        hand.player_folded = True
                    elif bb_action == 'f':
                        hand.dealer.stack += hand.pot
                        print(f'{hand.dealer.name} wins the hand.')
                        hand.player_folded = True
        elif dealer_action == 'c':
            dealer_river_call()
            hand.get_winner()
            hand.allocate_pot()
        elif bb_action == 'c':
            bb_river_call()
            hand.get_winner()
            hand.allocate_pot()
        elif dealer_action == 'f':
            hand.bb.stack += hand.pot
            print(f'{hand.bb.name} wins the hand.')
            hand.player_folded = True
        elif bb_action == 'f':
            hand.dealer.stack += hand.pot
            print(f'{hand.dealer.name} wins the hand.')
            hand.player_folded = True


def reset_hand():
    hand.pot = 0
    hand.dealer.put_in_pot_pre = 0
    hand.dealer.put_in_pot_flop = 0
    hand.dealer.put_in_pot_turn = 0
    hand.dealer.put_in_pot_river = 0
    hand.dealer.all_in = False
    hand.bb.put_in_pot_pre = 0
    hand.bb.put_in_pot_flop = 0
    hand.bb.put_in_pot_turn = 0
    hand.bb.put_in_pot_river = 0
    hand.bb.all_in = False


count = 0

while player1.stack > 0.00 and player2.stack > 0.00:
    if count % 2 == 0:
        hand = NewHand(player1, player2)
    else:
        hand = NewHand(player2, player1)

    reset_hand()
    hand.take_blinds()

    print(f'Look away {hand.bb.name}!')
    sleep(5)
    clear_screen()
    print(f'{hand.dealer.name} you hand is: {hand.dealer_hand[0]}{hand.dealer_hand[1]}, write this down!')
    sleep(6)
    clear_screen()

    print(f'Look away now {hand.dealer.name}, and tell {hand.bb.name} to look.')
    sleep(5)
    clear_screen()
    print(f'{hand.bb.name} you hand is: {hand.bb_hand[0]}{hand.bb_hand[1]}, write this down!')
    sleep(6)
    clear_screen()

    print(f'The dealer is: {hand.dealer.name}')
    print(f'Stacks are {player1.name}: {player1.stack}, {player2.name}: {player2.stack}')
    print(f'The pot stands at: ${hand.pot}')

    pre_flop_decision_tree()
    if not hand.player_folded and not hand.dealer.all_in and not hand.bb.all_in:
        flop_decision_tree()
        if not hand.player_folded and not hand.dealer.all_in and not hand.bb.all_in:
            turn_decision_tree()
            if not hand.player_folded and not hand.dealer.all_in and not hand.bb.all_in:
                river_decision_tree()

    count += 1
    sleep(2)
    clear_screen()

else:
    if player1.stack > player2.stack:
        print(f'Game over. {player1.name} is the winner!')
    else:
        print(f'Game over. {player2.name} is the winner!')
