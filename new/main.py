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


def get_genesis_json_and_setup(genesis: dict) -> list: # TODO teraz to jest lista a nie json
    result = list()
    for coin_id, name in genesis.items():
        if name not in users:
            raise RuntimeError(f"Nieznany użytkownik {name}")
        users[name].wallet[coin_id] = coins[coin_id]
        result.append(f'Create {coin_id} to {name}')
    return result


if __name__ == "__main__":
    data = load_json("new/input.json")

    users = get_users(data)
    coins = data['coins']
    genesis = data['genesis']

    if not coins.keys() == genesis.keys():
        raise RuntimeError("Brak zgodności pomiędzy tablicą coinów a przypisaniem do userów")

    transactions = data['transactions']
    genesis_json = get_genesis_json_and_setup(genesis) # to będzie zapisane jako dane genesis
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

    cm.blocks[2].data = 'Alec pays 2 to Magnus'
    cm.header_hash = '763840e37f0c197364d0309ea894c322ec993b9031c0d9893eb72515528619bc'
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