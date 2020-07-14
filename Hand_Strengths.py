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
card_vals_al = {
    'A': 1,
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


def is_straight_flush(cards: list):
    """ Returns True if there are 5 sequential cards of the same suit in the seven cards passed to the function. """
    assert len(cards) == 7  # Replace with custom error!!!
    suits = [c[1] for c in cards]
    common_suit = Counter(suits).most_common(1)[0][0]
    cards_of_common_suit = [c for c in cards if c[1] == common_suit]
    if len(cards_of_common_suit) < 5:
        return False
    values = []
    for c in cards_of_common_suit:
        values.append(card_vals_al[c[0]])
    values = sorted(values)
    split_values = []
    for i in range(len(values) - 4):
        split_values.append(values[i:i+5])
    for five_card_run in split_values:
        if five_card_run[-1] - five_card_run[0] == 4:
            return True
    values = []
    for c in cards_of_common_suit:
        values.append(card_vals[c[0]])
    values = sorted(values)
    split_values = []
    for i in range(len(values) - 4):
        split_values.append(values[i:i+5])
    for five_card_run in split_values:
        if five_card_run[-1] - five_card_run[0] == 4:
            return True
    return False


def is_quads(cards: list):
    """ Returns True if there are 4 or more cards of the same value in the seven cards passed to the function. Assumes
    that all stronger hand classes have been discounted, therefore does not check for straight flushes."""
    assert len(cards) == 7
    values = [c[0] for c in cards]
    most_common_val_count = Counter(values).most_common(1)[0][1]
    if most_common_val_count != 4:
        return False
    return True


def is_full_house(cards: list):
    """ Returns True if there 3 of the most common card, and either 2 or 3 of the second most common card in the seven
    cards passed to the function. Assumes that all stronger hand classes have been discounted, therefore does not check
    for straight flushes, quads. """
    assert len(cards) == 7
    values = [c[0] for c in cards]
    most_common_val_count = Counter(values).most_common(1)[0][1]
    if most_common_val_count != 3:
        return False
    values = [v for v in values if v != Counter(values).most_common(1)[0][0]]
    second_most_common_val_count = Counter(values).most_common(1)[0][1]
    if second_most_common_val_count not in [2, 3]:
        return False
    return True


def is_flush(cards: list):
    """ Returns True if there are 5 or more cards of the same suit in the seven cards passed to the function. Assumes
    that all stronger hand classes have been discounted, therefore does not check for straight flushes, quads etc. """
    assert len(cards) == 7
    suits = [c[1] for c in cards]
    most_common_suit_count = Counter(suits).most_common(1)[0][1]
    if most_common_suit_count < 5:
        return False
    return True


def is_straight(cards: list):
    """ Returns True if there are 5 sequential cards in the seven cards passed to the function. Assumes that all
    stronger hand classes have been discounted, therefore does not check for straight flushes, quads etc."""
    assert len(cards) == 7
    values = []
    for c in cards:
        values.append(card_vals_al[c[0]])
    values = sorted(values)
    split_values = []
    for i in range(3):
        split_values.append(values[i:i+5])
    for five_card_run in split_values:
        if five_card_run[-1] - five_card_run[0] == 4 and len(five_card_run) == len(set(five_card_run)):
            return True
    values = []
    for c in cards:
        values.append(card_vals[c[0]])
    values = sorted(values)
    split_values = []
    for i in range(3):
        split_values.append(values[i:i+5])
    for five_card_run in split_values:
        if five_card_run[-1] - five_card_run[0] == 4 and len(five_card_run) == len(set(five_card_run)):
            return True
    return False


def is_trips(cards: list):
    """ Returns True if there 3 of the most common card in the seven cards passed to the function. Assumes that all
    stronger hand classes have been discounted, therefore does not check for flushes, full houses etc. """
    assert len(cards) == 7
    values = [c[0] for c in cards]
    most_common_val_count = Counter(values).most_common(1)[0][1]
    if most_common_val_count != 3:
        return False
    return True


def is_two_pair(cards: list):
    """ Returns True if there 2 of the most common card, and 2 of the second most common card in the seven cards passed
    to the function. Assumes that all stronger hand classes have been discounted, therefore does not check for straight
    flushes, quads. """
    assert len(cards) == 7
    values = [c[0] for c in cards]
    most_common_val_count = Counter(values).most_common(1)[0][1]
    if most_common_val_count != 2:
        return False
    values = [v for v in values if v != Counter(values).most_common(1)[0][0]]
    second_most_common_val_count = Counter(values).most_common(1)[0][1]
    if second_most_common_val_count != 2:
        return False
    return True


def is_pair(cards: list):
    """ Returns True if there 2 of the most common card in the seven cards passed to the function. Assumes that all
    stronger hand classes have been discounted, therefore does not check for flushes, full houses etc. """
    assert len(cards) == 7
    values = [c[0] for c in cards]
    most_common_val_count = Counter(values).most_common(1)[0][1]
    if most_common_val_count != 2:
        return False
    return True


def tests():
    print(is_straight_flush(['7c', 'Ac', 'Qc', 'Tc', '3c', '4c', 'Jc']))  # False
    print(is_straight_flush(['2c', 'Ac', '5c', 'Tc', '3c', '4c', 'Jd']))  # True
    print(is_straight_flush(['Kd', 'Ac', 'Qc', 'Tc', '3c', '4c', 'Jc']))  # False
    print(is_quads(['Qc', 'Qs', 'Qd', 'Qh', 'Kh', 'Kc', 'Jd']))  # True
    print(is_quads(['Qc', 'Qs', 'Qd', 'Ks', 'Kh', 'Kc', 'Jd']))  # False
    print(is_flush(['Qc', '8s', 'Qs', 'Kc', 'Kd', 'Ks', 'Js']))  # False
    print(is_flush(['Qc', '8s', 'Qs', 'Kc', 'Ts', 'Ks', 'Js']))  # True
    print(is_straight(['Tc', '8s', 'Qs', '9c', 'Kd', 'Ks', 'Js']))  # True
    print(is_straight(['Tc', '8s', 'Qs', 'Jc', 'Kd', 'Ks', 'Js']))  # False
    print(is_trips(['Tc', '8s', 'Qs', '9c', 'Kd', 'Ks', 'Js']))  # False
    print(is_trips(['Kc', '8s', 'Qs', '9c', 'Kd', 'Ks', 'Js']))  # True
    print(is_two_pair(['Tc', '8s', 'Qs', '9c', 'Kd', 'Ks', 'Js']))  # False
    print(is_two_pair(['Jc', '8s', 'Qs', '9c', 'Kd', 'Ks', 'Js']))  # True
    print(is_pair(['Tc', '8s', 'Qs', '9c', 'Kd', 'Ks', 'Js']))  # True
    print(is_pair(['Tc', '8s', 'Qs', '9c', 'Kd', 'As', 'Js']))  # False
