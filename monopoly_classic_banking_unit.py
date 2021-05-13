# ---------------------------------------------------------------
# Monopoly Classic Banking Unit | Eshan Uniyal
# February 2019, Python 3
# A program that acts as a banking unit for a game of Monopoly Classic
# ---------------------------------------------------------------

import datetime # importing module to save game history to external file

players = {}

# dictionary to hold all property sets
property_dict = {'brown' : ['Mediterranean Avenue', 'Baltic Avenue'],
                 'light blue' : ['Oriental Avenue', 'Vermont Avenue', 'Connecticut Avenue'],
                 'pink' : ['St. Charles Place', 'States Avenue', 'Virginia Avenue'],
                 'orange' : ['St. James Place', 'Tennessee Avenue', 'New York Avenue'],
                 'red' : ['Kentucky Avenue', 'Indiana Avenue', 'Illinois Avenue'],
                 'yellow' : ['Atlantic Avenue', 'Ventnor Avenue', 'Marvin Gardens'],
                 'green' : ['Pacific Avenue', 'North Carolina Avenue', 'Pennsylvania Avenue'],
                 'blue' : ['Park Place', 'Boardwalk'],
                 'railroads' : ['Reading Railroad', 'Pennsylvania Railroad', 'B. & O. Railroad', 'Short Line Railroad'],
                 'utilities' : ['Electric Company', 'Water Works']}

# list to hold all property set colours
property_sets = tuple([x for x in property_dict.keys()]) # all property sets
# list to hold all available property sets
avail_sets = list(property_sets)

# list to hold all properties
properties = tuple([p for p_set in property_sets for p in property_dict[p_set]])
# list to hold all available properties
avail_properties = list(properties)


# mapping property prices to properties
prop_prices = [60, 60, 100, 100, 120, 140, 140, 160, 180, 180, 200, 220, 220, 240, 260, 260, 280, 300, 300, 320, 350, 400, 200, 200, 200, 200, 150, 150]
prices_dict = {} # dictionary to hold all properties mapped with their prices
for i in range(0, len(properties)):
    prices_dict[properties[i]] = prop_prices[i]

all_history, all_investment_history = [], [] # global lists to store histories

class Player:
    """Class to store all player variables"""

    def __init__(self, name):
        """initialises class object"""
        self.name = name.lower()
        self.account = 1500
        self.history = [] # variable to store transaction history of each player
        self.investment_history = []  # variable to store investment history of each player
        self.prop_sets = {} # variable to store property sets (and buildings developed on each)
        self.properties = []

        statement = f"Player {self.name.capitalize()} created."

        all_history.append(statement)
        self.history.append(statement)
        print(statement + '\n')

    def add_amount(self, amount):
        """to add amount to self.account"""
        self.account += amount
        statement = f"{amount} added to {self.name.capitalize()}'s account. " \
            f"It now has {self.account}."

        self.history.append(statement)
        all_history.append(statement)

        print(statement)

    def subtract_amount(self, amount):
        """to subtract amount from self.account"""
        self.account -= amount
        statement = f"{amount} subtracted from {self.name.capitalize()}'s account. " \
            f"It now has {self.account}."

        self.history.append(statement)
        all_history.append(statement)

        print(statement)

    def transfer_amount(self, amount, payee):
        """to transfer amount from self.account (payer account) to players[payee].account (payee account"""
        self.account -= amount
        players[payee].account += amount
        statement = f"{amount} transferred from {self.name.capitalize()}'s account to {payee.capitalize()}'s account. " \
            f"{self.name.capitalize()} and {payee.capitalize()} have {self.account} and {players[payee].account} respectively."

        self.history.append(statement)
        players[payee].history.append(statement)
        all_history.append(statement)

        print(statement)

    def rename(self, new_name):
        """to rename player name"""
        statement = f"{self.name.capitalize()} renamed to {new_name.lower().capitalize()}."
        self.name = new_name.lower()

        self.history.append(statement)
        all_history.append(statement)

        print(statement)

    def add_pass_go(self):
        """to add money when player passes go"""
        self.account += 200 # to adjust for different versions of Monopoly
        statement = f"{self.name.capitalize()} passed go. " \
            f"{self.name.capitalize()} now has {self.account}."

        self.history.append(statement)
        all_history.append(statement)

        print(statement)

    def buy_prop(self, prop, cost):
        # to buy a given property
        self.account -= cost
        statement = f"{self.name.capitalize()} bought {prop} for {cost}. " \
            f"{self.name.capitalize()} now has {self.account} in their account."

        self.properties.append(prop)
        avail_properties.remove(prop)

        self.history.append(statement)
        all_history.append(statement)
        self.investment_history.append(statement)
        all_investment_history.append(statement)

        print(statement)


    def invest_prop(self, prop_set, n_buildings, cost):
        """to invest in properties"""
        self.account -= cost # cost computed by invest_divest function

        # updating number of buildings
        if prop_set in self.prop_sets:
            self.prop_sets[prop_set] += n_buildings
        else:
            self.prop_sets[prop_set] = n_buildings


        statement = f"{self.name.capitalize()} invested {cost} to develop {n_buildings} buildings " \
            f"in the {prop_set.lower()} set. {self.name.capitalize()} now has {self.account} in their account " \
            f"and {self.prop_sets[prop_set]} buildings on the {prop_set} property set."

        self.history.append(statement)
        all_history.append(statement)
        self.investment_history.append(statement)
        all_investment_history.append(statement)

        print(statement)

    def divest_prop(self, prop_set, n_buildings, profit):
        """to divest in properties"""
        self.account += profit # profit computed by invest_divest function
        self.prop_sets[prop_set] -= n_buildings # removing buildings from prop_sets

        statement = f"{self.name.capitalize()} profited {profit} from removing {n_buildings} buildings " \
            f"in the {prop_set.lower()} set. {self.name.capitalize()} now has {self.account} in their account " \
            f"and {self.prop_sets[prop_set]} buildings on the {prop_set} property set.."

        self.history.append(statement)
        all_history.append(statement)
        self.investment_history.append((statement))
        all_investment_history.append(statement)

        print(statement)


