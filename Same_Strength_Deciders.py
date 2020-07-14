from collections import Counter

card_vals = {
    'A': 14,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13
}


def stronger_sf(dealer_7cc: list, bb_7cc: list):
    """If both players have a straight flush, returns winner as the player with the higher straight flush."""
    dealer_suits = [c[1] for c in dealer_7cc]
    # Finds the suit that both players use to comprise their straight flushes. No need to check bb common suit, it must
    # be the same as straight flushes of different suits are impossible in a single hand of texas holdem.
    common_suit = Counter(dealer_suits).most_common(1)[0][0]

    dealer_suited_vals = sorted([card_vals[c[0]] for c in dealer_7cc if c[1] == common_suit])
    bb_suited_vals = sorted([card_vals[c[0]] for c in bb_7cc if c[1] == common_suit])

    split_dealer_vals = []
    split_bb_vals = []
    dealer_5cc = []
    bb_5cc = []

    for i in range(len(dealer_suited_vals) - 4):
        split_dealer_vals.append(dealer_suited_vals[i:i+5])
    for five_card_run in split_dealer_vals:
        if five_card_run[-1] - five_card_run[0] == 4:
            dealer_5cc = five_card_run
    for i in range(len(bb_suited_vals) - 4):
        split_bb_vals.append(bb_suited_vals[i:i+5])
    for five_card_run in split_bb_vals:
        if five_card_run[-1] - five_card_run[0] == 4 and len(five_card_run) == len(set(five_card_run)):
            bb_5cc = five_card_run

    if len(dealer_5cc) > 0 and len(bb_5cc) == 0:  # if len({Player}_5cc) = 0 means sf must be A2345 (lowest possible)
        return 'dealer'
    elif len(dealer_5cc) == 0 and len(bb_5cc) > 0:
        return 'bb'
    elif len(dealer_5cc) == 0 and len(bb_5cc) == 0:
        return 'tie'
    elif len(dealer_5cc) > 0 and len(bb_5cc) > 0 and dealer_5cc[1] > bb_5cc[1]:
        return 'dealer'
    elif len(dealer_5cc) > 0 and len(bb_5cc) > 0 and dealer_5cc[1] < bb_5cc[1]:
        return 'bb'
    else:
        return 'tie'


def stronger_quads(dealer_7cc: list, bb_7cc: list):
    """If both players have different quads, returns player with the higher quads. If both players have same quads,
    returns player with best high card to compliment quads or tie if players have same high card."""

    dealer_vals = [c[0] for c in dealer_7cc]
    bb_vals = [c[0] for c in bb_7cc]
    # Finds the most common value in players' 7 card combos, i.e. the one they have four of
    dealer_mcv = Counter(dealer_vals).most_common(1)[0][0]
    bb_mcv = Counter(bb_vals).most_common(1)[0][0]

    dealer_non_quad_vals = sorted([card_vals[v] for v in dealer_vals if v != dealer_mcv])
    bb_non_quad_vals = sorted([card_vals[v] for v in bb_vals if v != bb_mcv])

    # Returns the winner of the hand.
    if card_vals[dealer_mcv] > card_vals[bb_mcv]:
        return 'dealer'
    elif card_vals[dealer_mcv] < card_vals[bb_mcv]:
        return 'bb'
    elif card_vals[dealer_mcv] == card_vals[bb_mcv] and dealer_non_quad_vals[-1] > bb_non_quad_vals[-1]:
        return 'dealer'
    elif card_vals[dealer_mcv] == card_vals[bb_mcv] and dealer_non_quad_vals[-1] < bb_non_quad_vals[-1]:
        return 'bb'
    else:
        return 'tie'


