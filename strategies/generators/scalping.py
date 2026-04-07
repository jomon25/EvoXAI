import random
from strategies.dna import StrategyDNA

class ScalpingGenerator:
    """Scalping strategy generator."""
    TIMEFRAMES = ['1min', '3min']
    ENTRY_CONDITIONS = [
        'Bid-ask spread aware entry',
        'Microstructure signal',
        'Rapid volatility expansion'
    ]
    EXIT_CONDITIONS = ['Small profit target hit', 'Dynamic trailing stop']

    def generate(self) -> StrategyDNA:
        return StrategyDNA(
            style='scalping',
            timeframe=random.choice(self.TIMEFRAMES),
            entry_conditions=random.sample(self.ENTRY_CONDITIONS, k=1),
            exit_conditions=random.sample(self.EXIT_CONDITIONS, k=1),
            filters=['Spread limit filter'],
            parameters={
                'spread_limit': random.uniform(0.0001, 0.0005),
            },
            risk_params={
                'risk_percent': random.uniform(0.001, 0.005),
                'rr_ratio': random.uniform(1.0, 2.0),
                'max_positions': random.randint(1, 10),
            }
        )
