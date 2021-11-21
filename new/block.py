import json


class Block:
    def __init__(self, prev_hash, data):
        self.prev_hash = prev_hash
        self.set_data(data)

    def __str__(self):
        return f"BLOCK:\t\t{self.prev_hash} -> {self.data}"

    def set_data(self, data):
        self.data = "{'data': " + str(data) + "}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, separators=(',', ':'))

    def from_dict(self, loaded_dict):
        self.prev_hash = loaded_dict["prev_hash"]
        self.data = loaded_dict["data"]
        return self