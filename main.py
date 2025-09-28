import random
cards_num = 52
players = 0
cards = {"ace":4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4, 10:4, "jack":4, "queen":4, "king":4}
player_hands = {}
players_totals = {}
dealer_hand = {}
stand = {}
def dealer_draws_at_start():
    dealer_hand = (
        (random.choice(list(cards.keys()))),
        (random.choice(list(cards.keys())))
    )
    
    cards[dealer_hand[1]] -= 1
    cards[dealer_hand[0]] -= 1

    print(f"Dealer hand: {dealer_hand[0], 'hidden'}")
    print(f"Remaining cards: {cards}")
    return dealer_hand



def deal_cards_at_start():
    while True:
        try:
            players = int(input("Enter number of players (1-10): "))
            if 1 <= players <= 10:
                break
            else:
                print("Please enter a valid number of players between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            return players
    
    for i in range(players):
        player_hands[i] = (
            random.choice(list(cards.keys())),
            random.choice(list(cards.keys()))
        )

        cards[player_hands[i][1]] -= 1
        cards[player_hands[i][0]] -= 1

        print(f"Player {i+1} hand: {player_hands[i]}")
        print(f"Remaining cards: {cards}")
    
    dealer_draws_at_start()
    return players


def turn(players, player):
    bust = False
    print(f"Player {player+1}'s turn.")
    print(f"Current hand: {player_hands[player]}")
    while True:
        action = input("Do you want to 'hit' or 'stand'? ").strip().lower()
        if action == 'hit':
            while True:
                new_card = random.choice(list(cards.keys()))
                if cards[new_card] <= 0:
                    continue
                player_hands[player] += (new_card,)
                cards[new_card] -= 1
                print(f"New card: {new_card}")
                print(f"Updated hand: {player_hands[player]}")
                #we need to check if the player busts here
                
                total = 0
                for card in player_hands[player]:
                    if card == "king" or card == "queen" or card == "jack":
                        total += 10

                    elif card == "ace":
                        if total + 11 > 21:
                            total += 1
                        else:
                            total += 11
                    else:
                        total += int(card)
                print(f"Player {player+1} total: {total}")
                if total > 21:
                    print(f"Player {player+1} busts!")
                    #delete player from game
                    del(player_hands[player])
                    players-=1
                    print(f"Number of players remaining: {players}")
                    bust = True
                else:
                    players_totals[player] = total


                print(f"Remaining cards: {cards}")
                break

        if bust:
            break
        if action == 'stand':
            print(f"Player {player+1} stands with hand: {player_hands[player]}") 
            stand[player] = True
            break
        
        print("Invalid action. Please enter 'hit' or 'stand'.")
    return players, stand
        



def players_turns(players):
    for player in range(players):
        if stand.get(player):
            continue
        players = turn(players, player)[0]
    return players


def dealer_total():
        total = 0
        for card in dealer_hand:
            if card == "king" or card == "queen" or card == "jack":
                total += 10
            elif card == "ace":
                if total + 11 > 17 and total + 11 < 21:
                    total += 11
                else:
                    total += 1
            else:
                total += card
        print(f"Dealer total: {total}")
        return total

def dealers_turn(dealer_hand):
    print("Dealer's turn.")
    while dealer_total() < 17:
         new_card = random.choice(list(cards.keys()))
         if cards[new_card] <= 0:
             continue
         dealer_hand[new_card] = ""
         cards[new_card] -= 1
         print(f"Dealer draws: {new_card}")
         print(f"Dealer's hand: {dealer_hand}")
    if dealer_total() > 21:
        print("Dealer busts! Players win!")
    else:
        print(f"Dealer stands with total: {dealer_total()}")
    return dealer_total


def compare(dealer_total):
    for player in players_totals:
        if players_totals[player] > dealer_total:
            print(f"Player {player+1} wins!")
        else:
            print(f"Player {player+1} loses!")
      



# start the game
players = deal_cards_at_start()

while True:
    print(f"Number of players remaining: {players}")
    if players > 0 and len(stand) < players:
        print("Starting players' turns.")
        players = players_turns(players)
    elif players > 0 and len(stand) == players:
        for player in stand:
            if stand[player]:
                print(f"Player {player+1} has chosen to stand.")
        break
    else:
        print("All players have busted. Game over.")
        break

if players > 0:
    total = dealers_turn(dealer_hand)
    compare(total)


    