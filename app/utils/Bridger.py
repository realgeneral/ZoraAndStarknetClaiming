import asyncio
import random
import re

import httpx
import web3.exceptions as ex3

from web3 import Web3
from web3.types import Wei

from app.logs import logging as logger
from app.utils.configs.config import rpcs, contracts


class Bridger:
    def __init__(self, pk):
        self.pk = pk

    async def eth_zora_bridge(self, bridge_amount):
        try:
            web3 = Web3(Web3.HTTPProvider(rpcs["eth"]))
            logger.info(f"Successfully connected to {rpcs['eth']}")
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)

            logger.info(f"Wallet address: {wallet_address}")
            logger.info(f"Balance in ETH network: {web3.from_wei(wallet_balance, 'ether')}")

            contract = web3.eth.contract(address=Web3.to_checksum_address(contracts["ZoraBridge"]["address"]),
                                         abi=contracts["ZoraBridge"]["abi"])

            bridge_tx = contract.functions.depositTransaction(
                wallet_address,
                web3.to_wei(bridge_amount, "ether"),
                100000,
                False,
                b''
            ).build_transaction({
                'from': wallet_address,
                'value': web3.to_wei(bridge_amount, "ether"),
                'gas': round(
                    contract.functions.depositTransaction(wallet_address, web3.to_wei(bridge_amount, "ether"), 100000,
                                                          False,
                                                          b'').estimate_gas(
                        {'from': wallet_address, 'value': web3.to_wei(bridge_amount, "ether"),
                         'nonce': web3.eth.get_transaction_count(wallet_address)}) * 1.15),
                'nonce': web3.eth.get_transaction_count(wallet_address)
            }
            )

            signed_bridge_tx = web3.eth.account.sign_transaction(bridge_tx, self.pk)
            raw_bridge_tx_hash = web3.eth.send_raw_transaction(signed_bridge_tx.rawTransaction)
            bridge_tx_hash = web3.to_hex(raw_bridge_tx_hash)

            logger.info(f"Bridge tx hash: {bridge_tx_hash}")

            for i in range(5):
                await asyncio.sleep(5)
                try:
                    bridge_tx_receipt = web3.eth.wait_for_transaction_receipt(raw_bridge_tx_hash, timeout=300)

                    if bridge_tx_receipt.status == 1:
                        logger.info(f"Successfully bridged: {bridge_amount} wei to Zora")
                        logger.info(f"Transaction: https://etherscan.io/tx/{bridge_tx_hash}")
                        return "✅"
                    else:
                        logger.error("Something went wrong while bridging")
                except ex3.TransactionNotFound as err:
                    logger.error(f"Something went wrong while bridging: {err}")
                    continue
                except Exception as err:
                    logger.error(f"Something went wrong while bridging: {err}")

        except Exception as err:
            if "insufficient funds" and "have" in str(err):
                have = int(re.search(r'have (\d+)', err.args[0]['message']).group(1))
                want = int(re.search(r'want (\d+)', err.args[0]['message']).group(1))
                gas = int(re.search(r'gas (\d+)', err.args[0]['message']).group(1))
                logger.error(f"Insufficient funds for gas * price + value. Want: {want} Have: {have} Gas: {gas}")
                return "❌ Insufficient funds for gas"
            elif "insufficient funds" in str(err):
                logger.error(f"Insufficient funds for gas * price + value.")
                return "❌ Insufficient funds for gas"
            else:
                logger.error(f"Something went wrong: {err}")
                return "❌ Something went wrong"

    @staticmethod
    def get_current_gwei():
        web3 = Web3(Web3.HTTPProvider(rpcs["eth"]))
        try:
            gas_price = web3.eth.gas_price
            current_base_fee = round(gas_price / 10 ** 9)
            logger.info(f"Current base fee: {current_base_fee} gwei")
            return current_base_fee
        except Exception as err:
            logger.error("Error while fetching gas price:", err)
            return None

    @staticmethod
    def choose_random_amount(min_amount_for_bridge, max_amount_for_bridge) -> Wei:
        min_places = len(str(min_amount_for_bridge).split('.')[1])
        max_places = len(str(max_amount_for_bridge).split('.')[1])
        places = max(min_places, max_places)

        random_number = random.uniform(float(min_amount_for_bridge), float(max_amount_for_bridge))
        formatted_string = "{:." + str(places) + "f}"
        formatted_number = float(formatted_string.format(random_number))
        logger.info(f"Random amount: {formatted_number}")

        return formatted_number


    @staticmethod
    async def get_transactions(address):
        API_KEY = "J3C3KSIT2V7TVVQJ7AKF23G2DR3UANACBZ"
        try:
            url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"

            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

            await asyncio.sleep(2)
            return data.get('result', [])

        except httpx.RequestError as e:
            logger.error(f"Request error while getting list of txs: {e}")
            return []

    @staticmethod
    async def used_bridge(private_key):
        bridge_address = "0x1a0ad011913A150f69f6A19DF447A0CfD9551054"
        try:
            web3 = Web3(Web3.HTTPProvider(rpcs["eth"]))
            wallet_address = web3.eth.account.from_key(private_key).address

            transactions = await Bridger.get_transactions(wallet_address)
            for tx in transactions:
                if tx['to'].lower() == bridge_address.lower():
                    return True
            return False
        except Exception as err_:
            logger.info(f"Failed to get trx for bridge check: {err_}")
            return False
