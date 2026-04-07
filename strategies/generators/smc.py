import random
from strategies.dna import StrategyDNA

class SMCGenerator:
    """Smart Money Concepts strategy generator."""
    TIMEFRAMES = ['5min', '15min', '1h', '4h', '1d']
    ENTRY_CONDITIONS = [
        'Price returns to order block after liquidity sweep',
        'CHoCH (Change of Character) confirmed on lower timeframe',
        'Fair Value Gap present and price entering it',
        'Breaker block reclaimed above/below key level',
        'Inducement sweep followed by strong displacement',
    ]
    EXIT_CONDITIONS = [
        'Next liquidity pool reached',
        'Order block invalidated (candle close beyond stop)',
        'Premium/Discount reached on Fibonacci',
    ]

    def generate(self) -> StrategyDNA:
        return StrategyDNA(
            style='smc',
            timeframe=random.choice(self.TIMEFRAMES),
            entry_conditions=random.sample(self.ENTRY_CONDITIONS, k=random.randint(1, 3)),
            exit_conditions=random.sample(self.EXIT_CONDITIONS, k=1),
            filters=random.sample(['FVG confirmation', 'Volume spike', 'HTF alignment',
                                   'Session killzone', 'Sweep confirmation'], k=2),
            parameters={
                'ob_tolerance': random.uniform(0.001, 0.005),
                'fvg_min_size': random.uniform(0.001, 0.003),
                'sweep_confirm_bars': random.randint(1, 3),
                'choch_lookback': random.randint(5, 20),
            },
            risk_params={
                'risk_percent': random.uniform(0.005, 0.02),
                'rr_ratio': random.uniform(1.5, 4.0),
                'max_positions': random.randint(1, 3),
            }
        )
