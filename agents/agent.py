import random, numpy as np
from strategies.dna import StrategyDNA

class TradingAgent:
    def __init__(self, agent_id: int, capital: float = 10_000):
        self.id = agent_id
        self.capital = capital
        self.equity_curve = [capital]
        self.trades:list = []
        self.dna = self._random_dna()

    def _random_dna(self) -> dict:
        return {
            'rsi_threshold': random.uniform(25, 40),
            'trend_window': random.randint(5, 20),
            'vol_filter': random.uniform(0.8, 2.0),
            'risk_factor': random.uniform(0.5, 1.5),
        }

    def act(self, market_state: dict, crowd_sentiment: float) -> float:
        signal = 1.0 if market_state.get('momentum', 0) > 0 else -1.0
        
        # Anti-herding: fade the crowd when sentiment is extreme
        if abs(crowd_sentiment) > 0.7:
            signal = -signal
            
        vol_ok = market_state.get('vol_ratio', 1.0) > self.dna['vol_filter'] * 0.5
        return signal * self.dna['risk_factor'] * 0.01 * self.capital if vol_ok else 0.0

    def update_pnl(self, pnl: float) -> None:
        self.capital += pnl
        self.equity_curve.append(self.capital)

    @property
    def fitness(self) -> float:
        rets = np.diff(self.equity_curve) / (np.array(self.equity_curve[:-1]) + 1e-9)
        return (np.mean(rets) / (np.std(rets) + 1e-9)) * np.sqrt(252) if len(rets) > 1 else 0.0
