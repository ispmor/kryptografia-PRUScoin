import json

from block import Block
from chain_manager import ChainManager
from user import User

max_nonce = 2 ** 64
difficulty = 16


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
    return result  # to musi być json??


def setup(genesis: dict, users: dict):
    for coin_id, name in genesis.items():
        if name not in users:
            raise RuntimeError(f"Nieznany użytkownik {name}")
        users[name].wallet[coin_id] = coins[coin_id]


def get_transactions(data: dict) -> list:
    return data['transactions']


def assign_other_public_keys(users: dict):
    for name1, user1 in users.items():
        for name2, user2 in users.items():
            if user1 is not user2:
                user1.other_public_keys[name2] = user2.public_key


if __name__ == "__main__":
    data = load_json("input.json")

    # ––– 1. CREATE IDENTITY –––
    users = get_users(data)
    assign_other_public_keys(users)

    coins = get_coins(data)
    genesis = get_genesis(data)
    transactions = get_transactions(data)

    if not len(coins) == len(genesis):
        raise RuntimeError("Nie zgadza się liczba wpisów z genesis z ilością coinów")

    if not coins.keys() == genesis.keys():
        raise RuntimeError("Brak zgodności pomiędzy tablicą coinów a przypisaniem do userów")

    # ––– 2. CREATE BLOCKCHAIN –––
    setup(genesis, users)  # przypisz userom coiny
    genesis_json = create_genesis_json(genesis)
    cm = ChainManager(users, coins)
    genesis_block = Block(None, genesis_json, cm._private_key, None)
    cm.setup(genesis_block)

    print("POCZĄTKOWY STAN PORTFELI:")
    for name, user in users.items():
        print(f'{name}: {user.wallet}')
    print()

    # ––– 3. PRZYKŁADY TRANSAKCJI –––
    for transaction in transactions:
        cm.broadcast_to_pending_transactions(transaction)
        cm.make_turn(difficulty, max_nonce)

    print("STAN PORTFELI PO TRANSAKCJACH:")
    for name, user in users.items():
        print(f'{name}: {user.wallet}')
    print()

    print('SUMA:')
    for name, user in users.items():
        print(f'{name} = {user.checkout()}$')
    print()

    # ––– 4. WALIDACJA GENESIS –––
    print('SPRAWDZENIE PODPISU GENESIS (Alec):', users['Alec'].validate_genesis_signature())
    print()

    # ––– 5. WALIDACJA TRANSAKCJI –––
    print('SPRAWDZENIE WSZYSTKICH PODPISÓW (CM):', cm.validate_signatures())
    print()

    # ––– 6. WALIDACJA Z HASHAMI –––
    print("PRZYKŁADOWY BLOCKCHAIN I WALIDACJA Z HASHAMI: ")
    print(cm)
    print("Weryfikacja chain_manager: ", end='')
    print("OK") if cm.validate() else print("!!! ERROR !!!")
    print("Weryfikacja user: ", end='')
    print("OK") if users['Alec'].validate_blockchain() else print("!!! ERROR !!!")
    print()