def stronger_fh(dealer_7cc: list, bb_7cc: list):
    """If both players have full houses, returns winner as the player with the higher full house."""
    dealer_values = [c[0] for c in dealer_7cc]
    bb_values = [c[0] for c in bb_7cc]
    dealer_5cc = []
    bb_5cc = []
    
    dealer_mcv = Counter(dealer_values).most_common(1)[0][0]
    dealer_values = [val for val in dealer_values if val != dealer_mcv]
    dealer_second_common_val = Counter(dealer_values).most_common(1)[0][0]
    dealer_second_common_count = Counter(dealer_values).most_common(1)[0][1]
    dealer_values = [val for val in dealer_values if val != dealer_second_common_val]
    dealer_third_common_val = Counter(dealer_values).most_common(1)[0][0]
    dealer_third_common_count = Counter(dealer_values).most_common(1)[0][1]
    
    if dealer_second_common_count == 2 and dealer_third_common_count != 2:
        # If 'standard' full house, appends the trips first and the pair second.
        for i in range(3):
            dealer_5cc.append(dealer_mcv)
        for i in range(2):
            dealer_5cc.append(dealer_second_common_val)
    elif dealer_second_common_count == 3:
        # If a 'double trips' full house checks which trips is higher, appends that first, then two of the lower trips
        # values.
        if card_vals[dealer_mcv] > card_vals[dealer_second_common_val]:
            for i in range(3):
                dealer_5cc.append(dealer_mcv)
            for i in range(2):
                dealer_5cc.append(dealer_second_common_val)
        else:
            for i in range(3):
                dealer_5cc.append(dealer_second_common_val)
            for i in range(2):
                dealer_5cc.append(dealer_mcv)
    else:
        # If 7 card combo consists of trips and 2 pairs appends the trips followed by the higher pair.
        if card_vals[dealer_second_common_val] > card_vals[dealer_third_common_val]:
            for i in range(3):
                dealer_5cc.append(dealer_mcv)
            for i in range(2):
                dealer_5cc.append(dealer_second_common_val)
        else:
            for i in range(3):
                dealer_5cc.append(dealer_mcv)
            for i in range(2):
                dealer_5cc.append(dealer_third_common_val)
    
    bb_mcv = Counter(bb_values).most_common(1)[0][0]
    bb_values = [val for val in bb_values if val != bb_mcv]
    bb_second_common_val = Counter(bb_values).most_common(1)[0][0]
    bb_second_common_count = Counter(bb_values).most_common(1)[0][1]
    bb_values = [val for val in bb_values if val != bb_second_common_val]
    bb_third_common_val = Counter(bb_values).most_common(1)[0][0]
    bb_third_common_count = Counter(bb_values).most_common(1)[0][1]
    
    if bb_second_common_count == 2 and bb_third_common_count != 2:
        # if 'standard' full house, appends the trips first and the pair second
        for i in range(3):
            bb_5cc.append(bb_mcv)
        for i in range(2):
            bb_5cc.append(bb_second_common_val)
    elif bb_second_common_count == 3:
        # if a 'double trips' full house checks which trips is higher, appends that first, then two of the lower trips
        # values to the 5 card combo used to make the full house
        if card_vals[bb_mcv] > card_vals[bb_second_common_val]:
            for i in range(3):
                bb_5cc.append(bb_mcv)
            for i in range(2):
                bb_5cc.append(bb_second_common_val)
        else:
            for i in range(3):
                bb_5cc.append(bb_second_common_val)
            for i in range(2):
                bb_5cc.append(bb_mcv)
    elif bb_second_common_count == 2 and bb_third_common_count == 2:
        # if 7 card combo consists of trips and 2 pairs appends the trips followed by the higher pair to the
        # 5 card combo used to make the full house
        if card_vals[bb_second_common_val] > card_vals[bb_third_common_val]:
            for i in range(3):
                bb_5cc.append(bb_mcv)
            for i in range(2):
                bb_5cc.append(bb_second_common_val)
        else:
            for i in range(3):
                bb_5cc.append(bb_mcv)
            for i in range(2):
                bb_5cc.append(bb_third_common_val)

    if card_vals[dealer_5cc[0]] > card_vals[bb_5cc[0]]:
        return 'dealer'
    elif card_vals[bb_5cc[0]] > card_vals[dealer_5cc[0]]:
        return 'bb'
    elif card_vals[dealer_5cc[0]] == card_vals[bb_5cc[0]] and card_vals[dealer_5cc[3]] > card_vals[bb_5cc[3]]:
        return 'dealer'
    elif card_vals[dealer_5cc[0]] == card_vals[bb_5cc[0]] and card_vals[bb_5cc[3]] > card_vals[dealer_5cc[3]]:
        return 'bb'
    else:
        return 'tie'


