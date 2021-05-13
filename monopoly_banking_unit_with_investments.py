# ---------------------------------------------------------------
# Monopoly Banking Unit | Eshan Uniyal
# June 2018, Python 3 | Updated February 2019
# A program that acts as a banking unit for a game of Monopoly
# ---------------------------------------------------------------

import random  # for asset valuation
from math import exp

# dictionary to hold all players (keys) and their class objects (values)
players = {}
all_history = []  # global lists to store histories

class Asset:
    """Asset class that accrues value over time"""

    def __init__(self, name, value, ror, p_up):
        self.name = name
        self.value = value  # starting value of asset
        self.ror = ror  # rate of return
        self.p_up = p_up  # probability of asset value going up

    def tick(self):
        """update value of asset stochastically"""
        old_value = self.get_value()
        # increase value
        if random.random() < self.p_up:
            self.value *= exp(self.ror)
        # decrease value
        else:
            self.value /= exp(self.ror)

        return f"{self.name}: ${old_value} => ${self.get_value()}"


    def get_value(self):
        return round(self.value, 2)

    def get_name(self):
        return self.name

    def get_ror(self):
        return self.ror

    def get_p_up(self):
        return self.p_up



assets = {
        "Crypto": Asset("Crypto", 61, 0.4, 0.60),
        "Mutual Funds": Asset("Mutual Funds", 897.67, 0.15, 0.80),
        "Bonds": Asset("Bonds", 247.7, 0.05, 0.95)
    }

# Current assets: 
# Arnold: 14, 1, 0 (total $1751.67)
# Vaibhav: 2, 6, 0 (total $5508.02)
# Sahen: 79, 0, 0 (total $4819.0)
# Kerilyn: 3, 0, 0 (total $183.0)
# Eshan: 8, 0, 1 (total $735.7)

tax = 0.05

def tick():
    for asset in assets.values():
        print((asset.tick()))

class Player:
    """Class to store all player variables"""

    def __init__(self, name):
        """initialises class object"""
        self.name = name.lower()
        self.history = []  # variable to store transaction history of each player
        # variable to store assets held
        self.assets = {asset_type : 0 for asset_type in assets.keys()}

        statement = f"Player {self.get_name()} created."

        all_history.append(statement)
        self.history.append(statement)
        print(statement + '\n')

    def get_name(self):
        return self.name.capitalize()

    def get_assets(self):
        return self.assets

    def invest(self, asset_type, quantity):
        self.assets[asset_type] += quantity
        statement = f"{self.get_name()} invested in {quantity} units of {asset_type} for ${quantity * assets[asset_type].get_value()}. "\
            f"{self.get_name()} now has {self.assets[asset_type]} units of {asset_type}."

        all_history.append(statement)
        self.history.append(statement)
        print(statement + '\n')

    def divest(self, asset_type, quantity):
        self.assets[asset_type] -= quantity
        statement = f"{self.get_name()} divested {quantity} units of {asset_type} for ${quantity * assets[asset_type].get_value() * (1 - tax)}. "\
            f"{self.get_name()} now has {self.assets[asset_type]} units of {asset_type}."

        all_history.append(statement)
        self.history.append(statement)
        print(statement + '\n')

    def transfer(self, payee, asset_type, quantity):
        """to transfer amount from self.account (payer account) to players[payee].account (payee account)"""
        self.assets[asset_type] -= quantity
        payee.assets[asset_type] += quantity
        statement = f"{quantity} units of {asset_type} transferred from {self.get_name()}'s account to {payee.get_name()}'s account. " \
            f"{self.get_name()} and {payee.get_name()} have {self.assets[asset_type]} and {payee.assets[asset_type]} units of {asset_type} respectively."

        self.history.append(statement)
        payee.history.append(statement)
        all_history.append(statement)

        print(statement)

    def list_assets(self):
        total = 0
        for key, val in assets.items():
            value = val.get_value() * self.assets[key]
            print(f"    {key}: ${val.get_value()} x {self.assets[key]} = ${value}")
            total += value
        print(f"    Total: {round(total, 2)}")


    def rename(self, new_name):
        """to rename player name"""
        statement = f"{self.get_name()} renamed to {new_name.lower().capitalize()}."
        self.name = new_name.lower()

        self.history.append(statement)
        all_history.append(statement)

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


