import Hand_Strengths
import Same_Strength_Deciders
from random import shuffle
from Players import Player


class Deck:
        """List of 52 ordered cards, in format '{val}{suit}'."""
        suits = list('hsdc')
        vals = [str(n) for n in range(2, 10)] + list('TJQKA')

        def __init__(self):
            self._cards = [val + suit for val in self.vals for suit in self.suits]

        def __len__(self):
            return len(self._cards)

        def __setitem__(self, position, card):
            self._cards[position] = card

        def __getitem__(self, position):
            return self._cards[position]

        def __repr__(self):
            print('<Deck of 52 ordered cards in format: "{val}{suit}">')


def shuffle_deck(deck: Deck):
    shuffle(deck)
    return deck[:]


class NewHand:

    def __init__(self, dealer: Player, bb: Player):
        self.dealer = dealer
        self.bb = bb
        self.pot = 0
        self.deck = shuffle_deck(Deck())
        self.dealer_hand = [self.deck[1], self.deck[3]]
        self.bb_hand = [self.deck[0], self.deck[2]]
        self.community_cards = [self.deck[5], self.deck[6], self.deck[7], self.deck[9], self.deck[11]]
        # community cards are not [deck[4], deck[5], deck[6], deck[7], deck[8]] as cards are 'burned' before each street
        self.dealer_7cc = self.dealer_hand + self.community_cards
        self.bb_7cc = self.bb_hand + self.community_cards
        self.player_folded = False
        self.winner = None

    def take_blinds(self):
        self.dealer.stack -= 0.50
        self.dealer.put_in_pot_pre += 0.50
        self.bb.stack -= 1.00
        self.bb.put_in_pot_pre += 1.00
        self.pot += 1.50

    def get_winner(self):
        """Finds the winner of the hand and assigns it to self.winner. MUST RUN get_deck, get_hands_and_community_cards
        AND get_7ccs before running this function"""
        # Initialises hand strength as 0 (corresponding to high card, the lowest possible strength)
        dealer_strength = 0
        bb_strength = 0
        # Sequentially checks for stronger and stronger hands
        if Hand_Strengths.is_pair(self.dealer_7cc):
            dealer_strength = 1
        elif Hand_Strengths.is_two_pair(self.dealer_7cc):
            dealer_strength = 2
        elif Hand_Strengths.is_trips(self.dealer_7cc):
            dealer_strength = 3
        elif Hand_Strengths.is_straight(self.dealer_7cc):
            dealer_strength = 4
        elif Hand_Strengths.is_flush(self.dealer_7cc):
            dealer_strength = 5
        elif Hand_Strengths.is_full_house(self.dealer_7cc):
            dealer_strength = 6
        elif Hand_Strengths.is_quads(self.dealer_7cc):
            dealer_strength = 7
        elif Hand_Strengths.is_straight_flush(self.dealer_7cc):
            dealer_strength = 8
        
        if Hand_Strengths.is_pair(self.bb_7cc):
            bb_strength = 1
        elif Hand_Strengths.is_two_pair(self.bb_7cc):
            bb_strength = 2
        elif Hand_Strengths.is_trips(self.bb_7cc):
            bb_strength = 3
        elif Hand_Strengths.is_straight(self.bb_7cc):
            bb_strength = 4
        elif Hand_Strengths.is_flush(self.bb_7cc):
            bb_strength = 5
        elif Hand_Strengths.is_full_house(self.bb_7cc):
            bb_strength = 6
        elif Hand_Strengths.is_quads(self.bb_7cc):
            bb_strength = 7
        elif Hand_Strengths.is_straight_flush(self.bb_7cc):
            bb_strength = 8

        # Finds the winner of the hand. N.B. all functions called from the Same_Strength_Deciders module return
        # 'dealer', 'bb' or 'tie'.
        if dealer_strength > bb_strength:
            self.winner = 'dealer'
        elif dealer_strength == bb_strength == 0:
            self.winner = Same_Strength_Deciders.stronger_hc(self.dealer_7cc, self.bb_7cc)
        elif dealer_strength == bb_strength == 1:
            self.winner = Same_Strength_Deciders.stronger_pair(self.dealer_7cc, self.bb_7cc)
        elif dealer_strength == bb_strength == 2:
            self.winner = Same_Strength_Deciders.stronger_2p(self.dealer_7cc, self.bb_7cc)
        elif dealer_strength == bb_strength == 3:
            self.winner = Same_Strength_Deciders.stronger_trips(self.dealer_7cc, self.bb_7cc)
        elif dealer_strength == bb_strength == 4:
            self.winner = Same_Strength_Deciders.stronger_straight(self.dealer_7cc, self.bb_7cc)
        elif dealer_strength == bb_strength == 5:
            self.winner = Same_Strength_Deciders.stronger_flush(self.dealer_7cc, self.bb_7cc)
        elif dealer_strength == bb_strength == 6:
            self.winner = Same_Strength_Deciders.stronger_fh(self.dealer_7cc, self.bb_7cc)
        elif dealer_strength == bb_strength == 7:
            self.winner = Same_Strength_Deciders.stronger_quads(self.dealer_7cc, self.bb_7cc)
        elif dealer_strength == bb_strength == 8:
            self.winner = Same_Strength_Deciders.stronger_sf(self.dealer_7cc, self.bb_7cc)
        else:
            self.winner = 'bb'

    def allocate_pot(self):
        if self.winner == 'dealer':
            print(f'{self.dealer.name} wins the hand!')
            self.dealer.stack += self.pot
        elif self.winner == 'bb':
            print(f'{self.bb.name} wins the hand!')
            self.bb.stack += self.pot
        else:
            print('The hand is a tie')
            self.dealer.stack += self.pot / 2
            self.bb.stack += self.pot / 2
