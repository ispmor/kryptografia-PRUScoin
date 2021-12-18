import json
import rsa


class Block:
    def __init__(self, prev_hash, data, public_key):
        self.prev_hash = prev_hash
        self.signature = rsa.encrypt(str(data).encode(), public_key)
        self.set_data(data)

    def __str__(self):
        return f"BLOCK:\n\tpoprzedni hash: {self.prev_hash}\n\t-> {self.data}"

    def set_data(self, data):
        self.data = "{'data': " + str(data) + ", 'signature': " + str(self.signature) + "}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, separators=(',', ':'))

    def from_dict(self, loaded_dict):
        self.prev_hash = loaded_dict["prev_hash"]
        self.data = loaded_dict["data"]
        return self
