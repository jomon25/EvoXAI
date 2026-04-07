import random
from strategies.dna import StrategyDNA
from strategies.generators.smc import SMCGenerator
from strategies.generators.ict import ICTGenerator
from strategies.generators.snr import SnRGenerator
from strategies.generators.intraday import IntradayGenerator
from strategies.generators.swing import SwingGenerator
from strategies.generators.scalping import ScalpingGenerator

class StyleRouter:
    GENERATORS = {
        'smc': SMCGenerator(), 'ict': ICTGenerator(),
        'snr': SnRGenerator(), 'intraday': IntradayGenerator(),
        'swing': SwingGenerator(), 'scalping': ScalpingGenerator()
    }

    def generate(self, style: str | None = None) -> StrategyDNA:
        style = style or random.choice(list(self.GENERATORS))
        return self.GENERATORS[style].generate()

    def generate_batch(self, n: int = 100, style: str | None = None) -> list[StrategyDNA]:
        return [self.generate(style) for _ in range(n)]
