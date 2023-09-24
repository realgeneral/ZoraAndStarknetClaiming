from web3 import Web3

from app.logs import logging as logger
from app.utils.configs.config import rpcs, contracts


class Estimate:
    def __init__(self, pk):
        self.pk = pk

    def estimate_bridge(self, bridge_amount):
        web3 = Web3(Web3.HTTPProvider(rpcs["eth"]))
        logger.info(f"Successfully connected to {rpcs['eth']}")

        try:
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)

            logger.info(f"Wallet address: {wallet_address}")
            logger.info(f"Balance in ETH network: {web3.from_wei(wallet_balance, 'ether')}")

            contract = web3.eth.contract(address=Web3.to_checksum_address(contracts["ZoraBridge"]["address"]),
                                         abi=contracts["ZoraBridge"]["abi"])

            gas_estimate = contract.functions.depositTransaction(wallet_address, Web3.to_wei(bridge_amount, 'ether'),
                                                                 100000,
                                                                 False, b'').estimate_gas()

            gas_price = web3.eth.gas_price * 1.15

            total_cost_eth = Web3.from_wei(gas_estimate * gas_price, 'ether')

            return total_cost_eth
        except Exception as err:
            logger.error(f"Error while bridge estimating price: {err}")
            return None

    def eth_required(self, bridge_amount):
        bridge_fee = self.estimate_bridge(bridge_amount=bridge_amount)
        if bridge_fee:
            return round(float(bridge_fee) + bridge_amount, 6)
        else:
            logger.error("Something went wrong while getting eth required value")
            return "-"

    def get_eth_balance(self):
        web3 = Web3(Web3.HTTPProvider(rpcs["eth"]))
        logger.info(f"Successfully connected to {rpcs['eth']}")
        try:
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)
            eth_balance = web3.from_wei(wallet_balance, 'ether')
            return round(eth_balance, 5)
        except Exception as err:
            logger.error(f"Error while getting balance: {err}")
            return "-"

    def get_zora_balance(self):
        web3 = Web3(Web3.HTTPProvider(rpcs["zora"]))
        logger.info(f"Successfully connected to {rpcs['zora']}")
        try:
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)
            eth_balance = web3.from_wei(wallet_balance, 'ether')
            return round(eth_balance, 5)
        except Exception as err:
            logger.error(f"Error while getting balance: {err}")
            return "-"

    def get_eth_address(self):
        try:
            web3 = Web3(Web3.HTTPProvider(rpcs["eth"]))
            logger.info(f"Successfully connected to {rpcs['eth']}")
            return web3.eth.account.from_key(self.pk).address
        except Exception as err:
            logger.error(f"Error while getting balance: {err}")
            return "-"

    @staticmethod
    def get_current_gas():
        try:
            web3 = Web3(Web3.HTTPProvider(rpcs["eth"]))
            logger.info(f"Successfully connected to {rpcs['eth']}")
            gas_price = web3.eth.gas_price
            return round(Web3.from_wei(gas_price, 'gwei'), 2)
        except Exception as err:
            logger.error(f"Error while getting gas: {err}")
            return "-"
