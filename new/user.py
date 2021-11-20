class User:
    def __init__(self, name):
        self.name = name
        self.hash = None  # wartość przypisujemy dopiero potem
        self.wallet = dict()
        self.cm = None  # przypisujemy dopiero w konstruktorze cm

    def checkout(self):
        sum = 0
        for coin_id, value in self.wallet.items():
            sum += value
        return sum

    def validate_blockchain(self):
        return self.hash == self.cm.header_hash

    def __str__(self):
        return self.name