"""General functions"""

def determine_player(prompt='Enter player name: '):
    """function to use everywhere the program needs to prompt and determine a player"""
    while True:
        player = input(prompt).lower()
        if player not in players:
            print('Player not found.')
            continue
        else:
            break
    return player


def determine_amount(prompt='Enter amount: '):
    """function to use everywhere the program needs to prompt and determine an amount"""
    while True:
        try:
            amount = int(input(prompt))
        except ValueError:
            print('Invalid input. Enter a number.')
            continue
        else:
            break
    return amount


def confirm_decision(prompt):
    """function to confirm player decision"""

    while True:

        decision = input(prompt).lower()

        if decision not in ('y', 'n'):
            print('Invalid input.')
            continue

        else:
            return decision

"""Command menu functions"""

def add():
    """function to take player and amount input and add accordingly"""

    # determining player
    prompt = 'Add to whose account? '
    player = determine_player(prompt)

    # determining amount
    amount = determine_amount()

    # adding amount
    players[player].add_amount(amount)  # adds amount to player's account


def subtract():
    """function to take player and account input and subtract accordingly"""

    # determining player
    prompt = 'Subtract from whose account? '
    player = determine_player(prompt)

    # determining amount
    amount = determine_amount()

    # testing amount
    if amount > players[player].account:
        print(f'Insufficient funds. {player.capitalize()} currently has {players[player].account}.')
    # adds amount to player's account
    else:
        players[player].subtract_amount(amount)


def transfer():
    """function to transfer amount from payer to payee"""

    # determining payer
    prompt = 'Subtract from whose account? '
    payer = determine_player(prompt)

    # determining payee
    prompt = 'Add to whose account? '
    payee = determine_player(prompt)

    # determining amount and executing transaction
    amount = determine_amount()

    # testing amount
    if amount > players[payer].account:
        print(f"Insufficient funds in {payer.capitalize()}'s account. "
              f"{payer.capitalize()} currently has {players[payer].account}.")
    # transfers from payer's account to payee's account
    else:
        players[payer].transfer_amount(amount, payee)


def pass_go():
    """function to add money when player passes go"""

    # determining player
    player = determine_player()

    # adding pass go amount
    players[player].add_pass_go()


