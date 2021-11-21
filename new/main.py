import json

from block import Block
from chain_manager import ChainManager
from user import User


def load_json(filename: str) -> dict:
    input_file = open(filename)
    data = json.load(input_file)
    return data


def get_users(data: dict) -> dict:
    users = dict()
    for name in data['users']:
        users[name] = User(name)
    return users


def get_coins(data: dict) -> dict:
    return data['coins']


def get_genesis(data: dict) -> dict:
    return data['genesis']


def create_genesis_json(genesis: dict) -> list:
    result = list()
    for coin_id, name in genesis.items():
        result.append(f'Create {coin_id} to {name}')
    return result # to musi być json??


def setup(genesis: dict, users: dict):
    for coin_id, name in genesis.items():
        if name not in users:
            raise RuntimeError(f"Nieznany użytkownik {name}")
        users[name].wallet[coin_id] = coins[coin_id]


def get_transactions(data: dict) -> list:
    return data['transactions']


if __name__ == "__main__":
    data = load_json("new/input.json")

    users = get_users(data)
    coins = get_coins(data)
    genesis = get_genesis(data)
    transactions = get_transactions(data)

    if not len(coins) == len(genesis):
        raise RuntimeError("Nie zgadza się liczba wpisów z genesis z ilością coinów")

    if not coins.keys() == genesis.keys():
        raise RuntimeError("Brak zgodności pomiędzy tablicą coinów a przypisaniem do userów")

    setup(genesis, users)
    genesis_json = create_genesis_json(genesis)
    genesis_block = Block(None, genesis_json)
    cm = ChainManager(genesis_block, users, coins)

    print("PORTFELE:")
    for name, user in users.items():
        print(f'{name}: {user.wallet}')
    print()

    for transaction in transactions:
        cm.make_transaction(transaction)

    print("POPRAWNY BLOCKCHAIN:")
    print(cm)
    print("Poprawny blockchain") if cm.validate() else print("!!! ERROR !!!")
    print()

    print("PORTFELE PO TRANSAKCJACH:")
    for name, user in users.items():
        print(f'{name}: {user.wallet}')
    print()

    # cm.blocks[0].data = "['Create 1 to Alec', 'Create 2 to Magnus', 'Create 3 to Magnus', 'Create 4 to Alec', 'Create 5 to Magnus']"
    #
    # print("ZMIENIONY I NIEPOPRAWNY BLOCKCHAIN:")
    # print(cm)
    # print("Poprawny blockchain") if cm.validate() else print ("!!! ERROR !!!")

    cm.blocks[2].data = "{'data': 'Magnus pays 4 to Alec'}"
    cm.header_hash = '43ba8ee3395cfde7e5ab4347a5998924e6c967f837fe63df05605733dd853f9c'
    print("ZMIENIONY BLOCKCHAIN ALE POPRAWNY:")
    print(cm)
    print("Poprawny blockchain") if cm.validate() else print ("!!! ERROR !!!")
    print('Chyba, że...')
    print("Poprawny blockchain wg usera") if users['Alec'].validate_blockchain() else print ("!!! ERROR WG USERA !!!")

    print("PORTFELE PO TRANSAKCJACH:")
    for name, user in users.items():
        print(f'{name}: {user.wallet}')
    print()

    for name, user in users.items():
        print(f'{name} = {user.checkout()}$')