from random import shuffle

new_card_drawn = False

def create_deck():
    deck = []
    suits = ['♠', '♡', '♢', '♣']
    face_cards = ['A', 'J', 'Q', 'K']
    for suit in suits:
        for card in range(2, 11):
            deck.append(f'{card}{suit}')
        for face in face_cards:
            deck.append(f'{face}{suit}')
    shuffle(deck)
    return deck