import random
from strategies.dna import StrategyDNA

class ICTGenerator:
    """ICT strategy generator."""
    TIMEFRAMES = ['5min', '15min', '1h', '4h', '1d']
    ENTRY_CONDITIONS = [
        'Killzone entry',
        'New Week Open Gap touch',
        'Optimal Trade Entry (OTE) 0.618-0.786 Fib'
    ]
    EXIT_CONDITIONS = ['Liquidity pool reached', 'Time stop hit']

    def generate(self) -> StrategyDNA:
        return StrategyDNA(
            style='ict',
            timeframe=random.choice(self.TIMEFRAMES),
            entry_conditions=random.sample(self.ENTRY_CONDITIONS, k=1),
            exit_conditions=random.sample(self.EXIT_CONDITIONS, k=1),
            filters=['Killzone confirmation'],
            parameters={
                'ote_fib_level': random.uniform(0.618, 0.786),
            },
            risk_params={
                'risk_percent': random.uniform(0.005, 0.02),
                'rr_ratio': random.uniform(1.5, 4.0),
                'max_positions': random.randint(1, 2),
            }
        )
