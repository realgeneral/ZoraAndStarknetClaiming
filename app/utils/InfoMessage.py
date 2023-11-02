from dataclasses import dataclass


@dataclass
class InfoMessage:
    def __init__(self):
        pass

    info_route_stark = """
<b>🎡Starknet🎡</b>

<i>Available routes:</i>
                        
<b>1. Warmup route</b> (Run only if you have done the <b>medium route</b> at least once)
                        
Price per 1 run: <s>$3 USD</s> 🔥 $1.5 USD 🔥
                        
- 4-5 swaps on each DEX (AvnuFi, Jediswap, 10K Swap)
- 5-6 Dmail-messages
- Anti-sybil cluster system
- <i>New functions s00n..</i>
                        
<b>2. Medium route</b>
                        
Price per 1 run: <s>$5 USD</s> 🔥 $2.5 USD 🔥
                        
- Wallet Deployer 
- 4-6 swaps on each DEX (AvnuFi, Jediswap, 10K Swap)
- NFT mint (StarkNetID NFT, Starkverse NFT)
- 6-8 Dmail-messages 
- Anti-sybil cluster system
                        
<b>3. Premium route</b>
                        
<i>S00N...</i> 
     """

    info_route_zora: str


Info = InfoMessage()