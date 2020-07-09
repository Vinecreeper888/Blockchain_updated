#Import libraries
#time stamp, hash fucntion
import datetime
import hashlib


#simple class declaring a block
class Block:
	blockNo = 0
	data = None
	next = None
	hash = None
	nonce = 0
	prev_hash = 0x0
	timestamp = datetime.datetime.now() #fetches current time


	def __init__(self,data):
		self.data = data

	#define a hash function (SHA 256)
	def hash(self):
		h = hashlib.sha256() #getting sha256 method
		h.update(str(self.nonce).encode('utf-8')+str(self.data).encode('utf-8')+str(self.prev_hash).encode('utf-8')+str(self.timestamp).encode('utf-8')+str(self.blockNo).encode('utf-8'))
		return h.hexdigest() #returns hexadecimal output


	def __str__(self):
		return("Block Hash: "+str(self.hash())+"\n Block No: "+str(self.blockNo)+"\n Block  Data: "+str(self.data)+"\n Nonce: "+str(self.nonce)+"\n ----------------")


class BlockChain:
	diff = 20
	maxNonce = 2**32
	target = 2**(256-diff)


	block = Block("Genesis")
	dummy = head = block

	def add(self,block):
		block.prev_hash = self.block.hash()
		block.blockNo = self.block.blockNo+1

		#adding a block to the blockchain
		self.block.next = block
		self.block = self.block.next

	def mine(self,block):
		for n in range(self.maxNonce):
			if(int(block.hash(),16) <= self.target):
				self.add(block)
				#print(block)
				break
			else:
				block.nonce += 1


blockchain = BlockChain()


#print the blocks
for i in range(10):
	blockchain.mine(Block("Block"+str(i+1)))

while(blockchain.head != None):
	print(blockchain.head)
	blockchain.head = blockchain.head.next

#Output: Displays 10 blocks










