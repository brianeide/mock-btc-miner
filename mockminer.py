import hashlib
from binascii import unhexlify
from binascii import hexlify
import time


def little_endian(string: str):
    chars = list(string[::-1])
    for i in range(0, len(chars), 2):
        char_ahead = chars[i + 1]
        chars[i + 1] = chars[i]
        chars[i] = char_ahead
    return ''.join(chars)


class Block:
    def __init__(self, prev_hash: str, n_bits: str, version: str, timestamp: int, merkle_root: str):
        self.prev_hash = prev_hash
        self.n_bits = n_bits  # bits hex as str, no 0x
        self.version = version  # version as hex str, no 0x
        self.transactions = list()
        self.merkle_root = merkle_root
        self.time = timestamp
        self.nonce = 0

    def serialize_header(self):
        return ''.join([little_endian(self.version),
                        little_endian(self.prev_hash),
                        little_endian(self.merkle_root),
                        little_endian(str(hex(self.time))[2:]),
                        little_endian(self.n_bits),
                        little_endian('{:08x}'.format(self.nonce))])

    def calculate_hash(self):
        hashed = hashlib.sha256(hashlib.sha256(unhexlify(self.serialize_header())).digest()).digest()
        return hexlify(hashed[::-1]).decode('utf-8')

    def valid_hash(self, hash_attempt: str):
        target = "0x" + self.n_bits
        exponent = target[:4]
        significand = target[4:]
        significand_bytes = int(len(significand) / 2)
        target_value = int("0x" + significand, 16) * (256 ** (int(exponent, 16) - significand_bytes))
        return int("0x" + hash_attempt, 16) < target_value


def mine(block):
    last_update = 0
    last_nonce = 0
    hash_found = None
    while hash_found is None:
        calculated = block.calculate_hash()
        if block.valid_hash(calculated):
            hash_found = calculated
            break
        else:
            block.nonce += 1
            if time.time() - last_update > 30:
                if last_update > 0:
                    hps = (block.nonce - last_nonce) / (time.time() - last_update)
                    print("Hash rate:", hps, "H/s;", "Nonce:", block.nonce)
                last_update = time.time()
                last_nonce = block.nonce
    return hash_found


def fancy_print(lines: list):
    longest = sorted(list(map(len, lines)))[-1]
    for line in lines:
        if line == "*":
            print("*" * longest)
        else:
            pad = (longest - len(line)) // 2
            print(" " * pad, line, sep='')


def main():
    fancy_print(["*", "Mock Bitcoin Miner",
                 "Use https://chainquery.com/bitcoin-cli/getblock to get values in proper format.", "*"])
    version = input("Version (Hex): ")
    assert len(version) == 8, "Improper hex format in version"
    prevhash = input("Previous block's hash: ")
    assert len(prevhash) == 64, "Improper hash format in previous hash"
    merkle_root = input("Merkle Root: ")
    assert len(merkle_root) == 64, "Improper hash format in merkle root"
    timestamp = input("Time (Decimal integer): ")
    assert timestamp.isdigit(), "Improper decimal timestamp format"
    timestamp = int(timestamp)
    bits = input("Bits (Hex): ")
    assert len(bits) == 8, "Improper hex format in bits"
    block = Block(prevhash, bits, version, timestamp, merkle_root)
    input("Press enter to start mining.")
    start = time.time()
    block_hash = mine(block)
    print("Hash found:", block_hash)
    print("Winning nonce:", block.nonce)
    elapsed = time.time() - start
    print("Time elapsed:", round(elapsed, 3), "seconds")


if __name__ == '__main__':
    main()
