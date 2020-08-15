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

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def __str__(self):
        return (f'Current hand: {", ".join(self.hand)} Score: {self.score}')

    def pick_card(self, card):
        self.hand.append(card)
        return self.hand

    def clear_deck(self):
        self.hand.clear()

    def calculate_score(self):
        face_card = {'A': 1, 'K': 10, 'Q': 10, 'J': 10}
        for card in self.hand:
            if card[0] in face_card:
                self.score += face_card[card[0]]
            elif card[0] == '8':
                self.score += 50
            else:
                self.score += int(card[0])
        return self.score

    def check_card_can_be_played(self, card, facedown_card):
        global new_card_drawn
        status = False
        if new_card_drawn:
            if card[0:-1] == facedown_card[0:-1]:
                facedown_card = card
                status = True
            elif card[-1] == facedown_card[-1]:
                status = True
                facedown_card = card
            new_card_drawn = False
        elif card[0:-1] == facedown_card[0:-1]:
            facedown_card = card
            self.hand.remove(card)
            status = True

        elif card[-1] == facedown_card[-1]:
            facedown_card = card
            self.hand.remove(card)
            status = True

        elif card[0] == '8':
            facedown_card = card
            self.hand.remove(card)
            status = True

        else:
            print(f'You can\'t play this card {card} on face down card {facedown_card}')

        return status, facedown_card

    def pick_atmost3_cards(self, facedown_card, deck):
        global new_card_drawn
        end_game = False
        for i in range(3):
            if len(deck) > 0:
                print(f'{self.name} is picking {i + 1} card:')
                new_card = deck.pop()
                new_card_drawn = True
                status, facedown_card = self.check_card_can_be_played(new_card, facedown_card)
                if status == True:
                    return deck, facedown_card, end_game
                else:
                    self.pick_card(new_card)
            else:
                end_game = True
                return deck, facedown_card, end_game
        return deck, facedown_card, True if len(deck) == 0 else False

    def player_play(self, facedown_card, deck):
        print(f'{self.name} turn:')
        end_game = False
        while True:
            try:
                print(f'Current deck: {self.hand}, face down card is: {facedown_card}, total cards in hand: {len(self.hand)}, total cards remaining in deck: {len(deck)}')
                choice = input(f'Enter the index of the card you want to play, to pick a card enter --pick or to read the rules by entering --help: ')
                if choice == '--help':
                    read_rules()
                    continue
                elif choice == '--pick':
                    deck, facedown_card, end_game = self.pick_atmost3_cards(facedown_card, deck)
                    return deck, facedown_card, end_game
                elif choice.isnumeric():
                    status, facedown_card = self.check_card_can_be_played(self.hand[int(choice)], facedown_card)
                    if not status:
                        deck, facedown_card, end_game = self.pick_atmost3_cards(facedown_card, deck)
                        return deck, facedown_card, end_game

                    return deck, facedown_card, end_game
            except ValueError:
                print('Entered index should be an integer')
            except IndexError:
                print('Entered index is out of range')

