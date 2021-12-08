import json

from block import Block
from chain_manager import ChainManager
from user import User
from Crypto.PublicKey import RSA
from Crypto import Signature
from Crypto import Hash
import base64

def load_json(filename: str) -> dict:
    input_file = open(filename)
    data = json.load(input_file)
    return data


def get_users(data: dict) -> dict:
    users = dict()
    for user in data['users']:
        users[user["name"]] = User(user["name"], user["public_key"], user["private_key"])
    return users


def get_coins(data: dict) -> dict:
    return data['coins']


def get_genesis(data: dict) -> dict:
    return data['genesis']


def verify(message: Hash, signature: bytes, public_key: RSA.RsaKey):
    signer = Signature.pkcs1_15.new(public_key)
    signer.verify(message, signature)


def create_genesis_json(genesis: dict) -> list:
    result = list()
    for coin_id, block in genesis.items():
        result.append(f'Create {coin_id} to {block["user"]}')
    return result # to musi być json??


def setup(genesis: dict, users: dict, cm: ChainManager):
    for coin_id, coin_user_assignment in genesis.items():
        if coin_user_assignment["user"] not in users:
            raise RuntimeError(f"Nieznany użytkownik {coin_user_assignment['user']}")
        assignment = f"coin_id: {coin_user_assignment['coin_id']}, user: {coin_user_assignment['user']}"
        if coin_user_assignment["cm_signature"] != base64.b64encode(cm.sign(assignment)).decode():
            raise RuntimeError("Zły podpis")
        users[coin_user_assignment['user']].wallet[coin_id] = coins[coin_id]


def get_transactions(data: dict) -> list:
    return data['transactions']


def get_cm_keys(data):
    return data["chain_manager"]["public_key"], data["chain_manager"]["private_key"]


if __name__ == "__main__":
    data = load_json("input.json")
    users = get_users(data)
    coins = get_coins(data)
    cm_public, cm_private = get_cm_keys(data)

    cm = ChainManager(cm_public, cm_private)
    genesis = get_genesis(data)
    transactions = get_transactions(data)

    if not len(coins) == len(genesis):
        raise RuntimeError("Nie zgadza się liczba wpisów z genesis z ilością coinów")

    if not coins.keys() == genesis.keys():
        raise RuntimeError("Brak zgodności pomiędzy tablicą coinów a przypisaniem do userów")

    setup(genesis, users, cm)
    genesis_json = create_genesis_json(genesis)
    genesis_block = Block(None, genesis_json)
    cm.setup(genesis_block, users, coins)

    print("POCZĄTKOWY STAN PORTFELI:")
    for name, user in users.items():
        print(f'{name}: {user.wallet}')
    print()

    for transaction in transactions:
        cm.make_transaction(transaction)

    # –––––––––––––––––––– PRZYKŁAD 1 ––––––––––––––––––––
    print("-> Przykład 1: POPRAWNY BLOCKCHAIN:")
    print(cm)
    print("Weryfikacja chain_manager: ", end='')
    print("blockchain poprawny") if cm.validate() else print("!!! ERROR !!!")
    print("Weryfikacja user: ", end='')
    print("blockchain poprawny") if users['Alec'].validate_blockchain() else print("!!! ERROR !!!")
    print()

    print("STAN PORTFELI PO TRANSAKCJACH:")
    for name, user in users.items():
        print(f'{name}: {user.wallet}')
    print()

    for name, user in users.items():
        print(f'{name} = {user.checkout()}$')

    print()

    # –––––––––––––––––––– PRZYKŁAD 2 ––––––––––––––––––––
    print("-> Przykład 2: NIEPOPRAWNY BLOCKCHAIN:")
    cm.blocks[0].data = "{'data': ['Create 1 to Alec', 'Create 2 to Magnus', 'Create 3 to Magnus', 'Create 4 to Alec', 'Create 5 to Magnus']}"

    print("ZMIENIONY I NIEPOPRAWNY BLOCKCHAIN:")
    print(cm)
    print("Weryfikacja chain_manager: ", end='')
    print("blockchain poprawny") if cm.validate() else print ("!!! ERROR !!!")
    print("Weryfikacja user: ", end='')
    print("blockchain poprawny") if users['Alec'].validate_blockchain() else print("!!! ERROR !!!")
    print()
    cm.blocks[0].data = "{'data': ['Create 1 to Alec', 'Create 2 to Magnus', 'Create 3 to Magnus', 'Create 4 to Magnus', 'Create 5 to Magnus']}"

    # –––––––––––––––––––– PRZYKŁAD 3 ––––––––––––––––––––
    print("-> Przykład 3: NIEPOPRAWNY BLOCKCHAIN ale wykrywa to user, a nie CM")
    # zmieniamy ostatni blok i header hash tak, że wg CM wszystko jest ok
    cm.blocks[2].data = "{'data': 'Magnus pays 4 to Alec'}"
    cm.header_hash = 'bbb29e13ae8bc4ffee316a5878c5b73739c8ce20b13200cd35b2a4eeba10dac9'
    print("ZMIENIONY BLOCKCHAIN ALE POPRAWNY:")
    print(cm)
    print("Weryfikacja chain_manager: ", end='')
    print("blockchain poprawny") if cm.validate() else print("!!! ERROR !!!")
    print("Weryfikacja user: ", end='')
    print("blockchain poprawny") if users['Alec'].validate_blockchain() else print ("!!! ERROR !!!")
    print()

    # –––––––––––––––––––– PRZYKŁAD 4 ––––––––––––––––––––
    print("-> Przykład 4: DOUBLE SPENDING, Magnus płaci coin_id którego nie ma")
    t = {
        "from": "Magnus",
        "to": "Alec",
        "coin_id": "5"
    }
    cm.make_transaction(t)