def stronger_flush(dealer_7cc: list, bb_7cc: list):
    """If both players have flushes, returns winner as the player with the higher flush. Ties possible."""
    dealer_suits = [c[1] for c in dealer_7cc]
    # Finds the suit that both players use to comprise their flushes. No need to check bb common suit, it must be the 
    # same as flushes of different suits are impossible in a single hand of texas holdem.
    common_suit = Counter(dealer_suits).most_common(1)[0][0]
    # Finds strongest 5 card combo for each player, comprised of cards of suits matching the common_suit variable
    dealer_suited_vals = sorted([card_vals[c[0]] for c in dealer_7cc if c[1] == common_suit])
    bb_suited_vals = sorted([card_vals[c[0]] for c in bb_7cc if c[1] == common_suit])
    dealer_5cc = sorted(dealer_suited_vals[-5:], reverse=True)
    bb_5cc = sorted(bb_suited_vals[-5:], reverse=True)

    # Returns the winner of the hand
    value_tuples = zip(dealer_5cc, bb_5cc)
    for val in value_tuples:
        if val[0] == val[1]:
            pass
        elif val[0] > val[1]:
            return 'dealer'
        else:
            return 'bb'
    return 'tie'


def stronger_straight(dealer_7cc: list, bb_7cc: list):
    dealer_vals = set([card_vals[c[0]] for c in dealer_7cc])
    bb_vals = set([card_vals[c[0]] for c in bb_7cc])
    dealer_vals = sorted(list(dealer_vals))
    bb_vals = sorted(list(bb_vals))

    split_dealer_vals = []
    split_bb_vals = []
    dealer_5cc = []
    bb_5cc = []

    for i in range(len(dealer_vals) - 4):
        split_dealer_vals.append(dealer_vals[i:i+5])
    for five_card_run in split_dealer_vals:
        if five_card_run[-1] - five_card_run[0] == 4:
            dealer_5cc = five_card_run
    for i in range(len(bb_vals) - 4):
        split_bb_vals.append(bb_vals[i:i+5])
    for five_card_run in split_bb_vals:
        if five_card_run[-1] - five_card_run[0] == 4 and len(five_card_run) == len(set(five_card_run)):
            bb_5cc = five_card_run

    if len(dealer_5cc) > 0 and len(bb_5cc) == 0:  # if len({Player}_5cc) = 0 means straight must be A2345 (lowest possible)
        return 'dealer'
    elif len(dealer_5cc) == 0 and len(bb_5cc) > 0:
        return 'bb'
    elif len(dealer_5cc) == 0 and len(bb_5cc) == 0:
        return 'tie'
    elif len(dealer_5cc) > 0 and len(bb_5cc) > 0 and dealer_5cc[1] > bb_5cc[1]:
        return 'dealer'
    elif len(dealer_5cc) > 0 and len(bb_5cc) > 0 and dealer_5cc[1] < bb_5cc[1]:
        return 'bb'
    else:
        return 'tie'


