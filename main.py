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

def fetch_face_card(deck):
    facedown_card = deck.pop()
    while True:
        if facedown_card[0] == '8':
            deck.insert(int(len(deck) / 2), facedown_card)
        else:
            break
    return facedown_card, deck

def read_rules():
    with open('rules.txt', 'r') as rule:
        print(rule.read())
        while True:
            resume = input('Enter --resume to continue the game: ')
            if resume != '--resume':
                print('Continue reading...')
            else:
                return