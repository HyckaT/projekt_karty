from flask import Flask, render_template, jsonify, session
import module   # soubor s třídou karta

app = Flask(__name__)
app.secret_key = "secret_code"


# Počítání hodnoty karet v ruce
def value_counter(deck_content):
    ace_over21(deck_content)
    return sum(card["value"] for card in deck_content)


def ace_over21(deck_content):
    total = sum(card["value"] for card in deck_content)

    # Zatímco máme A = 11 a součet je >21, přepisujeme A na 1
    for card in deck_content:
        if total > 21 and card["value"] == 11:
            card["value"] = 1
            total -= 10  # protože jsme z 11 udělali 1
    return deck_content


# Rozdání karet na začátku hry
@app.route('/')
def index():
    deck = session.get("deck")
    player_cash = session.get("player_cash", 5000)
    bet_amount = session.get("bet_amount", 0)


    if not deck or len(deck) < 18:  # méně než 35 % karet v balíčku
        deck = [card.to_dict() for card in module.deck_generator()]
        session["deck"] = deck
        print({"message": "novy bnalicek!"})

    if bet_amount == 0:
        return render_template("index.html", player_cash=player_cash, bet_amount=0,
                               player_score=0, dealer_score=0,
                               player_cards=[], dealer_cards=[
                                   {"symbol": "?", "value": "?", "image": "/static/images/back.png"},
                                   {"symbol": "?", "value": "?", "image": "/static/images/back.png"},
                               ])

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    session["deck"] = deck 
    session["player_hand"] = player_hand
    session["dealer_hand"] = dealer_hand
    session["game_over"] = False

    player_score = value_counter(player_hand)

    return render_template("index.html", player_score=player_score, dealer_score=dealer_hand[0]["value"],
                            player_cash=player_cash,
                            bet_amount=bet_amount,
                            player_cards=player_hand,
                            dealer_cards=[dealer_hand[0], {"symbol": "?", "value": "?", "image": "/static/images/back.png"}])

@app.route('/bet/<int:amount>')
def bet(amount):
    player_cash = session.get("player_cash", 5000)

    if amount <= 0:
        return jsonify({"error": "Zadej částku větší než 0."})

    if amount > player_cash:
        return jsonify({"error": "Nedostatek peněz!"})

    player_cash -= amount
    session["player_cash"] = player_cash
    session["bet_amount"] = amount

    # Po úspěšné sázce rovnou rozdáme karty
    deck = session.get("deck")
    if not deck or len(deck) < 18:
        deck = [card.to_dict() for card in module.deck_generator()]

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    session["deck"] = deck
    session["player_hand"] = player_hand
    session["dealer_hand"] = dealer_hand

    player_score = value_counter(player_hand)


    if player_score == 21:
        print("BLACKJACK!")
        winnings = int(amount * 2.5)
        player_cash += winnings
        session["player_cash"] = player_cash
        session["bet_amount"] = 0
        session["game_over"] = True

        return jsonify({
            "message": "BLACKJACK! Vyhrál jsi!",
            "player_cash": player_cash,
            "player_score": player_score,
            "dealer_score": dealer_hand[0]["value"],
            "player_cards": player_hand,
            "bet_amount": amount,
            "dealer_cards": [dealer_hand[0], {"symbol": "?", "value": "?", "image": "/static/images/back.png"}]
        })


    session["game_over"] = False
    session["player_cash"] = player_cash
    session["bet_amount"] = amount

    return jsonify({
        "player_cash": player_cash,
        "bet_amount": amount,
        "player_cards": player_hand,
        "dealer_cards": [dealer_hand[0], {"symbol": "?", "value": "?", "image": "/static/images/back.png"}],
        "player_score": player_score,
        "dealer_score": dealer_hand[0]["value"]
    })



@app.route('/tahni_kartu')
def tahni_kartu():
    if session.get("game_over"):
        return jsonify({"message": "Hra skončila, začni novou!"})
    
    deck = session.get("deck", [])
    player_hand = session.get("player_hand", [])

    if not deck:  
        return jsonify({"message": "Balíček je prázdný!"})
    
    new_card = deck.pop()  
    player_hand.append(new_card)  
    session["deck"] = deck 
    session["player_hand"] = player_hand

    player_score = value_counter(player_hand)

    response_data = {
        "image": new_card["image"],
        "symbol": new_card["symbol"],
        "value": new_card["value"],
        "player_score": player_score
    }
    if player_score == 21:
        session["game_over"] = True
        response_data["message"] = "Vyhrál jsi!"
        session["player_cash"] = session.get("player_cash", 0) + session.get("bet_amount", 0) * 2
        session["bet_amount"] = 0
        response_data["player_cash"] = session["player_cash"]


    if player_score > 21:
        session["game_over"] = True
        response_data["message"] = "Přetáhl jsi! Prohráváš."
        session["bet_amount"] = 0
        response_data["player_cash"] = session.get("player_cash", 0)

        if session.get("player_cash", 0) <= 0:
            session.clear()
            response_data["restart"] = True

    
    return jsonify(response_data)


# Hráč stojí, dealer hraje
@app.route('/stand')
def stand():
    if session.get("game_over"):
        return jsonify({"message": "Hra skončila, začni novou!"})

    deck = session.get("deck", [])
    player_hand = session.get("player_hand", [])
    dealer_hand = session.get("dealer_hand", [])

    while value_counter(dealer_hand) < 17:
        dealer_hand.append(deck.pop())

    session["dealer_hand"] = dealer_hand
    session["game_over"] = True

    player_score = value_counter(player_hand)
    dealer_score = value_counter(dealer_hand)
    player_cash = session.get("player_cash", 0)
    bet_amount = session.get("bet_amount", 0)


    if dealer_score > 21 or player_score > dealer_score:
        result = "Vyhrál jsi!"
        player_cash += bet_amount * 2
    elif player_score < dealer_score:
        result = "Prohrál jsi!"
        session["bet_amount"] = 0

        if session.get("player_cash", 0) <= 0:
            session.clear()
            return jsonify({
            "player_hand": player_hand,
            "dealer_hand": dealer_hand,
            "player_score": player_score,
            "dealer_score": dealer_score,
            "player_cash": player_cash,
            "message": result + " Spouštím novou hru.",
            "restart": True
        })
    else:
        result = "Remíza!"
        player_cash += bet_amount

    session["player_cash"] = player_cash
    session["bet_amount"] = 0  # reset bet_amount

    return jsonify({
        "message": result,
        "player_hand": player_hand,
        "dealer_hand": dealer_hand,
        "player_score": player_score,
        "dealer_score": dealer_score,
        "player_cash": player_cash
    })

# Restart hry
@app.route('/restart')
def restart():
    return jsonify({"message": "Hra byla restartována, začni novou!"})

if __name__ == "__main__":
    app.run(debug=True)
