from unittest import TestCase

from main import get_users, get_coins, get_genesis, get_transactions, create_genesis_json

example_json = {
  "users": ["Alec", "Magnus"],
  "coins": {
    "1": 1,
    "2": 1,
    "3": 1,
    "4": 1,
    "5": 1
  },
  "genesis": {
    "1": "Alec",
    "2": "Magnus",
    "3": "Magnus",
    "4": "Magnus",
    "5": "Magnus"
  },
  "transactions": [
    {
      "from": "Magnus",
      "to": "Alec",
      "coin_id": "2"
    },
    {
      "from": "Magnus",
      "to": "Alec",
      "coin_id": "5"
    }
  ]
}

class TestMain(TestCase):
    def test_get_users(self):
        users = get_users(example_json)
        assert len(users) == 2

    def test_get_coins(self):
        coins = get_coins(example_json)
        assert len(coins) == 5
        assert coins["3"] == 1

    def test_get_genesis(self):
        genesis = get_genesis(example_json)
        coins = get_coins(example_json)
        users = get_users(example_json)
        assert len(coins) == len(genesis)
        assert coins.keys() == genesis.keys()
        for coin_id, user in genesis.items():
            assert user in users

    def test_get_transactions(self):
        transactions = get_transactions(example_json)
        assert len(transactions) == 2
        for transaction in transactions:
            assert len(transaction) == 3

    def test_create_genesis_json(self):
        genesis = get_genesis(example_json)
        json = create_genesis_json(genesis)
        assert json == ['Create 1 to Alec', 'Create 2 to Magnus', 'Create 3 to Magnus', 'Create 4 to Magnus', 'Create 5 to Magnus']