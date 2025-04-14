from custom_exceptions import CardNotFound

#balíček karet
class DeckOfCards:
 
    def __init__(self):
        self.datasorage = []
        self.counter = 0
    
    def count_of_cards(self):
        return self.counter

    def add_card(self, card: list):
        #přidá do balíčku novou další kartu
        self.datasorage.append(card)
        self.counter += 1

    def remove_card(self, position):
        #odebere kartu na dané pozici
        try:
            self.datasorage.pop(position)
            self.counter -= 1
        except Exception:
            CardNotFound()

    def view_cards(self):
        """Metoda vypíše všechny karty v adresáři"""
        for card in self.datasorage:
            card.get_card()