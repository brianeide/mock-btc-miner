# mock-btc-miner
A mock Bitcoin mining program to demonstrate proof of work as well as block header serialization and hashing

# Instructions
- Find a block you would like to mine.
  - I recommend finding a block with a low nonce value: https://blockchair.com/bitcoin/blocks?s=nonce(asc)#f=id,nonce
- Go to https://chainquery.com/bitcoin-cli/getblock.
- Paste the block hash. Make sure the verbosity is set to 1 (json block).
- Click execute command.
- Run `mockminer.py`
- Enter each value according to the JSON result in the getblock query.
- Press enter to begin mining. The program will print your current hash rate and current nonce every 30 seconds.
- Once the hash is found, the program will print the hash as well as the nonce used to calculate the hash. These two values will match up with the values found in the JSON result or any blockchain explorer such as Blockchair.

# Example
I used block #32620 because it has a low nonce that takes about a minute to find. I went to https://blockchair.com/bitcoin/block/32620 and copied the hash. I used the [getblock command](https://chainquery.com/bitcoin-cli/getblock) and executed it with verbosity 1 to get the following result:
```
{
    "result": {
        "hash": "00000000130f1bc659bdc4045694f84a6f058d309bce35ad916f12dec3ddc7f9",
        "confirmations": 671501,
        "strippedsize": 215,
        "size": 215,
        "weight": 860,
        "height": 32620,
        "version": 1,
        "versionHex": "00000001",
        "merkleroot": "ae88e563ea75214dbd85a1b781fa262203626449ab88175f5992d3a2ba890190",
        "tx": [
            "ae88e563ea75214dbd85a1b781fa262203626449ab88175f5992d3a2ba890190"
        ],
        "time": 1262388986,
        "mediantime": 1262387024,
        "nonce": 5460703,
        "bits": "1d00d86a",
        "difficulty": 1.182899534312841,
        "chainwork": "00000000000000000000000000000000000000000000000000007fb041d22c6a",
        "nTx": 1,
        "previousblockhash": "0000000013f2b8673ea86b0ae63d067d8e960e49d75a7e9ff197cb89074bef0e",
        "nextblockhash": "00000000126bcc16e5909b4a7ee56fed07762fc366c87212b6a4f2f16c1238a6"
    },
    "error": null,
    "id": null
}
```

I then ran the program and entered the values as follows:
```
Version (Hex): 00000001
Previous block's hash: 0000000013f2b8673ea86b0ae63d067d8e960e49d75a7e9ff197cb89074bef0e
Merkle Root: ae88e563ea75214dbd85a1b781fa262203626449ab88175f5992d3a2ba890190
Time (Decimal integer): 1262388986
Bits (Hex): 1d00d86a
```

I then started the mining process, and the hash was found in about 67 seconds:
```
Hash found: 00000000130f1bc659bdc4045694f84a6f058d309bce35ad916f12dec3ddc7f9
Winning nonce: 5460703
Elapsed time: 66.914 seconds
```