def stronger_trips(dealer_7cc: list, bb_7cc: list):
    dealer_vals = [c[0] for c in dealer_7cc]
    bb_vals = [c[0] for c in bb_7cc]
    # Finds the most common value in players' 7 card combos, i.e. the one they have three of
    dealer_mcv = Counter(dealer_vals).most_common(1)[0][0]
    bb_mcv = Counter(bb_vals).most_common(1)[0][0]
    dealer_5cc = [card_vals[dealer_mcv], card_vals[dealer_mcv], card_vals[dealer_mcv]]
    bb_5cc = [card_vals[bb_mcv], card_vals[bb_mcv], card_vals[bb_mcv]]

    dealer_non_trip_vals = sorted([card_vals[v] for v in dealer_vals if v != dealer_mcv], reverse=True)
    bb_non_trip_vals = sorted([card_vals[v] for v in bb_vals if v != bb_mcv], reverse=True)
    # Appends each players' two best high cards to the trip value to give each of their 5 card combos
    dealer_5cc.append(dealer_non_trip_vals[0])
    dealer_5cc.append(dealer_non_trip_vals[1])
    bb_5cc.append(bb_non_trip_vals[0])
    bb_5cc.append(bb_non_trip_vals[1])

    # Returns the winner of the hand
    if dealer_5cc[0] > bb_5cc[0]:
        return 'dealer'
    elif dealer_5cc[0] < bb_5cc[0]:
        return 'bb'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[3] > bb_5cc[3]:
        return 'dealer'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[3] < bb_5cc[3]:
        return 'bb'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[3] == bb_5cc[3] and dealer_5cc[4] > bb_5cc[4]:
        return 'dealer'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[3] == bb_5cc[3] and dealer_5cc[4] < bb_5cc[4]:
        return 'bb'
    else:
        return 'tie'


