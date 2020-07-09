# import the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify


# create class for blockchain


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof=1, prev_hash='0')

    # define a function to create a block
    def create_block(self, proof, prev_hash):
        # create  a block with essential keys
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash}

        # lets append teh block to the chain
        self.chain.append(block)
        return block

    # lets fetch the previous block
    def get_prev_block(self):
        return self.chain[-1]

    # find the proof of work
    def proof_of_work(self, prev_proof):
        # initilise the variable for proof of work with 1
        new_proof = 1
        check_proof = False

        # Now lets iterate every check_proof until it is false
        while(check_proof is False):
            hash_operation = hashlib.sha256(
                str(new_proof**2 - prev_proof**2).encode()).hexdigest()

            # define a condition for miners to check the initial four digits of block are 0
            if(hash_operation[:4] == '0000'):
                check_proof = True
            else:
                new_proof += 1

        return(new_proof)

    # define a function to generate blocks
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return(hashlib.sha256(encoded_block).hexdigest())

    # define a function to check the validity
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        new_proof = 1
        block_index = 1

        while(block_index < len(chain)):
            block = chain[block_index]

            if(block['prev_hash'] != self.hash(prev_block)):
                return(False)

            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if(hash_operation[:4] == '0000'):
                return False

            prev_block = block
            block_index += 1
        return True


# mining the block
# create a web based app using Flask
app = Flask(__name__)

# create the instance of the blockchain
blockchain = Blockchain()

# use a route decorator
@app.route('/mineblock', methods=['GET', 'POST'])
# define a method to mine a block
def mineblock():
    prev_block = blockchain.get_prev_block()
    #prev_proof = prev_block['proof']
    prev_hash = blockchain.hash(prev_block)
    proof = blockchain.hash(prev_block)
    block = blockchain.create_block(proof, prev_hash)

    response = {'message': 'Congratulations! you have just mined a block',
                'index': block['index'], 'timestamp': block['timestamp'], 'proof': block['proof'], 'prev_hash': block['prev_hash']}

    return(jsonify(response), 200)


# Get the full block chain
# use a route decorator
@app.route('/getchain', methods=['GET', 'POST'])
def getchain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)
                }

    return(jsonify(response), 200)


# Running the flask app
app.run(host='0.0.0.0', port=5000)