def buy():
    """function to buy a property"""

    # determining player
    player = determine_player()

    # determining property
    while True:
        prop = input('Which property would you like to buy? ').title()
        if prop in properties:
            break
        else:
            print('Property not found.')

    if prop in avail_properties:

        cost = prices_dict[prop]
        if cost > players[player].account:
            print(f"Insufficient funds in {player.capitalize()}'s account."
                  f"{player.capitalize()} currently has {players[player].account}.")

        else:
            print(f"Purchasing {prop} would cost {prices_dict[prop]}. "
                  f"{player.capitalize()} currently has {players[player].account}.")
            # confirming decision
            prompt = f'Are you sure you wish to purchase {prop}? (Y/N) '
            decision = confirm_decision(prompt)

            if decision == 'y':
                players[player].buy_prop(prop, cost)
            else:
                print('Purchase cancelled.')

    else:
        print('Cannot purchase; property owned by another player.')

def invest_divest(command):
    """function to calculate costs/profit and carry out investment or divestment """

    # determining player
    player = determine_player()

    # printing according to command
    if command == 'invest':
        print(f"You may invest in any of the following property sets: {', '.join(property_sets)}")
    elif command == 'divest':
        print(f"You may divest from any of the following property sets: {', '.join(players[player].prop_sets)}")

    # determining property set
    while True:
        prop_set = input('Select property set: ').lower()
        if prop_set not in property_sets:
            print('Property set not found.')
            continue
        else:
            break

    # checking whether player can invest desired number of houses
    if command == 'invest':

        # determining existing number of houses
        if prop_set in players[player].prop_sets:
            existing_buildings = players[player].prop_sets[prop_set]
        else:
            existing_buildings = 0

        print(f"{player.capitalize()} currently has {existing_buildings} buildings on {prop_set}.")

        # determining number of houses
        prompt = 'How many buildings in total do you wish to develop? '
        n_buildings = determine_amount(prompt)

        # checking whether additional n_buildings can be developed
        if prop_set in ('brown', 'blue'):
            if n_buildings + existing_buildings > 10:
                print(f"Cannot develop {n_buildings} buildings; total buildings would exceed limit.")
                return
        else:
            if n_buildings + existing_buildings > 15:
                print(f"Cannot develop {n_buildings} buildings; total buildings would exceed limit.")
                return

    elif command == 'divest':

        # checking whether the player has the property set
        if prop_set not in players[player].prop_sets:
            print(f"Cannot divest; {player.capitalize()} currently has no buildings on {prop_set}.")
            return

        # if player does have buildings on prop_set
        else:
            # determining existing houses
            existing_buildings = players[player].prop_sets[prop_set]

            print(f"{player.capitalize()} currently has {existing_buildings} buildings on {prop_set}.")

            # determining number of desired buildings to divest
            prompt = 'How many buildings in total do you wish to divest? '
            n_buildings = determine_amount(prompt)

            if n_buildings > players[player].prop_sets[prop_set]:
                print(f"Player cannot divest {n_buildings} buildings; "
                      f"player only has {existing_buildings} buildings.")
                return

    # determining cost/profit
    multiplier = 100 # to calculate unit cost dependent on Monopoly version
    amount = 0 # to call of PyCharm's red flag about amount and n_buildings potentially not being defined

    if prop_set in ('brown', 'light blue'):
        amount = n_buildings * multiplier // 2 # costs 50 per house (or 500k) in first row
    elif prop_set in ('pink', 'orange'):
        amount = n_buildings * multiplier # costs 100 per house in second row
    elif prop_set in ('red', 'yellow'):
        amount = int(n_buildings * 1.5 * multiplier) # costs 150 per house in third row
    elif prop_set in ('green', 'dark blue'):
        amount = n_buildings * 2 * multiplier # costs 200 per house in fourth row

    # if player wishes to invest
    if command == 'invest':

        # testing cost
        if amount > players[player].account:
            print(f'Insufficient funds. \n'
                  f'Investing {n_buildings} buildings into the {prop_set} property set will cost {amount}; '
                  f'{player.capitalize()} currently has {players[player].account}.')
        # displaying cost
        else:
            print(f"Investing {n_buildings} buildings into the {prop_set} property set will cost {amount};"
                  f" {player.capitalize()} currently has {players[player].account}.")
            # confirming decision
            prompt = 'Are you sure you wish to invest? (Y/N) '
            decision = confirm_decision(prompt)
            # if decision confirmed, investing
            if decision == 'y':
                players[player].invest_prop(prop_set, n_buildings, amount)
            else:
                print('Investment called off.')

    # if player wishes to divest
    elif command == 'divest': # player wishes to divest

        amount = amount // 2 # if divesting, owner only gets half price

        # displaying profit
        print(f"By divesting {n_buildings} buildings from the {prop_set} property set, player will receive {amount}; "
                  f"{player.capitalize()} currently has {players[player].account}.")

        # confirming decision
        prompt = 'Are you sure you wish to divest? (Y/N) '
        decision = confirm_decision(prompt)

        # if decision confirmed, divesting
        if decision == 'y':
            players[player].divest_prop(prop_set, n_buildings, amount)
        else:
            print('Divestment called off.')