def stronger_2p(dealer_7cc: list, bb_7cc: list):
    """If both players have two pair, returns winner as the player with the higher two pair."""
    dealer_values = [c[0] for c in dealer_7cc]
    bb_values = [c[0] for c in bb_7cc]
    dealer_5cc = []
    bb_5cc = []
    
    dealer_mcv = Counter(dealer_values).most_common(1)[0][0]
    dealer_values = [val for val in dealer_values if val != dealer_mcv]
    dealer_2nd_mcv = Counter(dealer_values).most_common(1)[0][0]
    dealer_values = [val for val in dealer_values if val != dealer_2nd_mcv]
    dealer_3rd_mcv = Counter(dealer_values).most_common(1)[0][0]
    dealer_3rd_mcc = Counter(dealer_values).most_common(1)[0][1]
    sorted_remaining_vals = sorted([card_vals[v] for v in dealer_values], reverse=True)
    
    if dealer_3rd_mcc == 1:
        # If 'standard' two pair, appends the highest pair to the 5 card combo first, the lower pair second, and lastly 
        # the highest remaining card
        if dealer_mcv > dealer_2nd_mcv:
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_mcv])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_2nd_mcv])
            dealer_5cc.append(sorted_remaining_vals[0])
        else:
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_2nd_mcv])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_mcv])
            dealer_5cc.append(sorted_remaining_vals[0])
    else:
        # If two pair is comprised of three pairs (still counts as two pair in texas holdem); checks which pairs are 
        # higher, appends highest first, then second highest, finally appends the highest card remaining out of the 
        # third pair and the remaining one card.
        if card_vals[dealer_mcv] > card_vals[dealer_2nd_mcv] > card_vals[dealer_3rd_mcv]:
            highest_remaining_val = max(card_vals[dealer_3rd_mcv], card_vals[dealer_values[-1]])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_mcv])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_2nd_mcv])
            dealer_5cc.append(highest_remaining_val)
        elif card_vals[dealer_mcv] > card_vals[dealer_3rd_mcv] > card_vals[dealer_2nd_mcv]:
            highest_remaining_val = max(card_vals[dealer_2nd_mcv], card_vals[dealer_values[-1]])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_mcv])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_3rd_mcv])
            dealer_5cc.append(highest_remaining_val)
        elif card_vals[dealer_2nd_mcv] > card_vals[dealer_mcv] > card_vals[dealer_3rd_mcv]:
            highest_remaining_val = max(card_vals[dealer_3rd_mcv], card_vals[dealer_values[-1]])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_2nd_mcv])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_mcv])
            dealer_5cc.append(highest_remaining_val)
        elif card_vals[dealer_2nd_mcv] > card_vals[dealer_3rd_mcv] > card_vals[dealer_mcv]:
            highest_remaining_val = max(card_vals[dealer_mcv], card_vals[dealer_values[-1]])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_2nd_mcv])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_3rd_mcv])
            dealer_5cc.append(highest_remaining_val)
        elif card_vals[dealer_3rd_mcv] > card_vals[dealer_mcv] > card_vals[dealer_2nd_mcv]:
            highest_remaining_val = max(card_vals[dealer_2nd_mcv], card_vals[dealer_values[-1]])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_3rd_mcv])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_mcv])
            dealer_5cc.append(highest_remaining_val)
        elif card_vals[dealer_3rd_mcv] > card_vals[dealer_2nd_mcv] > card_vals[dealer_mcv]:
            highest_remaining_val = max(card_vals[dealer_mcv], card_vals[dealer_values[-1]])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_3rd_mcv])
            for i in range(2):
                dealer_5cc.append(card_vals[dealer_2nd_mcv])
            dealer_5cc.append(highest_remaining_val)
    
    bb_mcv = Counter(bb_values).most_common(1)[0][0]
    bb_values = [val for val in bb_values if val != bb_mcv]
    bb_2nd_mcv = Counter(bb_values).most_common(1)[0][0]
    bb_values = [val for val in bb_values if val != bb_2nd_mcv]
    bb_3rd_mcv = Counter(bb_values).most_common(1)[0][0]
    bb_3rd_mcc = Counter(bb_values).most_common(1)[0][1]
    sorted_remaining_vals = sorted([card_vals[v] for v in bb_values], reverse=True)
    
    if bb_3rd_mcc == 1:
        # If 'standard' two pair, appends the highest pair to the 5 card combo first, the lower pair second, and lastly 
        # the highest remaining card
        if bb_mcv > bb_2nd_mcv:
            for i in range(2):
                bb_5cc.append(card_vals[bb_mcv])
            for i in range(2):
                bb_5cc.append(card_vals[bb_2nd_mcv])
            bb_5cc.append(sorted_remaining_vals[0])
        else:
            for i in range(2):
                bb_5cc.append(card_vals[bb_2nd_mcv])
            for i in range(2):
                bb_5cc.append(card_vals[bb_mcv])
            bb_5cc.append(sorted_remaining_vals[0])
    else:
        # If two pair is comprised of three pairs (still counts as two pair in texas holdem); checks which pairs are 
        # higher, appends highest first, then second highest, finally appends the highest card remaining out of the 
        # third pair and the remaining one card.
        if card_vals[bb_mcv] > card_vals[bb_2nd_mcv] > card_vals[bb_3rd_mcv]:
            highest_remaining_val = max(card_vals[bb_3rd_mcv], card_vals[bb_values[-1]])
            for i in range(2):
                bb_5cc.append(card_vals[bb_mcv])
            for i in range(2):
                bb_5cc.append(card_vals[bb_2nd_mcv])
            bb_5cc.append(highest_remaining_val)
        elif card_vals[bb_mcv] > card_vals[bb_3rd_mcv] > card_vals[bb_2nd_mcv]:
            highest_remaining_val = max(card_vals[bb_2nd_mcv], card_vals[bb_values[-1]])
            for i in range(2):
                bb_5cc.append(card_vals[bb_mcv])
            for i in range(2):
                bb_5cc.append(card_vals[bb_3rd_mcv])
            bb_5cc.append(highest_remaining_val)
        elif card_vals[bb_2nd_mcv] > card_vals[bb_mcv] > card_vals[bb_3rd_mcv]:
            highest_remaining_val = max(card_vals[bb_3rd_mcv], card_vals[bb_values[-1]])
            for i in range(2):
                bb_5cc.append(card_vals[bb_2nd_mcv])
            for i in range(2):
                bb_5cc.append(card_vals[bb_mcv])
            bb_5cc.append(highest_remaining_val)
        elif card_vals[bb_2nd_mcv] > card_vals[bb_3rd_mcv] > card_vals[bb_mcv]:
            highest_remaining_val = max(card_vals[bb_mcv], card_vals[bb_values[-1]])
            for i in range(2):
                bb_5cc.append(card_vals[bb_2nd_mcv])
            for i in range(2):
                bb_5cc.append(card_vals[bb_3rd_mcv])
            bb_5cc.append(highest_remaining_val)
        elif card_vals[bb_3rd_mcv] > card_vals[bb_mcv] > card_vals[bb_2nd_mcv]:
            highest_remaining_val = max(card_vals[bb_2nd_mcv], card_vals[bb_values[-1]])
            for i in range(2):
                bb_5cc.append(card_vals[bb_3rd_mcv])
            for i in range(2):
                bb_5cc.append(card_vals[bb_mcv])
            bb_5cc.append(highest_remaining_val)
        elif card_vals[bb_3rd_mcv] > card_vals[bb_2nd_mcv] > card_vals[bb_mcv]:
            highest_remaining_val = max(card_vals[bb_mcv], card_vals[bb_values[-1]])
            for i in range(2):
                bb_5cc.append(card_vals[bb_3rd_mcv])
            for i in range(2):
                bb_5cc.append(card_vals[bb_2nd_mcv])
            bb_5cc.append(highest_remaining_val)
        
    # Returns the winner of the hand.
    if dealer_5cc[0] > bb_5cc[0]:
        return 'dealer'
    elif bb_5cc[0] > dealer_5cc[0]:
        return 'bb'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[2] > bb_5cc[2]:
        return 'dealer'
    elif dealer_5cc[0] == bb_5cc[0] and bb_5cc[2] > dealer_5cc[2]:
        return 'bb'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[2] == bb_5cc[2] and dealer_5cc[-1] > bb_5cc[-1]:
        return 'dealer'
    elif dealer_5cc[0] == bb_5cc[0] and bb_5cc[2] == dealer_5cc[2] and dealer_5cc[-1] < bb_5cc[-1]:
        return 'bb'
    else:
        return 'tie'


