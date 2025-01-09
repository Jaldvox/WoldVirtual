"""
This script handles the creation and management of a simple blockchain.
"""

import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    """
    Blockchain class to manage the chain of blocks.
    """
    def __init__(self):
        """
        Initialize the blockchain with a genesis block.
        """
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the genesis block and add it to the chain.
        """
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.calculate_hash(0, "0", time.time(), "Genesis Block"))
        self.chain.append(genesis_block)

    def calculate_hash(self, index, previous_hash, timestamp, data):
        """
        Calculate the hash of a block based on its index, previous hash, timestamp, and data.
        """
        value = str(index) + previous_hash + str(timestamp) + data
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def get_latest_block(self):
        """
        Get the latest block in the blockchain.
        """
        return self.chain[-1]

    def add_block(self, data):
        """
        Add a new block to the blockchain with the given data.
        """
        latest_block = self.get_latest_block()
        new_index = latest_block.index + 1
        new_timestamp = time.time()
        new_hash = self.calculate_hash(new_index, latest_block.hash, new_timestamp, data)
        new_block = Block(new_index, latest_block.hash, new_timestamp, data, new_hash)
        self.chain.append(new_block)

    def print_chain(self):
        """
        Print the entire blockchain.
        """
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print("-" * 30)