def split():
    """function to send a particular amount from player x to all other players"""

    # determining player
    player = determine_player()

    # determining whether player has to pay other players or collect from other players
    while True:
        type = input(f"Is {player.capitalize()} paying each other player or receiving from each player? "
                     f"(Enter 'pay' or 'receive') ").lower()
        if type not in ('pay', 'receive'):
            print("Invalid input. Enter 'pay' or 'receive'.")
            continue
        else:
            break

    # determining number of players to be paid to or collected from
    n_players = len(players) - 1

    # if player has to pay
    if type == 'pay':
        payer = player

        # determining amount
        prompt = f"Enter amount {payer.capitalize()} has to pay each player: "
        amount = determine_amount(prompt)

        # determining whether player has the total amount to pay
        if amount * n_players > players[payer].account:
            print(f"Insufficient funds in {payer.capitalize()}'s account. "
              f"{payer.capitalize()} currently has {players[payer].account}.")
        else:

            # transferring amount to other players
            for payee in players:
                if payee != payer:
                    players[payer].transfer_amount(amount, payee)

    elif type == 'receive':
        payee = player

        # determining amount
        amount = determine_amount(f"Enter amount {payee.capitalize()} has to receive from each player: ")

        # determining whether each player can pay
        condition = True # condition variable to represent whether each player can pay
        for payer in players:
            # if payer can't pay
            if amount > players[payer].account:
                print(f"Insufficient funds in {payer.capitalize()}'s account. "
                      f"{payer.capitalize()} currently has {players[payer].account}.")

                # updating pay ability condition
                condition = False

                break

        # if everyone is able to pay
        if condition:
            for payer in players:
                if payer != payee:
                    players[payer].transfer_amount(amount, player)


def trade():
    """function to organise trade of properties and money between two players"""

    # determining players
    player_1 = determine_player('Enter player 1 name: ')
    player_2 = determine_player('Enter player 2 name: ')

    while True:
        properties_1 = input('What properties is player 1 offering? Separate property names with a comma: ').split(', ')

        for prop in properties_1:

            if prop.title() not in properties:
                print(f"{prop.title()} is not a valid property name.")
                continue

            if prop.title() not in players[player_1].properties:
                print(f"{prop.title()} is not owned by {player_1.capitalize()}.")
                continue
        break

    while True:
        try:
            amount_1 = int(input("How much money is player 1 offering? If no money is involved, enter '0': "))
        except ValueError:
            print('Invalid input. Please enter a number.')
            continue

        if amount_1 > players[player_1].account:
            print(f"Insufficient funds in {player_1.capitalize()}'s account. "
                  f"{player_1.capitalize()} currently has {players[player_1].account}.")
        else:
            break

    while True:
        properties_2 = input('What properties is player 2 offering? Separate property names with a comma: ').split(', ')

        for prop in properties_2:

            if prop.title() not in properties:
                print(f"{prop.title()} is not a valid property name.")
                continue

            if prop.title() not in players[player_2].properties:
                print(f"{prop.title()} is not owned by {player_2.capitalize()}.")
                continue
        break

    while True:
        try:
            amount_2 = int(input("How much money is player 2 offering? If no money is involved, enter '0': "))
        except ValueError:
            print('Invalid input. Please enter a number.')
            continue

        if amount_2 > players[player_2].account:
            print(f"Insufficient funds in {player_2.capitalize()}'s account. "
                  f"{player_2.capitalize()} currently has {players[player_2].account}.")
        else:
            break

    players[player_1].transfer_amount(amount_1, player_2)
    players[player_2].transfer_amount(amount_2, player_1)