def stronger_pair(dealer_7cc: list, bb_7cc: list):
    dealer_vals = [c[0] for c in dealer_7cc]
    bb_vals = [c[0] for c in bb_7cc]
    # Finds the most common value in players' 7 card combos, i.e. the one they have two of.
    dealer_mcv = Counter(dealer_vals).most_common(1)[0][0]
    bb_mcv = Counter(bb_vals).most_common(1)[0][0]
    dealer_5cc = [card_vals[dealer_mcv], card_vals[dealer_mcv]]
    bb_5cc = [card_vals[bb_mcv], card_vals[bb_mcv]]
    
    dealer_non_trip_vals = sorted([card_vals[v] for v in dealer_vals if v != dealer_mcv], reverse=True)
    bb_non_trip_vals = sorted([card_vals[v] for v in bb_vals if v != bb_mcv], reverse=True)
    # Appends the strongest 3 high cards each player has to their respective 5 card combo.
    dealer_5cc.append(dealer_non_trip_vals[0])
    dealer_5cc.append(dealer_non_trip_vals[1])
    dealer_5cc.append(dealer_non_trip_vals[2])
    bb_5cc.append(bb_non_trip_vals[0])
    bb_5cc.append(bb_non_trip_vals[1])
    bb_5cc.append(bb_non_trip_vals[2])
    # Returns the winner of the hand.
    if dealer_5cc[0] > bb_5cc[0]:
        return 'dealer'
    elif dealer_5cc[0] < bb_5cc[0]:
        return 'bb'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[2] > bb_5cc[2]:
        return 'dealer'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[2] < bb_5cc[2]:
        return 'bb'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[2] == bb_5cc[2] and dealer_5cc[3] > bb_5cc[3]:
        return 'dealer'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[2] == bb_5cc[2] and dealer_5cc[3] < bb_5cc[3]:
        return 'bb'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[2] == bb_5cc[2] and dealer_5cc[3] == bb_5cc[3] and dealer_5cc[4] > bb_5cc[4]:
        return 'dealer'
    elif dealer_5cc[0] == bb_5cc[0] and dealer_5cc[2] == bb_5cc[2] and dealer_5cc[3] == bb_5cc[3] and dealer_5cc[4] < bb_5cc[4]:
        return 'bb'
    else:
        return 'tie'


