import random
from strategies.dna import StrategyDNA

class SnRGenerator:
    """Malaysian SnR strategy generator."""
    TIMEFRAMES = ['1h', '4h', '1d']
    ENTRY_CONDITIONS = [
        'Weekly close support bounce',
        'Demand/supply zone entry',
        'Confluence scoring above threshold'
    ]
    EXIT_CONDITIONS = ['Next zone reached', 'Trailing stop loss']

    def generate(self) -> StrategyDNA:
        return StrategyDNA(
            style='snr',
            timeframe=random.choice(self.TIMEFRAMES),
            entry_conditions=random.sample(self.ENTRY_CONDITIONS, k=1),
            exit_conditions=random.sample(self.EXIT_CONDITIONS, k=1),
            filters=['Price action confirmation'],
            parameters={
                'zone_tolerance': random.uniform(0.001, 0.005),
            },
            risk_params={
                'risk_percent': random.uniform(0.01, 0.03),
                'rr_ratio': random.uniform(2.0, 5.0),
                'max_positions': random.randint(1, 3),
            }
        )
