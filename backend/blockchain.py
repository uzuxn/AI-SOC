import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(1, str(datetime.utcnow()), {"event": "genesis"}, 0)
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain) + 1,
            timestamp=str(datetime.utcnow()),
            data=data,
            previous_hash=previous_block.hash,
        )
        self.chain.append(new_block)

    def to_dict(self):
        return {
            "length": len(self.chain),
            "chain": [
                {
                    "index": block.index,
                    "timestamp": block.timestamp,
                    "data": block.data,
                    "hash": block.hash,
                    "previous_hash": block.previous_hash
                }
            for block in self.chain
            ]
        }

blockchain = Blockchain()