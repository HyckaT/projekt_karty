from card import Card
from deck_of_cards import DeckOfCards
from custom_exceptions import CardNotFound

#založení objektů karet z balíčku 52 karet
karta_1 = Card(suit="♥",value="5")
#zkouška přepisu karty1
karta_1 = Card(suit="♥",value="7")
karta_2 = Card(suit="♠",value="A")
karta_3 = Card(suit="♣",value="10")

#karty krupiera
karty_krupiera = DeckOfCards()
karty_krupiera.add_card(karta_3)

#karty hráče
karty_hrace = DeckOfCards()
karty_hrace.add_card(karta_1)
karty_hrace.add_card(karta_2)

#zkouška prázdného balíčku karet
prazdny_balicek_karet = DeckOfCards()

# tady při odebírání na špatné neexistující pozici karty vypíše chybu
karty_hrace.remove_card(5)

#výpis karet hráče vs. krupiera + počty
print("________________________")
karty_krupiera.view_cards()
print(f"Krupier má {karty_krupiera.count_of_cards()} kartu(y).")
print("________________________")
karty_hrace.view_cards()
print(f"Hráč má {karty_hrace.count_of_cards()} kartu(y).")
print("________________________")
prazdny_balicek_karet.view_cards()
#volání metod karet
#karta_1.get_card()
#karta_2.get_card()

