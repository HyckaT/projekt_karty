import random

card_suits = ['♥', '♠', '♦', '♣']
card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

suit_dict = {'♠': 'S', '♥': 'H', '♦': 'D', '♣': 'C'}

# třída karta
class Card:
    def __init__(self, suit, value, num_value):
        self.name = value + suit_dict[suit]
        self.suit = suit
        self.value = num_value
        self.image = f"/static/images/{self.name}.png"

    def to_dict(self):
        return {"symbol": self.name, "value": self.value, "image": self.image}

def deck_generator():
    main_deck = []  
    for suit in card_suits:
        for value in card_values:
            if value == 'A':
                num_value = 11
            elif value in ['J', 'Q', 'K']:
                num_value = 10
            else:
                num_value = int(value)

            main_deck.append(Card(suit, value, num_value))
            random.shuffle(main_deck)
    return main_deck