def stronger_hc(dealer_7cc: list, bb_7cc: list):
    # Gets the top 5 cards for each player in descending order i.e. strongest card first
    dealer_vals = sorted([card_vals[c[0]] for c in dealer_7cc])
    bb_vals = sorted([card_vals[c[0]] for c in bb_7cc])
    dealer_5cc = sorted(dealer_vals[-5:], reverse=True)
    bb_5cc = sorted(bb_vals[-5:], reverse=True)

    # Returns the winner of the hand
    value_tuples = zip(dealer_5cc, bb_5cc)
    for val in value_tuples:
        if val[0] == val[1]:
            pass
        elif val[0] > val[1]:
            return 'dealer'
        else:
            return 'bb'
    return 'tie'


def tests():
    """Ensures the above functions output as expected."""
    print(stronger_sf(['Kc','Ac','Qc','Tc','3c','4c','Jc'], ['9c','8c','Qc','Tc','3c','4c','Jc']))  # dealer
    print(stronger_sf(['7d','Ac','8d','Td','9d','4c','Jd'], ['Kd','Ac','Qd','Td','9d','4c','Jd']))  # bb
    print(stronger_sf(['Kc','Qc','Jc','2h','Jh','Ac','Tc'], ['Kc','Qc','5c','9c','3c','Tc','Jc']))  # dealer
    print(stronger_sf(['Kc','Qc','Jc','2h','Jh','9c','Tc'], ['Kc','Qc','5c','9c','3c','Tc','Jc']))  # tie
    print(stronger_sf(['Kc','Qc','Jc','2h','Jh','Ac','Tc'], ['Ac','2c','5c','9c','3c','4c','Jc']))  # dealer
    print(stronger_sf(['9c','Qc','Jc','7c','Jh','8c','Tc'], ['Kc','Qc','5c','9c','3c','Tc','Jc']))  # bb
    print(stronger_quads(['Kc','Kd','Ks','Kh','3c','4c','Jc'], ['Ac','Ad','As','Ah','3c','4c','Jc']))  # bb
    print(stronger_quads(['Kc','Kd','Ks','Kh','3c','4c','Jc'], ['2c','2d','2s','2h','3c','4c','Jc']))  # dealer
    print(stronger_quads(['Kc','Kd','Ks','Kh','3c','4c','Ac'], ['Kc','Kd','Ks','Kh','3c','4c','Jc']))  # dealer
    print(stronger_quads(['Kc','Kd','Ks','Kh','3c','4c','Ac'], ['Kc','Kd','Ks','Kh','Ac','4c','Jc']))  # tie
    print(stronger_fh(['Kc','Kd','Ks','3h','3c','4c','Jc'], ['Ac','Ad','As','3h','3c','4c','Jc']))  # bb
    print(stronger_fh(['Kc','Kd','Ks','3h','3c','4c','Jc'], ['5c','5d','5s','3h','3c','4c','Jc']))  # dealer
    print(stronger_fh(['Kc','Kd','Ks','3h','3c','3c','Jc'], ['Qc','Ad','As','Qh','Qc','Ac','Jc']))  # bb
    print(stronger_fh(['Kc','Kd','Ks','2h','2c','3c','3c'], ['Kc','Kd','Ks','3h','3c','Ac','Jc']))  # tie
    print(stronger_flush(['Kc','Qc','5c','2h','2c','3c','3d'], ['Kc','Qc','5c','3h','3c','Ac','Jc']))  # bb
    print(stronger_flush(['Kc','Qc','5c','2h','2c','Ac','3d'], ['Kc','Qc','5c','3h','3c','Ac','Jc']))  # bb
    print(stronger_flush(['Kc','Qc','5c','2h','Jc','Ac','3d'], ['Kc','Qc','5c','3h','3c','Ac','Jc']))  # tie
    print(stronger_straight(['Kc','Qd','Jc','2h','Jc','Ac','Td'], ['Kc','Qd','5c','9h','3c','Tc','Jc']))  # dealer
    print(stronger_straight(['Kc','Qd','Jc','2h','Jc','9c','Td'], ['Kc','Qd','5c','9h','3c','Tc','Jc']))  # tie
    print(stronger_straight(['Kc','Qd','Jc','8h','Jc','9c','Td'], ['Kc','Qd','5c','9h','3c','Tc','Jc']))  # tie
    print(stronger_straight(['2c','3d','4c','2h','5c','Ac','Td'], ['Kc','Qd','5c','Ah','3c','Tc','Jc']))  # bb
    print(stronger_straight(['2c','3d','4c','2h','5c','Ac','Td'], ['2c','4d','5c','Ah','3c','Tc','Jc']))  # tie
    print(stronger_trips(['Kc','Kd','Ks','2h','Jc','Ac','3d'], ['Kc','Kd','Kh','7h','3c','Ac','Jc']))  # tie
    print(stronger_trips(['Kc','Kd','Ks','2h','Jc','Ac','3d'], ['Qc','Qd','Qh','7h','3c','Ac','Jc']))  # dealer
    print(stronger_trips(['Kc','Kd','Ks','2h','Jc','Ac','3d'], ['Kc','Kd','Kh','7h','3c','Qc','Jc']))  # dealer
    print(stronger_trips(['Kc','Kd','Ks','2h','Jc','Ac','3d'], ['Kc','Kd','Kh','7h','3c','Ac','Tc']))  # dealer
    print(stronger_2p(['Kc','Kd','2s','2h','Jc','Ac','3d'], ['Kc','Kd','7h','7h','3c','Ac','Tc']))  # bb
    print(stronger_2p(['Kc','Kd','7s','7h','Jc','Ac','3d'], ['Kc','Kd','7h','7h','3c','Ac','Tc']))  # tie
    print(stronger_2p(['Kc','Kd','7s','7h','Jc','Qc','3d'], ['Kc','Kd','7h','7h','3c','Ac','Tc']))  # bb
    print(stronger_2p(['Kc','Kd','7s','7h','Ac','Ac','3d'], ['Kc','Kd','7h','7h','3c','Ac','Tc']))  # dealer
    print(stronger_2p(['Kc','Kd','7s','7h','Jc','Jc','3d'], ['Kc','Kd','9h','9h','Tc','Ac','Tc']))  # dealer
    print(stronger_2p(['Kc','Kd','7s','Jh','Jc','7c','Ad'], ['Kc','Kd','7h','7h','Jc','Qc','Jc']))  # bb
    print(stronger_pair(['Kc','Kd','4s','2h','Jc','Ac','3d'], ['Qc','8d','Ah','7h','3c','Ac','Jc']))  # bb
    print(stronger_pair(['Ac','Kd','4s','2h','Jc','Ac','3d'], ['Qc','8d','Ah','7h','3c','Ac','Jc']))  # dealer
    print(stronger_pair(['Kc','Kd','8s','2h','Jc','Ac','3d'], ['Kc','8d','Ah','7h','3c','Kc','Jc']))  # tie
    print(stronger_pair(['Kc','Kd','6s','2h','Jc','Ac','3d'], ['Kc','8d','Ah','7h','3c','Kc','Jc']))  # bb
    print(stronger_pair(['Kc','Kd','4s','2h','Jc','Ac','3d'], ['Qc','8d','Ah','7h','3c','Ac','Jc']))  # bb
    print(stronger_hc(['Kc','Qd','5c','2h','Jc','Ac','3d'], ['Kc','Qd','5c','7h','3c','Ac','Jc']))  # bb
    print(stronger_hc(['Kc','Qd','5c','2h','Jc','Ac','3d'], ['Kc','Qd','5c','7h','3c','4c','Jc']))  # dealer
    print(stronger_hc(['Kc','Qd','5c','2h','Jc','Ac','3d'], ['Kc','Qd','5c','Ah','3c','4c','Jc']))  # tie
