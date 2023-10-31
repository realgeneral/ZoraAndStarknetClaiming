from dataclasses import dataclass

@dataclass
class ServicePrices:
    warm_up_zora: float
    main_zora: float
    warm_up_stark: float
    medium_stark: float
    premium_stark: float
