from web3 import Web3
from web3.middleware import geth_poa_middleware
import secret_sharing


def sendInitialEther(send_to_address):
	web3 = Web3(Web3.HTTPProvider("http://98.221.129.176:8545/"))
	web3.middleware_onion.inject(geth_poa_middleware, layer=0)
	account_1 = '0x321e341Ad86ccB8D8d7d8042D008dFa55E7B43eD'
	# private_key1 = 'ce6af70496a9f4fef5de7ee4f6d3db502fd34e41c2447b0acb0b869f3084143a'

	# read the private key from a file and split it into shares
	secret_sharing.split_private_key("privateKey.txt")
	# reconstruct the private key
	private_key1 = secret_sharing.reconstruct_private_key("shares.txt")


	# TO-DO: split the key and send emails
	account_2 = Web3.toChecksumAddress('0x' + send_to_address)
	#print(Web3.toChecksumAddress("0xae3ecdf8f767d5ee06fe98cfc854cc5b3179a184".upper()))

	#get the nonce.  Prevents one from sending the transaction twice
	nonce = web3.eth.getTransactionCount(account_1)

	#build a transaction in a dictionary
	tx = {
		'chainId': 2267,
	    'nonce': nonce,
	    'to': account_2,
	    'value': web3.toWei(100, 'ether'),
	    'gas': 200000,
	    'gasPrice': web3.toWei('50', 'gwei')
	}
	# TO-DO: select k participants and send them link to provide their secret shares for authentication
	#sign the transaction
	signed_tx = web3.eth.account.sign_transaction(tx, private_key1)

	#send transaction
	tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

	#get transaction hash
	print(web3.toHex(tx_hash))
	#########