def list_accounts():
    """function to list each players account"""

    # listing accounts
    for player, player_class in players.items():
        print(f"{player.capitalize()}: {player_class.account}")


def list_player_props():
    """function to list player's properties"""

    player = determine_player("Which player's properties do you want to list? ")

    if len(players[player].properties) == 0:
        print(f"{player.capitalize()} has no properties.")
    else:
        print(f"{player.capitalize()} has the following properties: ")
        print(*players[player].properties, sep=', ')

def list_history():
    """function to list all history, investment history, player history, or player investment history"""
    options = ['all history', 'investment history', 'player history', 'player investment history']

    # printing history types
    print(f"You may select any of the following game histories to display: {', '.join(options)}")

    # determining history type
    while True:
        history_type = input('Enter history type: ').lower()
        if history_type not in options:
            print('Invalid input.')
            continue
        else:
            break

    # if all history requested
    if history_type == 'all history':
        for line in all_history:
            print(line)

    # if all investment history requested
    elif history_type == 'investment history':
        for line in all_investment_history:
            print(line)

    # if player history or player investment history requested
    elif history_type in ('player history', 'player investment history'):

        # determining player
        player = determine_player()

        # if player history requested
        if history_type == 'player history':
            for line in players[player].history:
                print(line)

        # if player investment history requested
        elif history_type == 'player investment history':
            for line in players[player].investment_history:
                print(line)


def remove_player():
    """function to remove player by deleting his key from the players dictionary"""

    # determining player
    player = determine_player()

    # confirming decision
    prompt = f'Are you sure you wish to remove {player.capitalize()} from the game? (Y/N) '
    decision = confirm_decision(prompt)

    # removing player if decision confirmed
    if decision == 'y':
        del players[player]
        print(f"Player {player.capitalize()} has been removed from the game.")


def rename_player():
    """function to change the name of a player"""

    # to determine player name to be changed
    player = determine_player()

    # to determine new player name
    while True:
        new_name = input('Enter new player name: ').lower()
        if new_name in players:
            print(f'{new_name.capitalize()} is already in use.')
            continue
        else:
            break

    # confirming decision
    prompt = f"Are you sure you wish to change {player.capitalize()}'s name to {new_name.capitalize()}? (Y/N) "
    decision = confirm_decision(prompt)

    # executing change of name if decision is yes
    if decision == 'y':
        print(f"Player {player.capitalize()} has been removed from the game.")

        players[player].rename(new_name)
        players[new_name] = players[player]

        del players[player]


def end_game():
    """command to confirm end game and list final accounts"""
    # confirming end game command
    print("Note: After ending game, you will not be able to initiate any transactions, investments, or divestments, "
          "or remove or rename any players. \nHowever, if you so choose, you will be able to add or subtract amounts to "
          "remaining players' accounts to calculate their respective net worth.\n")

    prompt = 'Are you sure you wish to end the game? (Y/N) '
    decision = confirm_decision(prompt)

    # if end game confirmed
    if decision == 'y':
        print('Game ended.\n')

        # goes back to main() to break game loop
        return True

    # if end game cancelled
    return False


def net_worth():
    """function to help players calculate net worth"""

    # determining player
    player = determine_player()

    # determining whether player has any buildings whatsoever
    condition = False
    for prop_set, n_buildings in players[player].prop_sets.items():
        if n_buildings > 0:
            condition = True
            break

    # printing new command menu
    print()
    command_menu = ['add', 'subtract', 'end calculation']

    # printing current bank and assets
    # if player has any buildings, print account and assets
    if condition:

        print(f"{player.capitalize()} currently has {players[player].account} in their account and the following assets: ")

        for prop_set, n_buildings in players[player].prop_sets.items():
            if n_buildings > 0:
                print(f"{prop_set.capitalize()} property set: {n_buildings} buildings")

    # if player has no buildings, print account only
    else:
        print(f"{player.capitalize()} currently has {players[player].account} in their account.")

    # printing new command options
    print(f"\nCommand options: add, subtract, end calculation")

    while True:  # game loop designed to run until net worth is calculated
        print()

        # taking command input
        while True:
            command = input('Enter command: ').lower()
            if command not in command_menu:
                print('Invalid input.\n')
                continue
            else:
                break

        # testing commands
        if command == 'add':
            prompt = f"Add how much to {player.capitalize()}'s account? "
            amount = determine_amount(prompt)

            players[player].add_amount(amount)

        elif command == 'subtract':
            prompt = f"Subtract how much from {player.capitalize()}'s account? "
            amount = determine_amount()

            players[player].subtract_amount(amount)

        if command == 'end calculation':
            # printing net worth and saving to all history
            statement = f"{player.capitalize()} has a net worth of {players[player].account}."
            all_history.append(statement)
            break



