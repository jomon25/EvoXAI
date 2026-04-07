import random
from strategies.dna import StrategyDNA

class SwingGenerator:
    """Swing strategy generator."""
    TIMEFRAMES = ['4h', '1d', '1w']
    ENTRY_CONDITIONS = [
        'Multi-timeframe trend confirmation',
        'MACD divergence',
        'Key weekly level rejection'
    ]
    EXIT_CONDITIONS = ['Trend reversal', 'Opposite divergence']

    def generate(self) -> StrategyDNA:
        return StrategyDNA(
            style='swing',
            timeframe=random.choice(self.TIMEFRAMES),
            entry_conditions=random.sample(self.ENTRY_CONDITIONS, k=1),
            exit_conditions=random.sample(self.EXIT_CONDITIONS, k=1),
            filters=['RSI filter'],
            parameters={
                'macd_fast': random.randint(8, 15),
                'macd_slow': random.randint(20, 30),
            },
            risk_params={
                'risk_percent': random.uniform(0.01, 0.05),
                'rr_ratio': random.uniform(2.0, 6.0),
                'max_positions': random.randint(1, 4),
            }
        )
