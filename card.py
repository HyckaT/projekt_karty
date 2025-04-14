from custom_exceptions import CardNotFound

card_suits = ["♥", "♠", "♦", "♣"]
card_values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suit_dict = {"♠": "_piky", "♥": "_herce", "♦": "_kule", "♣": "_kříže"}
# J, Q, K se počítá za 10, A za 1 nebo 11 dle uvážení

# třída pro vytváření objektů karet do hry
class Card:
    def __init__(self, suit, value):
        self.name = value + suit_dict[suit]
        self.suit = suit
        self.value = value
        
    #vypíše hodnoty karty
    def get_card(self):
        print(f"Karta je {self.suit}{self.value}")

    #metoda k možnému zápisu karty do adresáře - vyřeš
    # def to_dict(self):
    #     return {"suit": self.suit, "value": self.value}
    #     raise CardNotFound("Text vyjímky")

