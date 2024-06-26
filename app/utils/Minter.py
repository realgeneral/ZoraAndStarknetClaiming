import asyncio
import re
import random
import string
import time
import web3.exceptions as ex3

from web3 import Web3
from app.logs import logging as logger
from app.utils.configs.config import rpcs, nft_contract_abi, nft_ZoraCreator_contract_abi, ZoraNFTCreator_contract_abi, JSONExtensionRegistry_contract_abi, blocks_contract_abi, mint_contract_abi, yassin_contract_abi


class Minter:
    def __init__(self, pk):
        self.pk = pk
        self.collectionAddress = ""

    async def mint(self, nft_address, nft_id: int):

        web3 = Web3(Web3.HTTPProvider(rpcs["zora"]
            #                           , request_kwargs={
            # 'proxies': {'https': "http://pnorwyha:snmfocltb81h@45.192.134.110:6431",
            #             'http':  "http://pnorwyha:snmfocltb81h@45.192.134.110:6431"}}
                                      ))

        logger.info(f"Successfully connected to {rpcs['zora']}")


        try:
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)

            logger.info(f"Wallet address: {wallet_address}")
            logger.info(f"Balance in ZORA network: {web3.from_wei(wallet_balance, 'ether')}")

            contract = web3.eth.contract(address=Web3.to_checksum_address(nft_address), abi=nft_contract_abi)

            mint_tx = contract.functions.mint(
                "0x169d9147dFc9409AfA4E558dF2C9ABeebc020182",
                nft_id,
                1,
                Web3.to_hex(b'\x00' * 12 + Web3.to_bytes(hexstr=wallet_address)),
            ).build_transaction({
                'from': web3.to_checksum_address(wallet_address),
                'value': web3.to_wei(0.000777, 'ether'),
                'gas': 150000,
                #'gasPrice': web3.to_wei(0.005, 'gwei'),
                'nonce': web3.eth.get_transaction_count(wallet_address),
                'maxPriorityFeePerGas': web3.to_wei(0.005, 'gwei'),
                'maxFeePerGas': web3.to_wei(0.005, 'gwei')
            })

            signed_mint_tx = web3.eth.account.sign_transaction(mint_tx, self.pk)
            raw_mint_tx_hash = web3.eth.send_raw_transaction(signed_mint_tx.rawTransaction)
            mint_tx_hash = web3.to_hex(raw_mint_tx_hash)

            logger.info(f"Mint tx hash: {mint_tx_hash}")

            for i in range(5):
                await asyncio.sleep(5)
                try:
                    mint_tx_receipt = web3.eth.wait_for_transaction_receipt(raw_mint_tx_hash, timeout=300)

                    if mint_tx_receipt.status == 1:
                        logger.info(f"✅ Transaction: https://explorer.zora.energy/tx/{mint_tx_hash}, {nft_address}")
                        return "✅"
                    else:
                        logger.error(f"⛔ Something went wrong while minting, {nft_address}")
                        return "❌ Something went wrong"
                except ex3.TransactionNotFound as err:
                    logger.error(f"⛔ Something went wrong while minting: {err}, {nft_address}")
                    continue
                except Exception as err:
                    logger.error(f"⛔ Something went wrong while minting: {err}, {nft_address}")
                    return "❌ Something went wrong"

        except Exception as err:
            if "insufficient funds" and "have" in str(err):
                have = int(re.search(r'have (\d+)', err.args[0]['message']).group(1))
                want = int(re.search(r'want (\d+)', err.args[0]['message']).group(1))
                gas = int(re.search(r'gas (\d+)', err.args[0]['message']).group(1))
                logger.error(f"Insufficient funds for gas * price + value. Want: {want} Have: {have} Gas: {gas}, {nft_address}")
                return "❌ Insufficient funds for gas"
            elif "insufficient funds" in str(err):
                logger.error(f"Insufficient funds for gas * price + value, {nft_address}")
                return "❌ Insufficient funds for gas"
            else:
                logger.error(f"TOTAL something went wrong: {err}, {nft_address}")
                return "❌ Something went wrong"

    async def purchase(self, nft_contract_address, value_to_send): # ZoraCreator1155Impl

        web3 = Web3(Web3.HTTPProvider(rpcs["zora"]
            #                           , request_kwargs={
            # 'proxies': {'https': "http://pnorwyha:snmfocltb81h@45.192.134.110:6431",
            #             'http': "http://pnorwyha:snmfocltb81h@45.192.134.110:6431"}}
                                      ))

        logger.info(f"Successfully connected to {rpcs['zora']}")

        try:
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)

            logger.info(f"Wallet address: {wallet_address}")
            logger.info(f"Balance in ZORA network: {web3.from_wei(wallet_balance, 'ether')}")

            contract = web3.eth.contract(address=Web3.to_checksum_address(nft_contract_address), abi=nft_ZoraCreator_contract_abi)

            mint_tx = contract.functions.purchase(
                1
            ).build_transaction({
                'from': web3.to_checksum_address(wallet_address),
                'value': web3.to_wei(value_to_send, 'ether'),
                'gas': 150000,
                # 'gasPrice': web3.to_wei(0.005, 'gwei'),
                'nonce': web3.eth.get_transaction_count(wallet_address),
                'maxPriorityFeePerGas': web3.to_wei(0.005, 'gwei'),
                'maxFeePerGas': web3.to_wei(0.005, 'gwei')
            })

            signed_mint_tx = web3.eth.account.sign_transaction(mint_tx, self.pk)
            raw_mint_tx_hash = web3.eth.send_raw_transaction(signed_mint_tx.rawTransaction)
            mint_tx_hash = web3.to_hex(raw_mint_tx_hash)

            logger.info(f"Mint tx hash: {mint_tx_hash}")

            for i in range(5):
                await asyncio.sleep(5)
                try:
                    mint_tx_receipt = web3.eth.wait_for_transaction_receipt(raw_mint_tx_hash, timeout=300)

                    if mint_tx_receipt.status == 1:
                        logger.info(f"✅ Transaction: https://explorer.zora.energy/tx/{mint_tx_hash}, {nft_contract_address}")
                        return "✅"
                    else:
                        logger.error(f"⛔ Something went wrong while minting, {nft_contract_address}")
                except ex3.TransactionNotFound as err:
                    logger.error(f"⛔ Something went wrong while minting: {err}, {nft_contract_address}")
                    continue
                except Exception as err:
                    logger.error(f"⛔ TOTAL went wrong while minting: {err}, {nft_contract_address}")
                    return "❌ Something went wrong "

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
                logger.error(f"Something went wrong: {err}, {nft_contract_address}")
                return "❌ Something went wrong"

    async def createERC721(self, name, symbol, mintPrice, mintLimitPerAddress, editionSize, royaltyBPS, description, imageURI): # ZoraNFTCreator

        web3 = Web3(Web3.HTTPProvider(rpcs["zora"], request_kwargs={
                                       'proxies': {'https': "http://pnorwyha:snmfocltb81h@216.173.109.154:6385",
                                                   'http': "http://pnorwyha:snmfocltb81h@216.173.109.154:6385"}}
                                      ))

        logger.info(f"Successfully connected to {rpcs['zora']}")

        try:
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)

            logger.info(f"Wallet address: {wallet_address}")
            logger.info(f"Balance in ZORA network: {web3.from_wei(wallet_balance, 'ether')}")

            contract = web3.eth.contract(address=Web3.to_checksum_address("0xA2c2A96A232113Dd4993E8b048EEbc3371AE8d85"), abi=ZoraNFTCreator_contract_abi)

            create_tx = contract.functions.createEdition(
                name=name,
                symbol=symbol,
                editionSize=editionSize,
                royaltyBPS=int(royaltyBPS*100), # royalty = 3% => royaltyBPS = 3*100
                fundsRecipient=wallet_address,
                defaultAdmin=wallet_address,
                saleConfig=[web3.to_wei(mintPrice, 'ether'), mintLimitPerAddress, 1691759829, 18446744073709551615, 0, 0, b"0x000000000000000000000000000000"],
                description=description,
                animationURI="",
                imageURI=imageURI
            ).build_transaction({
                'from': web3.to_checksum_address(wallet_address),
                'nonce': web3.eth.get_transaction_count(wallet_address),
                'maxPriorityFeePerGas': web3.to_wei(0.005, 'gwei'),
                'maxFeePerGas': web3.to_wei(0.005, 'gwei')
            })

            signed_create_tx = web3.eth.account.sign_transaction(create_tx, self.pk)
            raw_create_tx_hash = web3.eth.send_raw_transaction(signed_create_tx.rawTransaction)
            create_tx_hash = web3.to_hex(raw_create_tx_hash)

            logger.info(f"Contract create tx hash: {create_tx_hash}")

            for i in range(5):
                await asyncio.sleep(5)
                try:
                    create_tx_receipt = web3.eth.wait_for_transaction_receipt(raw_create_tx_hash, timeout=300)

                    if create_tx_receipt.status == 1:
                        log = create_tx_receipt['logs'][-1]

                        if log:
                            self.collectionAddress = "0x" + log['topics'][2].hex()[-40:]

                        logger.info(f"Created collection address: {self.collectionAddress}")
                        logger.info(f"✅ Transaction: https://explorer.zora.energy/tx/{create_tx_hash}")
                        return "✅"
                    else:
                        logger.error("Something went wrong while contract creating")
                        return "❌ Something went wrong"
                except ex3.TransactionNotFound as err:
                    logger.error(f"Something went wrong while minting: {err}")
                    continue
                except Exception as err:
                    logger.error(f"Something went wrong while contract creating: {err}")
                    return "❌ Something went wrong"

        except Exception as err:
            if "insufficient funds" in str(err):
                logger.error(f"Insufficient funds for gas * price + value.")
                return "❌ Insufficient funds for gas"
            else:
                logger.error(f"Something went wrong in createERC721: {err}")
                return "❌ Something went wrong"

    async def walletWarmUp1(self, nft_collection_address, uri): # Mint web page update emulating
        web3 = Web3(Web3.HTTPProvider(rpcs["zora"], request_kwargs={
                                       'proxies': {'https': "http://pnorwyha:snmfocltb81h@216.173.109.154:6385",
                                                   'http': "http://pnorwyha:snmfocltb81h@216.173.109.154:6385"}}
                                      ))
        try:
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)

            logger.info(f"Wallet address: {wallet_address}")
            logger.info(f"Balance in ZORA network: {web3.from_wei(wallet_balance, 'ether')}")
            logger.info(f"nft_collection_address {nft_collection_address}")
            logger.info(f"uri {uri}")

            contract = web3.eth.contract(address=Web3.to_checksum_address("0xABCDEFEd93200601e1dFe26D6644758801D732E8"),
                                         abi=JSONExtensionRegistry_contract_abi)

            warm_tx = contract.functions.setJSONExtension(
                    target=Web3.to_checksum_address(nft_collection_address),
                    uri=uri
            ).build_transaction({
                'from': web3.to_checksum_address(wallet_address),
                'nonce': web3.eth.get_transaction_count(wallet_address),
                'maxPriorityFeePerGas': web3.to_wei(0.005, 'gwei'),
                'maxFeePerGas': web3.to_wei(0.005, 'gwei')
            })

            signed_warm_tx = web3.eth.account.sign_transaction(warm_tx, self.pk)
            raw_warm_tx_hash = web3.eth.send_raw_transaction(signed_warm_tx.rawTransaction)
            warm_tx_hash = web3.to_hex(raw_warm_tx_hash)

            logger.info(f"Warming up tx hash: {warm_tx_hash}")

            for i in range(5):
                await asyncio.sleep(5)
                try:
                    create_tx_receipt = web3.eth.wait_for_transaction_receipt(raw_warm_tx_hash, timeout=300)
                    if create_tx_receipt.status == 1:
                        logger.info(f"✅ Transaction: https://explorer.zora.energy/tx/{warm_tx_hash}")
                        return "✅"
                    else:
                        logger.error("Something went wrong while  warming up1")
                        return "❌ Something went wrong"
                except ex3.TransactionNotFound as err:
                    logger.error(f"Something went wrong while  warming up1: {err}")
                    continue
                except Exception as err:
                    logger.error(f"Something went wrong while warming up1: {err}")
                    return "❌ Something went wrong"

        except Exception as err:
            if "insufficient funds" in str(err):
                logger.error(f"Insufficient funds for gas * price + value.")
                return "❌ Insufficient funds for gas"
            else:
                logger.error(f"Something went wrong: {err}")
                return "❌ Something went wrong"

    async def walletWarmUp2(self, nft_collection_address, publicSalePrice):  # Mint price updating
        web3 = Web3(Web3.HTTPProvider(rpcs["zora"], request_kwargs={
                                       'proxies': {'https': "http://pnorwyha:snmfocltb81h@216.173.109.154:6385",
                                                   'http': "http://pnorwyha:snmfocltb81h@216.173.109.154:6385"}}
                                      ))


        try:
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)

            logger.info(f"Wallet address: {wallet_address}")
            logger.info(f"Balance in ZORA network: {web3.from_wei(wallet_balance, 'ether')}")
            logger.info(f"nft_collection_address {nft_collection_address}")
            logger.info(f"publicSalePrice {publicSalePrice}")

            contract = web3.eth.contract(address=Web3.to_checksum_address(nft_collection_address),
                                         abi=nft_ZoraCreator_contract_abi)

            warm_tx = contract.functions.setSaleConfiguration(
                publicSalePrice=web3.to_wei(publicSalePrice, 'ether'),
                maxSalePurchasePerAddress=4294967295,
                publicSaleStart=int(time.time()),
                publicSaleEnd=18446744073709551615,
                presaleStart=0,
                presaleEnd=0,
                presaleMerkleRoot=b"0x000000000000000000000000000000"
            ).build_transaction({
                'from': web3.to_checksum_address(wallet_address),
                'nonce': web3.eth.get_transaction_count(wallet_address),
                'maxPriorityFeePerGas': web3.to_wei(0.005, 'gwei'),
                'maxFeePerGas': web3.to_wei(0.005, 'gwei')
            })

            signed_warm_tx = web3.eth.account.sign_transaction(warm_tx, self.pk)
            raw_warm_tx_hash = web3.eth.send_raw_transaction(signed_warm_tx.rawTransaction)
            warm_tx_hash = web3.to_hex(raw_warm_tx_hash)

            logger.info(f"Warming up tx hash: {warm_tx_hash}")

            for i in range(5):
                await asyncio.sleep(5)
                try:
                    create_tx_receipt = web3.eth.wait_for_transaction_receipt(raw_warm_tx_hash, timeout=300)
                    if create_tx_receipt.status == 1:
                        logger.info(f"✅ Transaction: https://explorer.zora.energy/tx/{warm_tx_hash}")
                        return "✅"
                    else:
                        logger.error("Something went wrong while  warming up2")
                        return "❌ Something went wrong"
                except web3.exceptions.TransactionNotFound as err:
                    logger.error(f"Something went wrong while  warming up2: {err}")
                    continue
                except Exception as err:
                    logger.error(f"Something went wrong while warming up2: {err}")
                    return "❌ Something went wrong"

        except Exception as err:
            if "insufficient funds" in str(err):
                logger.error(f"Insufficient funds for gas * price + value.")
                return "❌ Insufficient funds for gas"
            else:
                logger.error(f"Something went wrong: {err}")
                return "❌ Something went wrong"

    @staticmethod
    def generateUri(length=50, prefix="baf"):
        characters = string.ascii_lowercase + string.digits
        random_chars = ''.join(random.choice(characters) for _ in range(length - len(prefix)))
        return prefix + random_chars

    async def mintfun(self, nft_address, nft_name: str):

        web3 = Web3(Web3.HTTPProvider(rpcs["zora"], request_kwargs={
                                       'proxies': {'https': "http://pnorwyha:snmfocltb81h@216.173.109.154:6385",
                                                   'http': "http://pnorwyha:snmfocltb81h@216.173.109.154:6385"}}
                                      ))

        logger.info(f"Successfully connected to {rpcs['zora']}")


        try:
            wallet_address = web3.eth.account.from_key(self.pk).address
            wallet_balance = web3.eth.get_balance(wallet_address)

            logger.info(f"Wallet address: {wallet_address}")
            logger.info(f"Balance in ZORA network: {web3.from_wei(wallet_balance, 'ether')}")


            if nft_name == "Blocks":
                contract = web3.eth.contract(address=Web3.to_checksum_address(nft_address), abi=blocks_contract_abi)
                mint_tx = contract.functions.mint(

                ).build_transaction({
                    'from': web3.to_checksum_address(wallet_address),
                    'gas': 150000,
                    'nonce': web3.eth.get_transaction_count(wallet_address),
                    'maxPriorityFeePerGas': web3.to_wei(0.005, 'gwei'),
                    'maxFeePerGas': web3.to_wei(0.005, 'gwei')
                })

                signed_mint_tx = web3.eth.account.sign_transaction(mint_tx, self.pk)
                raw_mint_tx_hash = web3.eth.send_raw_transaction(signed_mint_tx.rawTransaction)
                mint_tx_hash = web3.to_hex(raw_mint_tx_hash)

                logger.info(f"Mint tx hash: {mint_tx_hash}")

                for _ in range(5):
                    await asyncio.sleep(5)
                    try:
                        mint_tx_receipt = web3.eth.wait_for_transaction_receipt(raw_mint_tx_hash, timeout=300)

                        if mint_tx_receipt.status == 1:
                            logger.info(f"✅ Transaction: https://explorer.zora.energy/tx/{mint_tx_hash}, {nft_address}")
                            return "✅"
                        else:
                            logger.error(f"⛔ Something went wrong while minting, {nft_address}")
                            return "❌ Something went wrong"
                    except ex3.TransactionNotFound as err:
                        logger.error(f"⛔ Something went wrong while minting: {err}, {nft_address}")
                        continue
                    except Exception as err:
                        logger.error(f"⛔ Something went wrong while minting: {err}, {nft_address}")
                        return "❌ Something went wrong"

            elif nft_name == "The Mancer":
                contract = web3.eth.contract(address=Web3.to_checksum_address(nft_address), abi=mint_contract_abi)

                mint_tx = contract.functions.mint(
                    10 # 50 and 100 available
                ).build_transaction({
                    'from': web3.to_checksum_address(wallet_address),
                    'value': web3.to_wei(0.00009965, 'ether'),
                    'gas': 150000,
                    'nonce': web3.eth.get_transaction_count(wallet_address),
                    'maxPriorityFeePerGas': web3.to_wei(0.005, 'gwei'),
                    'maxFeePerGas': web3.to_wei(0.005, 'gwei')
                })

                signed_mint_tx = web3.eth.account.sign_transaction(mint_tx, self.pk)
                raw_mint_tx_hash = web3.eth.send_raw_transaction(signed_mint_tx.rawTransaction)
                mint_tx_hash = web3.to_hex(raw_mint_tx_hash)

                logger.info(f"Mint tx hash: {mint_tx_hash}")

                for _ in range(5):
                    await asyncio.sleep(5)
                    try:
                        mint_tx_receipt = web3.eth.wait_for_transaction_receipt(raw_mint_tx_hash, timeout=300)

                        if mint_tx_receipt.status == 1:
                            logger.info(f"✅ Transaction: https://explorer.zora.energy/tx/{mint_tx_hash}, {nft_address}")
                            return "✅"
                        else:
                            logger.error(f"⛔ Something went wrong while minting, {nft_address}")
                            return "❌ Something went wrong"
                    except ex3.TransactionNotFound as err:
                        logger.error(f"⛔ Something went wrong while minting: {err}, {nft_address}")
                        continue
                    except Exception as err:
                        logger.error(f"⛔ Something went wrong while minting: {err}, {nft_address}")
                        return "❌ Something went wrong"

            elif nft_name == "sqr(16)":
                contract = web3.eth.contract(address=Web3.to_checksum_address(nft_address), abi=mint_contract_abi)

                mint_tx = contract.functions.mint(
                    4 # 16 or 64 not for free
                ).build_transaction({
                    'from': web3.to_checksum_address(wallet_address),
                    'gas': 150000,
                    'nonce': web3.eth.get_transaction_count(wallet_address),
                    'maxPriorityFeePerGas': web3.to_wei(0.005, 'gwei'),
                    'maxFeePerGas': web3.to_wei(0.005, 'gwei')
                })

                signed_mint_tx = web3.eth.account.sign_transaction(mint_tx, self.pk)
                raw_mint_tx_hash = web3.eth.send_raw_transaction(signed_mint_tx.rawTransaction)
                mint_tx_hash = web3.to_hex(raw_mint_tx_hash)

                logger.info(f"Mint tx hash: {mint_tx_hash}")

                for _ in range(5):
                    await asyncio.sleep(5)
                    try:
                        mint_tx_receipt = web3.eth.wait_for_transaction_receipt(raw_mint_tx_hash, timeout=300)

                        if mint_tx_receipt.status == 1:
                            logger.info(f"✅ Transaction: https://explorer.zora.energy/tx/{mint_tx_hash}, {nft_address}")
                            return "✅"
                        else:
                            logger.error(f"⛔ Something went wrong while minting, {nft_address}")
                            return "❌ Something went wrong"
                    except ex3.TransactionNotFound as err:
                        logger.error(f"⛔ Something went wrong while minting: {err}, {nft_address}")
                        continue
                    except Exception as err:
                        logger.error(f"⛔ Something went wrong while minting: {err}, {nft_address}")
                        return "❌ Something went wrong"

            elif nft_name == "Yassin Art on Zora":
                contract = web3.eth.contract(address=Web3.to_checksum_address(nft_address), abi=yassin_contract_abi)
                mint_tx = contract.functions.Mint(
                    11  # 30 and 500 available
                ).build_transaction({
                    'from': web3.to_checksum_address(wallet_address),
                    'value': web3.to_wei(0.00007754, 'ether'),
                    'gas': 150000,
                    'nonce': web3.eth.get_transaction_count(wallet_address),
                    'maxPriorityFeePerGas': web3.to_wei(0.005, 'gwei'),
                    'maxFeePerGas': web3.to_wei(0.005, 'gwei')
                })

                signed_mint_tx = web3.eth.account.sign_transaction(mint_tx, self.pk)
                raw_mint_tx_hash = web3.eth.send_raw_transaction(signed_mint_tx.rawTransaction)
                mint_tx_hash = web3.to_hex(raw_mint_tx_hash)

                logger.info(f"Mint tx hash: {mint_tx_hash}")

                for _ in range(5):
                    await asyncio.sleep(5)
                    try:
                        mint_tx_receipt = web3.eth.wait_for_transaction_receipt(raw_mint_tx_hash, timeout=300)

                        if mint_tx_receipt.status == 1:
                            logger.info(f"✅ Transaction: https://explorer.zora.energy/tx/{mint_tx_hash}, {nft_address}")
                            return "✅"
                        else:
                            logger.error(f"⛔ Something went wrong while minting, {nft_address}")
                            return "❌ Something went wrong"
                    except ex3.TransactionNotFound as err:
                        logger.error(f"⛔ Something went wrong while minting: {err}, {nft_address}")
                        continue
                    except Exception as err:
                        logger.error(f"⛔ Something went wrong while minting: {err}, {nft_address}")
                        return "❌ Something went wrong"

        except Exception as err:
            if "insufficient funds" and "have" in str(err):
                have = int(re.search(r'have (\d+)', err.args[0]['message']).group(1))
                want = int(re.search(r'want (\d+)', err.args[0]['message']).group(1))
                gas = int(re.search(r'gas (\d+)', err.args[0]['message']).group(1))
                logger.error(f"Insufficient funds for gas * price + value. Want: {want} Have: {have} Gas: {gas}, {nft_address}")
                return "❌ Insufficient funds for gas"
            elif "insufficient funds" in str(err):
                logger.error(f"Insufficient funds for gas * price + value, {nft_address}")
                return "❌ Insufficient funds for gas"
            else:
                logger.error(f"TOTAL something went wrong: {err}, {nft_address}")
                return "❌ Something went wrong"


#if __name__ == "__main__":
    #asyncio.run(minter.mintfun("0x1F781d47cD59257D7AA1Bd7b2fbaB50D57AF8587", nft_name="Blocks"))
    #asyncio.run(minter.mintfun("0x3a577c80f5834B0150DEFEa2AB71Ae7AEF5f463d", nft_name="The Mancer"))
    #asyncio.run(minter.mintfun("0xbC2cA61440fAF65a9868295Efa5d5D87c55B9529", nft_name="sqr(16)"))
    #asyncio.run(minter.mintfun("0xD425b16d3eF1a1ec0AB9b3f6CBeFD5Fe6BE42259", nft_name="Yassin Art on Zora"))
