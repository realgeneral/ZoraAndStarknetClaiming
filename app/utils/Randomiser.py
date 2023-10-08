import random


class Randomiser:

    @staticmethod
    def mintPrice():
        return round(random.uniform(0.00001, 3), 5)

    @staticmethod
    def mintLimitPerAddress():
        return random.randint(2, 5000)

    @staticmethod
    def editionSize():
        return random.randint(10, 9999)

    @staticmethod
    def royaltyBPS():
        return random.randint(1, 15)

    @staticmethod
    def average_time(n, func):
        return int(sum(func() for _ in range(n)) / 60)

    @staticmethod
    def random_bridge():
        return random.randint(45, 90)
    @staticmethod
    def random_bridge_after():
        return random.randint(90, 120)
    @staticmethod
    def random_contract():
        return random.randint(120, 150)
    @staticmethod
    def random_contract_after():
        return random.randint(100, 200)
    @staticmethod
    def random_warm_up():
        return random.randint(90, 120)
    @staticmethod
    def random_warm_up_after():
        return random.randint(500, 600)
    @staticmethod
    def random_mint():
        return random.randint(60, 80)
    @staticmethod
    def random_mint_after():
        return random.randint(300, 500)
