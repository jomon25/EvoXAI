import random
from strategies.dna import StrategyDNA

class IntradayGenerator:
    """Intraday strategy generator."""
    TIMEFRAMES = ['1min', '5min', '15min']
    ENTRY_CONDITIONS = [
        'Opening range breakout',
        'VWAP deviation cross',
        'News catalyst window'
    ]
    EXIT_CONDITIONS = ['End of day', 'Session high/low reached']

    def generate(self) -> StrategyDNA:
        return StrategyDNA(
            style='intraday',
            timeframe=random.choice(self.TIMEFRAMES),
            entry_conditions=random.sample(self.ENTRY_CONDITIONS, k=1),
            exit_conditions=random.sample(self.EXIT_CONDITIONS, k=1),
            filters=['Volume confirmation'],
            parameters={
                'vwap_dev': random.uniform(1.0, 3.0),
            },
            risk_params={
                'risk_percent': random.uniform(0.005, 0.015),
                'rr_ratio': random.uniform(1.0, 3.0),
                'max_positions': random.randint(1, 5),
            }
        )