def main():
    """main function running the game"""

    all_history.append("Game set up with 1500 in each player's account.")
    all_history.append('')
    print()

    # determining number of players
    while True:
        try:
            n_players = int(input("Please enter number of players: "))
        except ValueError:
            print('Invalid input. Enter a number.\n')
        else:
            statement = f'Game set up for {n_players} players.\n'
            all_history.append(statement)
            print(statement)
            break

    # populating player dictionary
    for i in range(1, n_players + 1):
        player_name = input(f'Please enter name of player {i}: ').lower()
        players[player_name] = Player(player_name)

    print('Game initiated.')

    # setting up game

    command_menu = ['add', 'subtract', 'transfer', 'pass go', 'buy', 'invest', 'divest', 'split', 'trade', 'list accounts', 'list player properties',
                    'list history', 'remove player', 'rename player', 'end game']

    print(f"Command options: ")
    print(*command_menu, sep=', ')

    print("Note: to list command options at any time, enter 'help'.")

    while True: # game loop designed to run until game is ended
        print()

        # taking command input
        while True:
            command = input('Enter command: ').lower()
            if command not in command_menu and command != 'help':
                print('Invalid input.\n')
                continue
            else:
                break

        # testing commands
        if command == 'add':
            add()

        elif command == 'subtract':
            subtract()

        elif command == 'transfer':
            transfer()

        elif command == 'pass go':
            pass_go()

        elif command == 'buy':
            buy()

        elif command in ('invest', 'divest'):
            invest_divest(command)

        elif command == 'split':
            split()

        elif command == 'trade':
            trade()

        elif command == 'list accounts':
            list_accounts()

        elif command == 'list player properties':
            list_player_props()

        elif command == 'list history':
            list_history()

        elif command == 'remove player':
            remove_player()

        elif command == 'rename player':
            rename_player()

        elif command == 'help':
            print(f"Command options: ")
            print(*command_menu, sep=', ')

        elif command == 'end game':

            # if player does indeed decide to end game
            if end_game():

                # checking whether user wants to calculate net worth
                while True:
                    check = input("Do you wish to calculate any player's net worth? (Y/N) ").lower()
                    if check not in ('y', 'n'):
                        print('Invalid input.\n')
                    else:
                        break

                # if user does want to calculate net worth
                if check == 'y':

                    while True:

                        # calculate net worth for player
                        net_worth()

                        # check if user wishes to calculate net worth for any other players
                        while True:
                            check = input("Do you wish to calculate any other player's net worth? (Y/N) ").lower()
                            if check not in ('y', 'n'):
                                print('Invalid input.\n')
                            else:
                                break

                        # if user wants to calculate net worth again
                        if check == 'y':
                            continue
                        else:
                            # breaks while loop for calculating net worth
                            break

                # printing final accounts
                print('Final accounts read as follows: ')
                list_accounts()
                print()

                # checking whether user wishes to declare a winner
                while True:
                    check = input('Do you wish to declare a winner? (Y/N) ').lower()
                    if check not in ('y', 'n'):
                        print('Invalid input.')
                    else:
                        break

                # declaring winner
                if check == 'y':

                    while True:
                        winner = input('Declare winner: ').lower()

                        if winner not in players:
                            print(f"{winner.capitalize()} not found.")

                        else:
                            # printing winner and saving to all_history
                            statement = f"{winner.capitalize()} has won the game.\n"
                            all_history.append(statement)
                            print(statement)
                            break

                break # ending main game loop


main()