def determine_quantity(prompt='Enter quantity: '):
    """function to use everywhere the program needs to prompt and determine an amount"""
    while True:
        try:
            quantity = float(input(prompt))
            if not quantity.is_integer() or quantity < 0:
                raise ValueError
        except ValueError:
            print('Invalid input. Enter a nonnegative integer.')
            continue
        else:
            break
    return int(quantity)


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


def invest_divest(command):
    """function to calculate costs/profit and carry out investment or divestment """

        # determining player
    player = players[determine_player()]

    # printing according to command
    if command == 'invest':
        print(f"You may invest in any of the following property asset types: {', '.join(assets.keys())}")
    elif command == 'divest':
        print(f"You own and may divest from the following asset types: {', '.join(player.get_assets().keys())}")

    print(f"The current value and owned quantity of each asset type is:")
    player.list_assets()

    # determining asset type
    while True:
        asset_type = input('Select asset type: ').title()
        if asset_type not in assets.keys():
            print('Asset type not found.')
            continue
        else:
            break


    # investing in asset
    if command == 'invest':

        quantity = determine_quantity('How many units of this asset would you like to purchase? ')

        prompt = f"Are you sure you wish to invest {quantity * assets[asset_type].get_value()} for {quantity} units of {asset_type}? (Y/N) "
        if confirm_decision(prompt) == "y":
            player.invest(asset_type, quantity)


    elif command == 'divest':

        quantity = determine_quantity('How many units of this asset would you like to divest? ')
        if quantity <= player.get_assets()[asset_type]:
            prompt = f"Are you sure you wish to divest {quantity} of {asset_type} for {quantity * assets[asset_type].get_value() * (1 - tax)}? (Y/N) "
            if confirm_decision(prompt) == "y":
                player.divest(asset_type, quantity)
        else:
            print(f"{player.get_name()} cannot divest {quantity} units of {asset_type}; {player.get_name()} only has {player.get_assets()[asset_type]} units.")


def transfer():
    """function to transfer amount from payer to payee"""

    # determining payer
    payer = players[determine_player('Transfer from whose account? ')]

    # determining payee
    payee = players[determine_player('Transfer to whose account? ')]

    # determining asset type
    while True:
        asset_type = input('Select asset type: ').title()
        if asset_type not in assets.keys():
            print('Asset type not found.')
            continue
        else:
            break

    # determining amount and executing transaction
    quantity = determine_quantity()


    # testing amount
    if quantity > payer.get_assets()[asset_type]:
        print(f"{payer.get_name()} cannot transfer {quantity} units of {asset_type}; {payer.get_name()} only has {payer.get_assets()[asset_type]} units.")
    # transfers from payer's account to payee's account
    else:
        payer.transfer(payee, asset_type, quantity)


def list_assets():
    """function to list each players assets"""

    # listing accounts
    for player in players.values():
        print(f"{player.get_name()}:")
        player.list_assets()


def list_history():
    """function to list all history or player history"""
    options = ['all history', 'player history']

    # printing history types
    print(
        f"You may select any of the following game histories to display: {', '.join(options)}")

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


    # if player history or player investment history requested
    elif history_type == 'player history':
        player = determine_player()
        for line in players[player].history:
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


def main():
    """main function running the game"""

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

    command_menu = ['tick', 'invest', 'divest', 'transfer', 'list assets',
                    'list history', 'remove player', 'rename player', 'end game']

    print(f"Command options: ")
    print(*command_menu, sep=', ')

    print("Note: to list command options at any time, enter 'help'.")

    while True:  # game loop designed to run until game is ended
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
        if command == 'tick':
            tick()

        elif command in ('invest', 'divest'):
            invest_divest(command)

        elif command == 'transfer':
            transfer()

        elif command == 'list assets':
            list_assets()

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
                    check = input(
                        "Do you wish to calculate any player's net worth? (Y/N) ").lower()
                    if check.lower() not in ('y', 'n'):
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
                            check = input(
                                "Do you wish to calculate any other player's net worth? (Y/N) ").lower()
                            if check.lower() not in ('y', 'n'):
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
                    check = input(
                        'Do you wish to declare a winner? (Y/N) ').lower()
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

                # saving history to external txt file
                file = open(filepath, 'w+')
                for statement in all_history:
                    file.write(statement + '\n')

                print(f"Game history saved to {filepath}.")

                break  # ending main game loop


main()
